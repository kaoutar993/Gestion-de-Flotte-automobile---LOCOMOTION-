from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from flask.globals import session
from flask_login import login_user, login_required, logout_user, current_user
from . models import ControleChauf, Emploies, Vehicules, Reparation ,Assurance, InterUser, Vehicules_SM, Vehicules_affected, Adminrequests
from . import db
from . import auth
from datetime import datetime



views = Blueprint('views', __name__)


@views.route('/',methods = ['GET','POST'])
@login_required
def home():
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    return render_template("Accueil.html",n=n,dt = dt,user=current_user)
    
    

@views.route('/emps',methods = ['GET','POST'])
@login_required
def afficher_emps():
    emps = Emploies.query.all()
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    return render_template("gestionBd/emps.html",n=n,emps=emps,user=current_user,dt=dt)


@views.route('/vehs',methods = ['GET','POST'])
@login_required
def afficher_vehs():
    vehs = Vehicules.query.all()
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    return render_template("gestionBd/vehs.html",n=n,vehs=vehs,user=current_user,dt=dt)


@views.route('/affecter_veh/<id>',methods = ['GET','POST'])
@login_required
def affect(id):
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    vehs = Vehicules.query.all()
    mat = request.form.get('matricule')
    repar= Reparation.query.all()
    veha=Vehicules_affected.query.all()
    vehm=Vehicules_SM.query.all()
    emp=Emploies.query.filter_by(id=id).first()
    print([i.id_veh for i in vehm])
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    return render_template("gestionBd/affecter_veh.html",n=n,vehs=vehs,veha=[i.vehicule_id for i in veha],vehm=[i.id_veh for i in vehm],repar=[i.id_veh for i in repar],emp=emp,user=current_user,dt=dt)

@views.route('/supp_aff/<ide>',methods = ['GET','POST'])
@login_required
def supp_aff(ide):
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    emp=Emploies.query.filter_by(id=ide).first()
    empa = Vehicules_affected.query.filter_by(employee_id=ide).first()
    if empa:
        db.session.delete(empa)
        db.session.commit()
        return render_template("gestionBd/aff_emp.html",n=n,empa=empa,emp=emp,dt=dt,user=current_user)
    else:
        return render_template("gestionBd/aff_emp.html",n=n,emp=emp,dt=dt,user=current_user)



@views.route('/affectation/<ide>/<idv>',methods = ['GET','POST'])
@login_required
def affecter(ide,idv):
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    #empa=Emploies.query.filter_by(id=ide).first()
    vehaa=Vehicules.query.filter_by(id=idv).first()
    empa=Vehicules_affected.query.filter_by(employee_id=ide).first()
    emp = Emploies.query.get(ide)
    if not empa:
        new_veha = Vehicules_affected(
                    employee_id=int(ide),
                    vehicule_id=int(idv),
                    date_affect=datetime.now()
        )  
        db.session.add(new_veha)
        db.session.commit()
        return render_template("gestionBd/aff_emp.html",n=n,vehaa=vehaa,empa=empa,emp=emp,user=current_user,dt=dt)
    else:
        return render_template("gestionBd/aff_emp.html",n=n,empa=empa,vehaa=vehaa,emp=emp,dt=dt,user=current_user)


@views.route('/assu',methods = ['GET','POST'])
@login_required
def assu():
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    assur = Assurance.query.all()
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    vh={i:Vehicules.query.filter_by(id=i.id_veh).first() for i in assur}
    return render_template("gestionBd/assu.html",n=n,assur=assur,user=current_user,dt=dt,vh=vh)

@views.route('/repar',methods = ['GET','POST'])
@login_required
def rep():
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    repar= Reparation.query.all()
    dtr={i:Vehicules.query.filter_by(id=i.id_veh).first() for i in repar}
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    return render_template("gestionBd/repar.html",n=n,dtr=dtr, repar=repar,user=current_user,dt=dt)


@views.route('/ajout_veh',methods=['GET','POST'])
@login_required
def ajout_veh():
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    if request.method=='POST':
        new_veh = Vehicules(
                marque= request.form.get('marque'),
                nom= request.form.get('nom'),
                matricule=request.form.get('matricule'),
                carburant=request.form.get('carburant'),
                km_parcouru=request.form.get('km_parcouru'),
                En_reparation=bool(request.form.get('En_reparation')),
                nom_assu=request.form.get('assu'),
                etat_assu=bool(request.form.get('etat_assu')),
                date_enreg=datetime.now()
        )
        """new_assu = Assurance(
                vehicule_AS_id=Vehicules.query.get(new_veh.vehicule_AS_id)
                nom= request.form.get('nom_assu')
                montant= request.form.get('montant_assu')
                date_payement = request.form.get('date')
        )"""
        db.session.add(new_veh)
       # db.session.add(new_ass)
        db.session.commit()
        return redirect(url_for('views.afficher_vehs'))
    return render_template("gestionBd/ajout_veh.html",n=n,dt=dt,user=current_user)


