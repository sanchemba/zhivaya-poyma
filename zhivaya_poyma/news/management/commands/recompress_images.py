from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from PIL import Image, ImageOps, UnidentifiedImageError


class Command(BaseCommand):
    help = "Safely recompress images in MEDIA_ROOT/news and/or MEDIA_ROOT/uploads"

    def add_arguments(self, parser):
        parser.add_argument(
            "--target",
            choices=["all", "news", "uploads"],
            default="all",
            help="Which directory to process: all, news, or uploads",
        )
        parser.add_argument(
            "--quality",
            type=int,
            default=80,
            help="JPEG/WEBP quality (default: 80)",
        )
        parser.add_argument(
            "--max-width",
            type=int,
            default=1800,
            help="Maximum width/height in pixels (default: 1800)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be changed without rewriting files",
        )
        parser.add_argument(
            "--skip-small",
            type=int,
            default=300 * 1024,
            help="Skip files smaller than this many bytes (default: 307200 = 300KB)",
        )

    def handle(self, *args, **options):
        target = options["target"]
        quality = options["quality"]
        max_width = options["max_width"]
        dry_run = options["dry_run"]
        skip_small = options["skip_small"]

        media_root = Path(settings.MEDIA_ROOT)

        target_dirs = []
        if target in ("all", "news"):
            target_dirs.append(media_root / "news")
        if target in ("all", "uploads"):
            target_dirs.append(media_root / "uploads")

        processed = 0
        skipped = 0
        failed = 0
        total_before = 0
        total_after = 0

        for target_dir in target_dirs:
            if not target_dir.exists():
                self.stdout.write(self.style.WARNING(f"Directory not found: {target_dir}"))
                continue

            self.stdout.write(self.style.NOTICE(f"Processing: {target_dir}"))

            for file_path in target_dir.rglob("*"):
                if not file_path.is_file():
                    continue

                ext = file_path.suffix.lower()
                if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
                    skipped += 1
                    continue

                before_size = file_path.stat().st_size
                if before_size < skip_small:
                    skipped += 1
                    continue

                try:
                    changed, after_size, note = self._process_image(
                        file_path=file_path,
                        quality=quality,
                        max_width=max_width,
                        dry_run=dry_run,
                    )

                    if changed:
                        processed += 1
                        total_before += before_size
                        total_after += after_size
                        self.stdout.write(
                            f"[OK] {file_path} | {self._fmt(before_size)} -> {self._fmt(after_size)} | {note}"
                        )
                    else:
                        skipped += 1

                except Exception as exc:
                    failed += 1
                    self.stdout.write(self.style.ERROR(f"[FAIL] {file_path}: {exc}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Processed: {processed}"))
        self.stdout.write(self.style.WARNING(f"Skipped:   {skipped}"))
        self.stdout.write(self.style.ERROR(f"Failed:    {failed}"))

        if processed:
            saved = total_before - total_after
            percent = (saved / total_before * 100) if total_before else 0
            label = "Would save" if dry_run else "Saved"
            self.stdout.write(self.style.SUCCESS(
                f"{label}:     {self._fmt(saved)} ({percent:.1f}%)"
            ))

    def _process_image(self, file_path: Path, quality: int, max_width: int, dry_run: bool):
        before_size = file_path.stat().st_size

        try:
            with Image.open(file_path) as img:
                original_format = (img.format or "").upper()
                img = ImageOps.exif_transpose(img)
                original_size = img.size

                if original_format in {"JPEG", "JPG", "WEBP"}:
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                elif original_format == "PNG":
                    if img.mode not in ("RGB", "RGBA", "P"):
                        img = img.convert("RGBA")

                img.thumbnail((max_width, max_width), Image.Resampling.LANCZOS)

                output = BytesIO()
                note_parts = []

                if img.size != original_size:
                    note_parts.append(f"resized {original_size[0]}x{original_size[1]} -> {img.size[0]}x{img.size[1]}")

                ext = file_path.suffix.lower()

                if ext in {".jpg", ".jpeg"} or original_format in {"JPEG", "JPG"}:
                    img = img.convert("RGB")
                    img.save(
                        output,
                        format="JPEG",
                        quality=quality,
                        optimize=True,
                        progressive=True,
                    )
                    note_parts.append(f"jpeg q={quality}")

                elif ext == ".webp" or original_format == "WEBP":
                    img = img.convert("RGB")
                    img.save(
                        output,
                        format="WEBP",
                        quality=quality,
                        method=6,
                    )
                    note_parts.append(f"webp q={quality}")

                elif ext == ".png" or original_format == "PNG":
                    save_img = img
                    if save_img.mode == "RGBA":
                        save_img.save(output, format="PNG", optimize=True)
                    else:
                        save_img = save_img.convert("P", palette=Image.ADAPTIVE, colors=256)
                        save_img.save(output, format="PNG", optimize=True)
                    note_parts.append("png optimized")

                else:
                    return False, before_size, "unsupported format"

                new_bytes = output.getvalue()
                after_size = len(new_bytes)

                if after_size >= before_size:
                    return False, before_size, "no gain"

                if dry_run:
                    return True, after_size, ", ".join(note_parts)

                with open(file_path, "wb") as f:
                    f.write(new_bytes)

                return True, after_size, ", ".join(note_parts)

        except UnidentifiedImageError:
            return False, before_size, "unidentified image"

    def _fmt(self, size_in_bytes: int) -> str:
        units = ["B", "KB", "MB", "GB"]
        size = float(size_in_bytes)
        for unit in units:
            if size < 1024 or unit == units[-1]:
                return f"{size:.1f} 