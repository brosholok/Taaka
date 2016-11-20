from flask import *
import flask_login, sqlite3

#configurations
app = Flask(__name__)   
app.secret_key = 'sitb2004!'   
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
DATABASE = 'users.db'

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/login_register')
def login_register():
	error = None
	return render_template('login_register.html', error=error)

#db
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def db_add_user(name, email, password):
	cur = get_db().cursor()
	user_info = (name, email, password)
	cur.execute("INSERT INTO users VALUES(?, ?, ?)", user_info)
	get_db().commit()
#register
@app.route("/register", methods=["POST"])
def register():
	db_add_user(request.form.get('name'), request.form.get("remail"), request.form.get("rpw"))
	return redirect(url_for('login'))
#/register

#login
class User(flask_login.UserMixin):
    pass

@app.route('/login', methods = ['POST'])
def login():
	cur = get_db().cursor()
	email = request.form['email']
	passw = request.form.get('password')
	e = cur.execute("SELECT email from users where email = (?)", [email])
	user_e = e.fetchone() 
	if user_e == email:
		password = cur.execute("SELECT password from users where password = (?)", [passw])
		passwcorrect = password.fetchone()
		if passwcorrect == passw:
			user = User()
			user.id = email
			flask_login.login_user(user)          
			return redirect(url_for('protected'))
	
	error = 'Bad login'
	return redirect(url_for('login_register'))

@app.route('/protected')
@flask_login.login_required
def protected():
	return render_template("logged_in.html")

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('home'))
#/login

if __name__ == '__main__':
  app.run(debug=True)
