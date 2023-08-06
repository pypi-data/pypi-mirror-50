import os
from flask import session, url_for, request, get_flashed_messages

assets_bucket = f"https://s3-{os.environ['SERVICE_REGION']}.amazonaws.com/{os.environ['ASSETS_BUCKET']}"


def get_js_path(folder, filename):
    if 'http://localhost' in request.host_url:
        return url_for(folder, filename=filename)
    else:
        return f"{assets_bucket}/{filename}"


def get_filename_last_update(file_name):
    return '?u=' + str(os.path.getmtime(file_name))


def clear_and_get_flash_message():
    success_message = get_flashed_messages(category_filter=["success"])
    error_message = get_flashed_messages(category_filter=["error"])
    warning_message = get_flashed_messages(category_filter=["warning"])
    if '_flashes' in session:
        session.pop('_flashes', None)
    return {
        'success': success_message,
        'error': error_message,
        'warning': warning_message
    }
