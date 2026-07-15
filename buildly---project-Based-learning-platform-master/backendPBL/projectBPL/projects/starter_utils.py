import io
import zipfile

from django.core.files.base import ContentFile


def _normalize_zip_path(path):
    return path.replace('\\', '/').lstrip('./')


def _should_skip_zip_path(path):
    normalized = _normalize_zip_path(path)
    if not normalized or normalized.endswith('/'):
        return True

    parts = normalized.split('/')
    return '.DS_Store' in parts or '__MACOSX' in parts


def build_starter_zip_from_uploads(uploaded_files, zip_name='starter.zip'):
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
        added_files = 0

        for uploaded in uploaded_files:
            arcname = _normalize_zip_path(uploaded.name)
            if _should_skip_zip_path(arcname):
                continue

            archive.writestr(arcname, uploaded.read())
            added_files += 1

    if added_files == 0:
        raise ValueError('المجلد المرفوع فارغ أو لا يحتوي على ملفات صالحة')

    buffer.seek(0)
    return ContentFile(buffer.getvalue(), name=zip_name)
