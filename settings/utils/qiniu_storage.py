import requests
from qiniu import Auth, put_data
import os

# 需要填写你的 Access Key 和 Secret Key
access_key = 'AtRSc-jXv5Y0v2DsatRzxOAychq9e4uSoGpM7IWD'
secret_key = 'xAEfx9iU16k4R97_7-H7qsJdHHYI5HqqUyZlarOQ'


def upload_image(file_data, cid):
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'sx-orc'
    # 上传后保存的文件名
    key = cid
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 360000)
    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    ret, info = put_data(token, key, file_data)
    print(info)
    return ret['key']


def download_image(key):
    q = Auth(access_key, secret_key)
    # 有两种方式构造base_url的形式
    # base_url = 'http://%s/%s' % ('http://q7bqpxrcr.bkt.clouddn.com/', key)
    # 或者直接输入url的方式下载
    base_url = 'http://q7bqpxrcr.bkt.clouddn.com/' + key
    # 可以设置token过期时间
    private_url = q.private_download_url(base_url, expires=360000)
    # 浏览图片地址
    print(private_url)
    return private_url

