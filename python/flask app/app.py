from flask import Flask, redirect, url_for, request, render_template, jsonify, flash, session
import pandas as pd
from pandas import json_normalize
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false')
db = client['gyan']
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
class Signin (FlaskForm):
    email = email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Sing In')
class SignUp (FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sing Up')
class Search(FlaskForm):
    search_query = StringField('Search',validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('find')
app = Flask(__name__)
app.config['SECRET_KEY']='FE9987C12AB63C56C2762373ABE7D'
    
from flask import render_template, flash, redirect, request

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = SignUp()
    if request.method == "POST": 
        print('Login requested for user {}'.format(form.username.data))
        user = {}
        user['name'] = (form.name.data)
        user['email'] = (form.email.data)
        user['username'] = (form.username.data)
        user['password'] = (form.password.data)
        db.users.insert_one(user) 
        return redirect('/login')
    flash("you are successfully registered now login")
    return render_template('signup.html',title='Signup',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    form = Signin()
    if request.method == "POST":
    
        if '@' in form.email.data:
            filter={
                'email': form.email.data
            }
        else:
            filter={
                'username': form.email.data
            }
        result = db['users'].find(
        filter=filter
        )
        if form.email.data is None:
            flash("No user","danger")
            return render_template("signin.html")
        else:
            if result[0]['password'] == form.password.data:
                 session["log"] = True
                 flash("You are now loggedin","sucess")
                 return redirect('/index')
            else:
                flash("wrong password",'danger')
    
    return render_template('signin.html',title='Signin',form=form)


@app.route('/index', methods=['GET', 'POST'])
def index():
    filter={
 
    }

    result = db['urls'].find(
        filter=filter 
    )
    import copy
    result2 = copy.copy(result)
    form = Search()
    if request.method == "POST": 
        q = form.search_query.data
        return redirect('/home?search='+q)
        
    
    return render_template('home.html', title='Home',form=form, urls=result,  key='topic', info=result2)



@app.route('/home')
def get_source():
    topic = request.args.get('topic')
    page = request.args.get('page')
    search = request.args.get('search')
    if not page :
        page=0
    if topic:
        query = topic
        key = 'topic'
        filter={
            'topic':topic
        }
    
    
    if search :
        query = search
        key='search'
        filter={
       
        'name': {
            '$regex': search
        }
   

        }
    result = db['courses'].find(
        filter=filter 
    ).skip(int(page)*10).limit(10)
    
    result2 = db['urls'].find(
        
    )
    
    result3 = db['university'].find(
         
    )
    
    print('----------------------')
    print(request.args.get('page'))
   
    print()
    print('----------------------')
    pages = db['courses'].count_documents(filter=filter)
    return render_template('index.html', title='Home', course=result, pages=pages,  q=query, page=page, key=key, urls=result2, list=result3 )

@app.route("/logout")
def logout():
    session.clear()
    flash("You are now logger out","sucess")
    return redirect('login')

if __name__ == "__main__":
    app.run(debug=True)
