from flask import Blueprint, request, jsonify
from settings.models import ImageData, User, db
from settings.utils import qiniu_storage
from settings.utils.YDMHTTPDemo3 import ydm_http
from settings import allowed_file
import pytesseract
from PIL import Image
import os


user_bp = Blueprint('user', __name__)

# 上传图片
# 请求路径: /user/upload
# 请求方式: POST
# 请求参数: image, name
# 返回值:2000 content
@user_bp.route('/upload', methods=['POST'])
def patch():
    image = request.files.get('photo')
    if not (image and allowed_file(image.filename)):
        return jsonify(error=1001, msg="请检查上传的图片类型，仅限于png、PNG、jpg、JPG")
    name = request.args.get('name')

    basedir = os.path.abspath(os.path.dirname(__file__))
    print(basedir)
    path = basedir + '/static/images/'
    file_path = path + image.filename
    image.save(file_path)
    # 有图片，识别图片
    try:
        # 图像识别引擎识别
        im = Image.open(file_path)
        result = pytesseract.image_to_string(im)
    except:
        # 云打码平台识别
        result = ydm_http(file_path)
        # 检查识别结果
        print(result)
    # 判断识别是否有字母，字符串方法转换判断
    if str(result).isalpha():
        # 有字母，上传七牛云
        sql_key = qiniu_storage.upload_image(image.read(), image.filename)
        # 将七牛返回的图片名，图片内容存到数据库
        # 先查询是否有用户
        user = User.query.filter(User.name == name).first()
        if not user:
            # 没有就创建
            user = User(name=name)
            db.session.add(user)
            db.session.commit()
        # 两表关联存储
        up_image = ImageData(id_num=User.id,
                         profile_image=sql_key,
                         result=result)
        db.session.add(up_image)
        db.session.commit()
    else:
        os.remove(file_path)
        return jsonify(errno=3000, content='图片不符合要求')
    os.remove(file_path)
    return jsonify(errno=2000, content='图片上传成功')


# 查询数据库返回的图片内容
# 请求路径: /user/look
# 请求方式: GET
# 请求参数: name
# 返回值:2000 content
@user_bp.route('/look', methods=['get'])
def look_data():
    # 将数据库的数据返回
    # 从前端获取用户
    name = request.args.get('name')
    # 查询用户是否存在，存在返回用户id
    user_id = User.query.filter(User.name == name).value(User.id)
    if not user_id:
        return jsonify(errno=4004, content='用户不存在')
    # 根据用户id查询图片库中的值，并返回所有
    content = ImageData.query.filter(user_id == ImageData.id_num).value(ImageData.result).all()
    return jsonify(errno=2000, content=content)


# 下载图片
# 请求路径: /user/download
# 请求方式: GET
# 请求参数: name
# 返回值:2000 content
@user_bp.route('/download', methods=['get'])
def download_data():
    name = request.args.get('name')
    user_id = User.query.filter(User.name == name).value(User.id)
    if not user_id:
        return jsonify(errno=4004, content='用户不存在')
    # 查询数据库中的图片名
    image_name = ImageData.query.filter(user_id == ImageData.id_num).value(ImageData.profile_image).all()
    for key in image_name:
        private_url = qiniu_storage.download_image(key)
        try:
            # 创建放置下载图片的文件夹
            os.mkdir('image')
        except:
            return jsonify(errno=4005, content='文件夹已创建')
        finally:
            with open(os.getcwd() + r'/static/image/' + key, 'w+', encoding='utf8')as f:
                f.write(private_url)
    return jsonify(errno=2000, content='加载完成')
