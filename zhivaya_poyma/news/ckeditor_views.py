import os
import uuid
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.text import get_valid_filename
from django.views.decorators.csrf import csrf_exempt
from PIL import Image, ImageOps


def _compress_uploaded_image(uploaded_file):
    img = Image.open(uploaded_file)
    img = ImageOps.exif_transpose(img)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    elif img.mode != "RGB":
        img = img.convert("RGB")

    img.thumbnail((1800, 1800), Image.Resampling.LANCZOS)

    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=80, optimize=True, progressive=True)
    buffer.seek(0)

    original_stem = Path(uploaded_file.name).stem
    safe_name = get_valid_filename(original_stem) or "image"
    filename = f"{safe_name}-{uuid.uuid4().hex[:8]}.jpg"

    return ContentFile(buffer.read(), name=filename)


@csrf_exempt
@staff_member_required
def ckeditor_image_upload(request):
    if request.method != "POST" or "upload" not in request.FILES:
        return HttpResponseBadRequest("No file uploaded.")

    uploaded_file = request.FILES["upload"]

    if not uploaded_file.content_type.startswith("image/"):
        return HttpResponseBadRequest("Only image uploads are allowed.")

    compressed_file = _compress_uploaded_image(uploaded_file)

    upload_dir = getattr(settings, "CKEDITOR_UPLOAD_PATH", "uploads/")
    save_path = os.path.join(upload_dir, compressed_file.name)

    stored_path = default_storage.save(save_path, compressed_file)
    file_url = default_storage.url(stored_path)

    return JsonResponse({
        "uploaded": 1,
        "fileName": os.path.basename(stored_path),
        "url": file_url,
    })