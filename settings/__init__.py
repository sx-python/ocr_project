from datetime import timedelta
from ocr_project import create_app
# 设置允许的文件格式
ALLOWED_EXTENSIONS = ['png', 'jpg', 'JPG', 'PNG']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 设置静态文件过期时间
create_app.send_file_max_age_default = timedelta(seconds=100)
