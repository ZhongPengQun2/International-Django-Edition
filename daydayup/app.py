# coding: utf-8
import logging
from flask import Flask, request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models import db

flask_app = Flask(__name__)
manager = Manager(flask_app)

# flask admin settings
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models.word import Word, Topic
from models.article import Article
from models.phrase import Phrase
flask_app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(flask_app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(Word, db.session, endpoint='word-admin'))
admin.add_view(ModelView(Article, db.session, endpoint='article-admin'))
admin.add_view(ModelView(Phrase, db.session, endpoint='phrase-admin'))
admin.add_view(ModelView(Topic, db.session, endpoint='topic-admin'))

flask_app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@127.0.0.1:6432/jiya"
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_app.config['SECRET_KEY'] = "qwertyuiopasdfghjklzxcvbnm"
flask_app.config['DEBUG'] = True

# db.init_app(flask_app)

# flask_app.logger.setLevel(logging.INFO)  # use the native logger of flask
# handler = logging.handlers.RotatingFileHandler(
#     '../log/app.log',
#     maxBytes=1024 * 1024 * 100,
#     backupCount=20
# )
# flask_app.logger.addHandler(handler)

# 注册初始化blueprint
from controllers.base import bp as base_bp
from controllers.user import bp as user_bp
from controllers.word import bp as word_bp
from controllers.article import bp as article_bp
from apis import bp as apis_bp
flask_app.register_blueprint(base_bp, url_prefix='/')
flask_app.register_blueprint(user_bp, url_prefix='/user')
flask_app.register_blueprint(word_bp, url_prefix='/word')
flask_app.register_blueprint(article_bp, url_prefix='/article')
flask_app.register_blueprint(apis_bp, url_prefix='/api')

db.init_app(flask_app)

migrate = Migrate(flask_app, db)
manager.add_command('db', MigrateCommand)


@flask_app.before_request
def protect_admin(*args, **kwargs):
    # 如果是login,可以通过白名单
    print '--'*80
    print request.path
    print '=='*80
    if request.path == '/admin':
        raise


if __name__ == '__main__':
    # flask_app.run()
    manager.run()