@views.route('/ajout_repar/<id>',methods=['GET','POST'])
@login_required
def ajout_repar(id):
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    veh= Vehicules.query.get(id)
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    if request.method=='POST':
        new_rep= Reparation(
                id_veh=id,
                montant= request.form.get('Montant'),
                place= request.form.get('place'),
                date_debut=request.form.get('ddate'),
                date_fin=request.form.get('fdate')
        )
        db.session.add(new_rep)
        db.session.commit()
        return redirect(url_for('views.rep'))
    return render_template("gestionBd/ajout_repar.html",n=n,veh=veh,dt=dt,user=current_user)

@views.route('/ajout_repar',methods=['GET','POST'])
@login_required
def ajout_rep():
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    return render_template("gestionBd/ajout_repar.html",n=n,dt=dt,user=current_user)

@views.route('/aff_veh/<id>',methods = ['GET','POST'])
@login_required
def aff_veh(id):
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    veh= Vehicules.query.get(id)
    assu=Assurance.query.filter_by(id_veh=id).first()
    veha=Vehicules_affected.query.filter_by(vehicule_id=id).first()
    vehm=Vehicules_SM.query.filter_by(id_veh=id).first()
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    if veha:
        empaa=Emploies.query.filter_by(id=veha.employee_id).first()
        return render_template("gestionBd/aff_veh.html",n=n,dt=dt,vehm=vehm,assu=assu,empaa=empaa,veha=veha,user=current_user,veh=veh)
    else:
        return render_template("gestionBd/aff_veh.html",n=n,dt=dt,vehm=vehm,assu=assu,veha=veha,user=current_user,veh=veh)

@views.route('/aff_emp/<id>',methods = ['GET','POST'])
@login_required
def aff_emp(id):
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    emp = Emploies.query.get(id)
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users}
    empa = Vehicules_affected.query.filter_by(employee_id=id).first()
    if empa:
        vehaa=Vehicules.query.filter_by(id=empa.vehicule_id).first()
        return render_template("gestionBd/aff_emp.html",n=n,dt=dt,vehaa=vehaa,emp=emp,empa=empa,user=current_user)
    else:   
        return render_template("gestionBd/aff_emp.html",n=n,vehaa=None,dt=dt,emp=emp,empa=empa,user=current_user)

@views.route('/alert',methods=['GET','POST'])
@login_required
def alert():
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    #assual=Assurance.query.filter_by(date_payement=).first()

    return render_template("#",n=n,user=current_user,dt=dt)


@views.route('/supp_veh/<id>',methods = ['GET','POST'])
@login_required
def supp_veh(id):
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users}
    veh = Vehicules.query.filter_by(id=id).first()
    assu = Assurance.query.filter_by(id_veh=veh.id).first()
    veha= Vehicules_affected.query.filter_by(vehicule_id=veh.id).first()
    repv= Reparation.query.filter_by(id_veh=veh.id).first()
    if repv:
        db.session.delete(repv)
    db.session.commit()
    if veha:
        db.session.delete(veha)
    db.session.commit()
    if assu:    
        db.session.delete(assu)
    db.session.commit()
    db.session.delete(veh)
    db.session.commit()
    return redirect(url_for('views.afficher_vehs'))
    #return render_template("gestionBd/vehs.html",veh=veh,dt=dt,user=current_user)
    


@views.route('/assu/<id_veh>',methods=['GET','POST'])
@login_required
def date_assu(id_veh):
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    #veh = Vehicules.query.get(int(id))
    assur = Assurance.query.all()
    #vh={i:Vehicules.query.get(i.vehicule_AS_id).matricule for i in assur}
    #print('###############################""""' + str(id_veh))
    date = datetime.strptime(request.form.get('date_assu'),'%Y-%m-%d')
    a = Assurance.query.filter_by(id_veh=id_veh).first()
    a.date_payement = date
    db.session.commit()
    return redirect(url_for('views.assu'))

@views.route('/assua/<id_veh>',methods=['GET','POST'])
@login_required
def date_assua(id_veh):
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    veh = Vehicules.query.get(id_veh)
    assu = Assurance.query.filter_by(id_veh=id_veh).first()

    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users}
    date = datetime.strptime(request.form.get('date_assu'),'%Y-%m-%d')
    a = Assurance.query.filter_by(id_veh=id_veh).first()
    a.date_payement = date
    db.session.commit()
    return redirect(url_for('views.aff_veh', id=id_veh)) 

@views.route('/control_chauf',methods = ['GET','POST'])
@login_required
def control_chauf():
    cont=ControleChauf.query.all()
    emps=Emploies.query.all()
    users = InterUser.query.all()
    dt={i:Emploies.query.filter_by(id=i.emp_id).first() for i in users }
    dte={i:Emploies.query.filter_by(id=i.chauf_id).first() for i in cont }
    dm= Adminrequests.query.all()
    dml=[i for i in dm] 
    n= len(dml)
    return render_template("gestionBd/control_chauf.html",n=n,dte=dte,cont=cont,user=current_user,dt=dt)

