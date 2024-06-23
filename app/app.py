from flask import Flask, render_template, redirect, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdhsdb232busc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

# with app.app_context():
#     db.create_all()

# with app.app_context():
#     password = generate_password_hash('123456')
#     user1 = User(username='Demetre', password=password)
#     db.session.add(user1)
#     db.session.commit()


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/about')
@app.route('/aboutus')
def about_us():
    return render_template('about_us.html')


@app.route('/user')
def user():
    return render_template('user.html')


@app.route('/registration', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)

        if username == '' or password == '':
            flash("Username or password can't be empty!")

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        except Exception as e:
            print(e)
            return "There was an issue adding the user"

    return render_template('registration.html')



@app.route('/login', methods=['POST', 'GET'])
def log_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect('/user')
        else:
            flash("Invalid username or password. Please try again.")
            return render_template('login.html')

    return render_template('login.html')

@app.route('/results')
def results():
    return render_template('Quizz.html')

@app.route('/top_10_drivers')
def top_10_drivers():

    return  render_template('top10.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('logout.html')

@app.route('/formula1_data')
def formula1_data():
    url = "https://api-formula-1.p.rapidapi.com/rankings/races"
    querystring = {"race": "50"}  # You can adjust this to fetch specific races or remove it for all races
    headers = {
        "x-rapidapi-key": "8b768a0b53mshb73968dfa1d4bc2p1e04d3jsn7a2169c91da6",
        "x-rapidapi-host": "api-formula-1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        content = response.json()
        # Extract relevant data here based on your API response structure
        races_data = content['response']  # Assuming the API response contains data for multiple races
        return render_template('formula_api.html', races_data=races_data)
    else:
        return "Error fetching data from the API"


if __name__ == '__main__':
    app.run(debug=True)
