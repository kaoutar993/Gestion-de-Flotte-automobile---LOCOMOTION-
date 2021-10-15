from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_user import UserManager
from flask_socketio import SocketIO, emit
from flask_session import Session
import pymysql


db = SQLAlchemy()
DB_NAME = "locodb"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '180348f5b22db17be014d5c1cb8151c858267cb44819e5460a7ae2528b91680e'
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/locodb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    socket = SocketIO(app)
    db.init_app(app)

    from .views import views
    from .auth import auth
    #Erros :
    @app.errorhandler(401)
    def page_not_found(e):
        return render_template('errors/401.html'), 401
    @app.errorhandler(403)
    def page_not_found(e):
        return render_template('errors/403.html'), 403
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    #######
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    
    from .models import UserRoles,Adminrequests, Assurance ,Conduire,Emploies,InterUser,Options,Permissions,Reparation,Vehicules,Vehicules_SM,Vehicules_affected,controle
    app.config['USER_ENABLE_EMAIL'] = False
    user_manager = UserManager(app,db,InterUser)
    create_database(app)
    

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return InterUser.query.get(int(id))

    return app

def create_socket(app):
    app.config['SESSION_TYPE']='filesystem' 
    Session(app)
    socket = SocketIO(app,manage_session=False,async_handlers=True)
    return socket

def create_database(app):
    db.create_all(app=app)
    print('Created Database!')

"""def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')"""