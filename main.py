from website import create_app, create_socket
import time
from flask import request
from flask_login import current_user
from website.models import db

app = create_app()
socket = create_socket(app)
users_on, check = {}, {}


@socket.on('connect')
def connect():
    username = current_user.username
    users_on[request.sid] = username
    if username not in check:
        check[username] = True
    if check[username]:  # or current_user.active == False:
        current_user.active = True
        db.session.commit()
        check[username] = False
        print("Connected at socket id : "+request.sid +
              " User : "+username + " from : " + request.url)


@socket.on('disconnect')
def disconnect():

    del(users_on[request.sid])
    time.sleep(5)
    if current_user.username in [users_on[i] for i in users_on]:
        pass
    else:
        current_user.active = False
        db.session.commit()
        check[current_user.username] = True
        print("Diconnected at socket id : "+request.sid +
              " User : "+current_user.username)


if __name__ == '__main__':
    # app.run(debug=True)
    socket.run(app, debug=True)
