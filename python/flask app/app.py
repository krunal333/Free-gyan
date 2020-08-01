from flask import Flask, redirect, url_for, request, render_template, jsonify, flash
import pandas as pd
from pandas import json_normalize
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false')
db = client['gyan']
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class SignUp (FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sing Up')
app = Flask(__name__)
app.config['SECRET_KEY']='FE9987C12AB63C56C2762373ABE7D'
    
from flask import render_template, flash, redirect, request

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignUp(request.form)
    if request.method == "POST" and form.validate():
            name = form.name.data
            email = form.email.data
            username  = form.username.data
            password = form.password.data
        
            return redirect('/home')
    user = {}
    user['name'] = (form.name.data)
    user['email'] = (form.email.data)
    user['username'] = (form.username.data)
    user['password'] = (form.password.data)
    db.users.insert_one(user) 
    return render_template('signup.html',title='Signup',form=form)

@app.route('/home')
def index():
    filter={}
    result = db['course'].find(
        filter=filter 
    ).limit(5000)

    
    print('----------------------')
    print(type(result))
    print('----------------------')
    return render_template('backup.html', title='Home', course=result)



@app.route('/home/<source>/<topic>/<page>')
def get_source(source,topic,page):
    filter={
        
    'source': str(source),
    
    'name': {
        '$regex': topic
    }


    }
    result = db['course'].find(
        filter=filter 
    ).skip(int(page)*10).limit(10)
    
    
    print('----------------------')
    print(type(result))
   
    print(source)
    print('----------------------')
    pages = db['course'].count_documents(filter=filter)
    return render_template('index.html', title='Home', course=result, pages=pages, source=source, topic=topic, page=page)

if __name__ == "__main__":
    app.run(debug=True)
