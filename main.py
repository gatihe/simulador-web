from flask import Flask, redirect, url_for, render_template, request, session, flash
import pyrebase
from datetime import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
from new_engine import *
import os
import shutil

config = {
    "apiKey": "AIzaSyDaNLLMVZgXPenWO3JMGjKt9TtIEcfDGkk",
    "authDomain": "simulador-75b51.firebaseapp.com",
    "databaseURL": "https://simulador-75b51.firebaseio.com",
    "projectId": "simulador-75b51",
    "storageBucket": "simulador-75b51.appspot.com",
    "messagingSenderId": "381390670054",
    "appId": "1:381390670054:web:a376551235a8d4f88b9327",
    "measurementId": "G-ZH6T8K1388"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()
storage = firebase.storage()
user_uid = ''

app = Flask(__name__)
a = False
app.secret_key="hello"
app.permanent_session_lifetime = timedelta(minutes=30)
simulation_lock = True

def empty_session():
    if auth.current_user is None:
        session.pop("user",None)
    return

@app.route("/")
def home():
    empty_session()
    global simulation_lock
    return render_template('index.html',array_test = [0,2,4,6], simulation_lock = simulation_lock)

@app.route('/login/', methods=['POST', 'GET'])
def login():
    empty_session()
    global user_uid
    global simulation_lock
    if request.method == "POST":
        session.permanent = True
        user = request.form['email']
        email = request.form['email']
        password = request.form['password']
        try:
            email = auth.sign_in_with_email_and_password(email,password)
            auth.get_account_info(email['idToken'])
            session["user"] = email['idToken']
            user_uid = email['localId']
        except:
            return "Please check your credentials"
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html",simulation_lock = simulation_lock)

@app.route('/user/')
def user():
    empty_session()
    if "user" in session:
        user = session["user"]
        return redirect(url_for("home"))
        #return ('<h1>'+user+'</h1>')
    else:
        return redirect(url_for("login"))



@app.route('/importacoes/', methods=['GET','POST'])
def importacoes():
    empty_session()
    global simulation_lock
    global user_uid
    if "user" in session:
        user = session["user"]
        global simulation_lock
        #return ('<h1>'+user+'</h1>')
        if request.method == 'POST':
            if request.files:
                timestamp = datetime.datetime.now().strftime("%d-%m_%I-%M-%S_%p")
                try:
                    catalogo = request.files['catalogo']
                    catalogo.save('imports/uploads/catalogo.xml')
                    storage.child(user_uid+"/"+timestamp+"_catalogo.xml").put("imports/catalogos/si_cat_2020.xml")
                except UnboundLocalError:
                    pass
                try:
                    configs = request.files['configs']
                    configs.save('imports/uploads/configs.xml')
                    storage.child(user_uid+"/"+timestamp+"_configs.xml").put("imports/configs/default_config.xml")
                    #current_config = storage.child(user_uid+"/configs.xml").download("usr/"+user_uid[-5:]+"/"+timestamp+"current_config.xml")
                    #current_catalogo = storage.child(user_uid+"/configs.xml").download("usr/"+user_uid[-5:]+"/"+user_uid[-5:]+"current_catalogo.xml")
                    simulation_lock = False
                except UnboundLocalError:
                    pass
                return render_template("importacoes.html", catalogo = catalogo, configs = configs, simulation_lock = simulation_lock)
        return render_template("importacoes.html", simulation_lock = simulation_lock)
    else:
        return redirect(url_for("login"))

@app.route("/simulacao/")
def simulacao():
    empty_session()
    if "user" in session:
        user = session["user"]
        global simulation_lock
        simulation, simulation_array, tempo_max_integralizacao, qtde_de_disciplinas_semestre_impar, qtde_de_disciplinas_semestre_par, subss, students_data, prereqs_report_export, std_records, std_info_export = new_simulation()
        return render_template('simulacao.html', simulation_table=[simulation.to_html(classes='table table-striped table-sm', header="false",justify="left", border="0", index=False)], prereqs_table=[prereqs_report_export.to_html(classes='table table-striped table-sm', header="false",justify="left", border="0", index=False)],std_records_table=[std_records.to_html(classes='table table-striped table-sm', header="false",justify="left", border="0", index=False)],std_info_table=[std_info_export.to_html(classes='table table-striped table-sm', header="false",justify="left", border="0", index=False)],params = subjects, simulation_lock = simulation_lock)
    else:
        return redirect(url_for("login"))

@app.route("/logout/")
def logout():
    empty_session()
    global simulation_lock
    auth.current_user = None
    if "user" in session:
        user = session["user"]
        flash("you have been logged out", "info")
    session.pop("user",None)
    #shutil.rmtree("usr/"+user_uid[-5:])
    simulation_lock = True
    return redirect(url_for("login"))
# @app.route("/admin/")
# def admin():
#     if a:
#         return 'adm'
#     return redirect(url_for("user", name ="Admin!!!"))
#
# @app.route('/<name>/')
# def user(name):
#     return ('Hello '+name)

if __name__ == '__main__':
    app.run(debug=True)



#functions being called
