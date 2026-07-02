from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from PIL import Image, ImageOps, UnidentifiedImageError


class Command(BaseCommand):
    help = "Recompress existing images in MEDIA_ROOT/news and MEDIA_ROOT/uploads"

    def add_arguments(self, parser):
        parser.add_argument(
            "--quality",
            type=int,
            default=80,
            help="JPEG quality (default: 80)",
        )
        parser.add_argument(
            "--max-width",
            type=int,
            default=1800,
            help="Maximum image width/height (default: 1800)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be changed without writing files",
        )

    def handle(self, *args, **options):
        quality = options["quality"]
        max_width = options["max_width"]
        dry_run = options["dry_run"]

        media_root = Path(settings.MEDIA_ROOT)
        target_dirs = [
            media_root / "news",
            media_root / "uploads",
        ]

        processed = 0
        skipped = 0
        failed = 0
        total_saved = 0

        for target_dir in target_dirs:
            if not target_dir.exists():
                self.stdout.write(self.style.WARNING(f"Directory not found: {target_dir}"))
                continue

            for file_path in target_dir.rglob("*"):
                if not file_path.is_file():
                    continue

                if file_path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
                    skipped += 1
                    continue

                try:
                    before_size = file_path.stat().st_size
                    changed = self._recompress_image(
                        file_path=file_path,
                        quality=quality,
                        max_width=max_width,
                        dry_run=dry_run,
                    )

                    if changed:
                        after_size = file_path.stat().st_size if not dry_run else before_size
                        saved = max(before_size - after_size, 0)
                        total_saved += saved
                        processed += 1
                        self.stdout.write(
                            f"[OK] {file_path} | {self._fmt(before_size)} -> {self._fmt(after_size)}"
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
        if not dry_run:
            self.stdout.write(self.style.SUCCESS(f"Saved:     {self._fmt(total_saved)}"))

    def _recompress_image(self, file_path: Path, quality: int, max_width: int, dry_run: bool) -> bool:
        try:
            with Image.open(file_path) as img:
                original_format = (img.format or "").upper()
                img = ImageOps.exif_transpose(img)

                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                elif img.mode != "RGB":
                    img = img.convert("RGB")

                original_size = img.size
                img.thumbnail((max_width, max_width), Image.Resampling.LANCZOS)

                if dry_run:
                    return True

                save_kwargs = {"optimize": True}

                if file_path.suffix.lower() in {".jpg", ".jpeg"} or original_format in {"JPEG", "JPG"}:
                    save_kwargs.update({
                        "format": "JPEG",
                        "quality": quality,
                        "progressive": True,
                    })
                elif file_path.suffix.lower() == ".webp" or original_format == "WEBP":
                    save_kwargs.update({
                        "format": "WEBP",
                        "quality": quality,
                        "method": 6,
                    })
                else:
                    save_kwargs.update({
                        "format": "JPEG",
                        "quality": quality,
                        "progressive": True,
                    })

                if file_path.suffix.lower() == ".png":
                    new_path = file_path.with_suffix(".jpg")
                    img.save(new_path, **save_kwargs)
                    if new_path != file_path:
                        file_path.unlink(missing_ok=True)
                else:
                    img.save(file_path, **save_kwargs)

                return True

        except UnidentifiedImageError:
            return False

    def _fmt(self, size_in_bytes: int) -> str:
        units = ["B", "KB", "MB", "GB"]
        size = float(size_in_bytes)
        for unit in units:
            if size < 1024 or unit == units[-1]:
                return f"{size:.1f} {unit}"
            size /= 1024