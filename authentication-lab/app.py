from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

config = {
  "apiKey": "AIzaSyAwkTEOF8EMI6uvr1qklM2YFrZ_6PLUnyI",
  "authDomain": "cool-firebase-go-brrrr.firebaseapp.com",
  "projectId": "cool-firebase-go-brrrr",
  "storageBucket": "cool-firebase-go-brrrr.appspot.com",
  "messagingSenderId": "597778007614",
  "appId": "1:597778007614:web:3ff7d05d2f00eab8d3f36f",
  "measurementId": "G-F4JWXP9V10",
  "databaseURL":"https://cool-firebase-go-brrrr-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
@app.route('/', methods=['GET', 'POST'])
def signin():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
   return render_template("signin.html")

@app.route('/signup',  methods=['GET', 'POST'])
def signup():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"fname": "asil","password":"asil123","lname": "gazmawi" ,"email": "asillimar@gmail.com","bio":"loves"}
            db.child("Users").child(login_session['user']
                ['localId']).set(user)
            return redirect('add_tweet')
       except:
           error = "Authentication failed"
   return render_template("signup.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect('/')



@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)