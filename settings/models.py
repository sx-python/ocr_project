from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
    name = db.Column('user_name', db.String, doc='用户名')


class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True, doc='图片id')
    id_num = db.Column('user_id', db.Integer, doc='用户ID')
    profile_image = db.Column(db.String, doc='图片')
    result = db.Column(db.String, doc='图片内容')
