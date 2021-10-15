from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session, abort
from flask_login import login_user, login_required, logout_user, current_user
from . extentions import Roles
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . models import InterUser, Adminrequests, Emploies, UserRoles, Permissions
from . import db
import json

from flask_user import roles_required

button = 0


auth = Blueprint('auth', __name__)


@auth.before_request
def before_request():
    if "/admin_update/" in request.url:
        if not session['confirm']:
            session["previous"] = request.url
            return redirect('/confirm')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # return str(InterUser.query.get(1).perm[0].perm)
    tmp = request.args.get('next')
    if tmp:
        session['next'] = tmp
    else:
        try:
            tmp = session['next']
            session['next'] = ""
        except Exception:
            session['next'] = ""

    if current_user.is_authenticated:
        return redirect('/')
    else:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            user = InterUser.query.filter_by(username=username).first()
            if user:
                if check_password_hash(user.password, password):
                    login_user(user, remember=True)
                    user.active = True
                    db.session.commit()
                    if tmp == "/logout":
                        return redirect('/')
                    return redirect(tmp or '/')
                else:
                    return "Password Incorrect"
            else:
                return "User Not Found"
        return render_template("index.html")



@auth.route('/signup', methods=['POST'])
def sign():
    username = first_name = request.form.get('username')
    cin = request.form.get('cin')
    password1 = request.form.get('password')
    password2 = request.form.get('password2')
    poste = Emploies.query.filter_by(cin=cin).first()
    #print(poste.poste)
    if poste:
        poste = poste.poste
        role = Permissions.query.filter_by(poste=poste).first()
        if role:
            #check username #
            user = InterUser.query.filter_by(username=username).first()
            emp = Emploies.query.filter_by(cin=str(cin)).first()
            if emp:
                if user:
                    return "user found"
                else:
                    # check if username is not in data already
                    if password1 == password2:
                        new_user = Adminrequests(
                            username=username,
                            emp_id=emp.id,
                            submited_at=datetime.now(),
                            password=generate_password_hash(password1),
                        )
                        db.session.add(new_user)
                        db.session.commit()
                        return redirect(url_for('views.home'))
                    else:
                        return "write the same password"
            else:
                return "Employee not found"
        else:
            abort(403)
    else:
        return "CIN NOT FOUND"


@auth.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    return render_template("login/register_user.html")

@auth.route('/onhold',methods = ['GET','POST'])
@login_required

def onhold():

    Ausers = Adminrequests.query.all()
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    if users :
        #get(id)
        dtA={i:Emploies.query.get(i.emp_id) for i in Ausers }
        return render_template("usage/onhold.html",n=n,dtA =dtA,user=current_user,dt=dt)
    else :
        return render_template("usage/done.html",n=n,user=current_user,dt=dt)
  


@auth.route('/op_approve/<username>', methods=['GET', 'POST'])
@login_required
def op_up(username):
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    user = Adminrequests.query.filter_by(username=username).first()
    new_user = InterUser(
        username=user.username,
        emp_id=user.emp_id,
        confirmed_at=datetime.now(),
        password=user.password,
        active=False
    )
    db.session.add(new_user)
    poste = Emploies.query.get(new_user.emp_id).poste
    perm = UserRoles(
        user_id=new_user.id,
        role_id=Permissions.query.filter_by(poste=poste).first().id
    )
    user = Adminrequests.query.filter_by(username=username).first()

    db.session.add(perm)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('auth.onhold'))


@auth.route('/op_delete/<username>', methods=['GET', 'POST'])
@login_required
def op_del(username):
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    user = Adminrequests.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('auth.onhold'))

#####################################################################################


@auth.route('/users')
@login_required
def users():
    #print(session["current_user"].poste)
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    session['confirm'] = False
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    if users :
        return render_template("usage/users.html",n=n,dt = dt,user=current_user)
    else :
        return render_template("usage/users.html",n=n,user=current_user)
    

########################### AdMIN uPDATES 
@auth.route('/update_admin',methods = ['GET','POST'])
@login_required
def update_admin():
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    if request.method=='POST':
        user=InterUser.query.filter_by(username=request.form.get('username')).first()
        
        perm=request.form.get('perm')
        user.perm=perm
        db.session.commit()
    return redirect(url_for('auth.users'))

@auth.route('/admin_update/<id>' ,methods = ['GET','POST'])
@login_required
def ad_up(id):
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    if request.method=="POST":

        perms = request.form.get('Permission').split(',')
        if perms!=[""]:
            old_perms = UserRoles.query.filter_by(user_id=id)
            for i in old_perms:
                db.session.delete(i)
            for perm in perms :
                new_perm = UserRoles(
                    user_id = int(id),
                    role_id = Permissions.query.filter_by(perm=perm).first().id
                )
                db.session.add(new_perm)
            db.session.commit()
            return redirect('/users')
        else :
            return redirect('/users')
    users = InterUser.query.get(id)
    dt={'current_user':Emploies.query.get(users.emp_id) }
    return render_template('usage/update_admin.html',n=n,dt=dt,user=users)


@auth.route('/admin_delete/<id>',methods = ['GET','POST'])
@login_required
def ad_del(id):
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    user = InterUser.query.get(id)
    role = UserRoles.query.filter_by(user_id=id).first()
    db.session.delete(role)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('auth.users'))

######################################## Update User Profile
@auth.route('/profile',methods = ['GET','POST'])
@login_required
def profile():
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    users = InterUser.query.all()
    dt = {i: Emploies.query.filter_by(id=i.emp_id).first() for i in users}
    dtb = {"current_user": Emploies.query.get(current_user.emp_id)}
    return render_template("usage/profile.html", n=n,dtb=dtb, user=current_user, dt=dt)  

@auth.route('/edit_profile/<parm>',methods = ['GET','POST'])
def edit_p(parm):
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    if parm == 'password':
        if request.method == "POST":
            old_pass = request.form.get('password0')
            if check_password_hash(current_user.password, old_pass):
                password1 = request.form.get('password')
                current_user.password = password=generate_password_hash(password1)
                db.session.commit()
                return redirect(url_for('auth.users'))
            else :
                return "Pass Incorrect"
        return render_template('usage/update_user.html',parm="password",n=n,dt=dt,user=current_user)
    elif parm=='username' :
        if request.method == "POST":
            username= request.form.get('username')
            current_user.username = username
            db.session.commit()
            return redirect(url_for('auth.users'))
        return render_template('usage/update_user.html',n=n,dt=dt,user=current_user,username_=True,parm="username")
    else :
        abort(404)
########################################

@auth.route('/confirm',methods = ['GET','POST'])
@login_required
def confirm():
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    if session["previous"]:
        if request.method =="POST":
            password = request.form.get('password')
            if check_password_hash(current_user.password, password):
                tmp = session["previous"]
                session["previous"] = ""
                session['confirm'] = True
                return redirect(tmp)

        return render_template("confirm/confirm.html",dt=dt,n=n,user=current_user)
    else :
        abort(403)

@auth.route('/log',methods = ['GET','POST'])
@login_required
def log():
    if Roles(current_user,["ROOT","ADMIN"]):
        return "LOG"
    else : return abort(403)

@auth.route('/logout')
@login_required
def logout():
    current_user.active = False
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.login'))
