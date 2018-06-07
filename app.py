from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:behappy@localhost/testlogging'
db = SQLAlchemy(app)


class User(db.Model):
	__tablename__='user_test'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(120), nullable=False)
	def __repr__(self):
		return '<User %r>' % self.username

@app.route('/',methods=['GET', 'POST'])
def index():
	exc = ''
	if request.method=="POST":
		username = request.values.get('username')
		password = request.values.get('password')
		userobj = User(username=username, password=password)
		try:
			db.session.add(userobj)
			db.session.commit()
		except Exception, e:
			exc = str(e)
	users = User.query.all()
	return render_template('index.html', exc=exc, users=users)

if __name__ == '__main__':
    app.run(debug=True)