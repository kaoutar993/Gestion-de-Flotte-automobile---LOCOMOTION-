from . import db
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey,CheckConstraint
from flask_user import UserMixin as Ux

#sql_db = 'sqlite:///DB.db'

class Emploies(db.Model):
    __tablename__ = "Emploies"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80),  nullable=False)
    lastname = db.Column(db.String(80),  nullable=False)
    cin = db.Column(db.String(80), unique=True, nullable=False)
    tel = db.Column(db.String(80), unique=True, nullable=False)
    adresse = db.Column(db.String(200),ForeignKey('Distance.adresse'))
    email = db.Column(db.String(120), unique=True, nullable=False)
    poste = db.Column(db.String(80),  nullable=False) 
    gender = db.Column(db.String(1),nullable = False)

class Vehicules(db.Model): 
    __tablename__ = "Vehicules"
    id = db.Column(db.Integer, primary_key=True)
    marque = db.Column(db.String(80),  nullable=False)
    nom = db.Column(db.String(80),  nullable=False)
    matricule = db.Column(db.String(80), unique=True, nullable=False)
    carburant = db.Column(db.String(80),  nullable=False)
    km_parcouru = db.Column(db.Float,  nullable=False)
    En_reparation= db.Column(db.Boolean())
    nom_assu = db.Column(db.String(80),  nullable=False)
    etat_assu=db.Column(db.Boolean())
    date_enreg=db.Column(db.Date()) #+
 
class Vehicules_SM(db.Model): 
    __tablename__ = "Vehicules_SM"
    id_veh = db.Column(db.Integer, ForeignKey('Vehicules.id'), primary_key=True)
    capacite=db.Column(db.Float)

class Assurance(db.Model): 
    __tablename__ = "Assurance"
    id = db.Column(db.Integer, primary_key=True)
    id_veh = db.Column(db.Integer, ForeignKey('Vehicules.id')) #matricule au lieu de id f affichage
    montant = db.Column(db.Float,  nullable=False)
    date_payement= db.Column(db.Date())

class Reparation(db.Model): 
    __tablename__ = "Reparation"
    id = db.Column(db.Integer, primary_key=True)
    id_veh = db.Column(db.Integer, ForeignKey('Vehicules.id')) #matricule au lieu de id f affichage
    place=db.Column(db.String(80))
    montant = db.Column(db.Float, nullable=False)
    date_debut= db.Column(db.Date())
    date_fin= db.Column(db.Date())

class Distance(db.Model): 
    __tablename__ = "Distance"
    adresse = db.Column(db.String(200), primary_key=True)
    distance = db.Column(db.Float, nullable=False)
'''modifier id_emp par l'adress !!!!!!!!!'''

class Conduire(db.Model):
    __tablename__="Conduire"
    chauffeur_id=db.Column(db.Integer, ForeignKey('Emploies.id'), primary_key=True)
    veh_id=db.Column(db.Integer,ForeignKey('Vehicules_SM.id_veh'),primary_key=True)
    date=db.Column(db.Date())
    destination=db.Column(db.String(80))
    


class Vehicules_affected(db.Model):
    __tablename__ = "Vehicules_affected"
    employee_id = db.Column(db.Integer, ForeignKey('Emploies.id'), primary_key=True)
    vehicule_id = db.Column(db.Integer, ForeignKey('Vehicules.id'), primary_key=True)
    date_affect = db.Column(db.Date,  nullable=False)
    date_remise = db.Column(db.Date,nullable=True)

""" !!!!!!!! ajouter attribut d'Assurance modifier table d'assu (supp attribut nom d'assu , ajouut id) !!!!!!! """

class controle(db.Model):  #controle employe
    __tablename__ = "controle"
    employee_id = db.Column(db.Integer, ForeignKey('Emploies.id'), primary_key=True)
    id_veh = db.Column(db.Integer, ForeignKey('Vehicules.id'), primary_key=True)
    date_controle= db.Column(db.Date, nullable=False)
    km_parcouru = db.Column(db.Float,  nullable=False)
    gaz_consomme = db.Column(db.Float,  nullable=False)  
    
    
# /'
# chager id emp et veh par CIN et matricule  (dans l'affichage)
# \,

class ControleChauf(db.Model):
    __tablename__ = "controleChauf"
    chauf_id = db.Column(db.Integer, ForeignKey('Conduire.chauffeur_id'), primary_key=True)
    id_veh = db.Column(db.Integer, ForeignKey('Conduire.veh_id'), primary_key=True) 
    destination= db.Column(db.String(100), nullable=False)
    date_dest= db.Column(db.Date, nullable=False)
    km_parcouru = db.Column(db.Float,  nullable=False)
    gaz_consomme = db.Column(db.Float,  nullable=False)

#!!! ForeignKey from Conduire !!!!!

class InterUser(db.Model, UserMixin):
    __tablename__ = "InterUser"
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, ForeignKey('Emploies.id'))
    username = db.Column(db.String(150),unique=True, nullable=False)
    password = db.Column(db.String(200), unique=True, nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.Date())
    perm = db.relationship('Permissions', secondary='user_roles')
    

# Define the Role data-model
class Permissions(db.Model):
    __tablename__ = "Permissions"
    id = db.Column(db.Integer, primary_key=True)
    poste = db.Column(db.String(150), nullable=False)
    perm = db.Column(db.String(150), nullable=False)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('InterUser.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('Permissions.id', ondelete='CASCADE'))

class Adminrequests(db.Model):
    __tablename__ = "Admin_requests"
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, ForeignKey('Emploies.id'))
    username = db.Column(db.String(150),unique=True, nullable=False)
    password = db.Column(db.String(200), unique=True, nullable=False)
    submited_at = db.Column(db.Date())

class Options(db.Model):
    __tablename__ = "Options"
    id = db.Column(db.Integer, primary_key=True)
    option = db.Column(db.String(150),unique=True, nullable=False)
    perm = db.Column(db.String(150), nullable=False)
    
"""class Log(db.Model) :
    __tablename__ ="Log"
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(150),unique=True, nullable=False)   
    log = db.Column(db.String(150),unique=True, nullable=False)"""


