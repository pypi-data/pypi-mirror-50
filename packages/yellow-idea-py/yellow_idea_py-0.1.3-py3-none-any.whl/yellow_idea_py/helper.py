import os
import uuid
import fnmatch
from datetime import datetime, timedelta
from flask import session, url_for, request, get_flashed_messages

assets_bucket = f"https://s3-{os.environ['SERVICE_REGION']}.amazonaws.com/{os.environ['ASSETS_BUCKET']}"


def get_created_at():
    return (datetime.today() + timedelta(hours=7)).isoformat()


def convert_to_new_data(data):
    # check new data or not
    if 'id' not in data or data['id'] == '0' or data['id'] == 0:
        data['id'] = str(uuid.uuid1())
    d = datetime.get_created_at()
    if 'created_at' not in data:
        data['created_at'] = d
    data['updated_at'] = d
    return data


def get_session_value(a, b):
    if b in a:
        return a[b]
    else:
        return None


def get_real_js_name(path, target):
    file_name = ""
    for file in os.listdir(path):
        if fnmatch.fnmatch(file, '*.js'):
            if target in file:
                file_name = file
                break
    return file_name


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
