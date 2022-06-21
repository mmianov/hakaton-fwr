from flask import Flask, jsonify,request
from flask_restful import Resource, Api, abort, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from scrapers import parse_orange_alerts, parse_nask_alerts
from flask_mail import Mail, Message
import secrets
import json

app = Flask(__name__)
# database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cyberly.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# app config
api = Api(app)
CORS(app)
# mail server
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'miodek099@gmail.com'
app.config['MAIL_PASSWORD'] = 'nYitM7aJKMabccTvCX7Y'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


class AuthorizedUsers(db.Model):
    __tablename__ = 'auth_users'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String, nullable=True)
    token = db.Column(db.String, nullable=True)


class MailSubscribers(db.Model):
    __tablename__ = 'mail_subscribers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'email': self.email
        }

class Alerts(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.String, nullable=False)
    content_images = db.Column(db.String, nullable=True)
    author = db.Column(db.String, nullable=False)
    author_link = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'content_images': self.content_images,
            'author': self.author,
            'author_link': self.author_link,
            'username': self.username,
            'link': self.link,
            'date': self.date,
            'avatar': self.avatar,
        }
#db.create_all()


# checks if an alert already exists in database
def check_if_duplicate_db(value):
    if db.session.query(Alerts.content).filter_by(content=value).first() is not None:
        return True
    return False


# adds JSON like file to database
def add_to_database(alert):
    if not check_if_duplicate_db(alert['content']):
        alert_record = Alerts(content=alert['content'], content_images=alert['content_images'],
                              author=alert['author'], author_link=alert['author_link'], username=alert['username'],
                              link=alert['link'], date=alert['date'], avatar=alert['avatar'])
        db.session.add(alert_record)
        db.session.commit()

        return Alerts.serialize(alert_record)
    return "Alert is already in database!"


def get_orange_alerts_data():
    print(time.strftime("Fetching Orange and CERT data: %A, %d. %B %Y %I:%M:%S %p"))
    orange_alerts = parse_orange_alerts(60)
    # for alert in orange_alerts:
    #     add_to_database(alert)
    # nask_alerts = parse_nask_alerts(80)
    # for alert in nask_alerts:
    #     add_to_database(alert)


def send_newsletter():
    msg = Message('Hello', sender='miodek099@gmail.com', recipients=['mateuszmianovany@gmail.com'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return "Sent"


def insert_new_user(username):
    if db.session.query(AuthorizedUsers.author).filter_by(author=username).first() is not None:
        return 'User already exists!'
    generated_token = secrets.token_hex(32)
    new_user = AuthorizedUsers(author=username, token=generated_token)
    db.session.add(new_user)
    db.session.commit()
    return f'{username} added to authorized users and can now access API endpoints with token: {generated_token}'


def check_token(author, token):
    if db.session.query(AuthorizedUsers.token).filter_by(author=author).first()[0] == token:
        return True
    return False


def add_to_subs_db(email):
    if db.session.query(MailSubscribers.email).filter_by(email=email).first() is not None:
        return 'Email already in database'
    else:
        new_sub = MailSubscribers(email=email)
        db.session.add(new_sub)
        db.session.commit()
        return MailSubscribers.serialize(new_sub), 201



parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('token', type=str, required=True, help="token is required!")
parser.add_argument('content', type=str, required=True, help="content is required!")
parser.add_argument('content_images', type=str, required=False)
parser.add_argument('author', type=str, required=True, help="author is required!")
parser.add_argument('author_link', type=str, required=True, help="author link is required!")
parser.add_argument('username', type=str, required=True, help="username source is required!")
parser.add_argument('link', type=str, required=True, help="link is required!")
parser.add_argument('date', type=str, required=True, help="date is required!")
parser.add_argument('avatar', type=str, required=False)




class AlertsList(Resource):
    def get(self):
        records = Alerts.query.all()
        return [Alerts.serialize(record) for record in records]

    def post(self):
        args = parser.parse_args()
        if check_token(args['author'], args['token']):
            new_alert = add_to_database(args)
            return new_alert, 201
        else:
            return 'Not authorized', 401


mailParser = reqparse.RequestParser(bundle_errors=True)
mailParser.add_argument('token', type=str, required=True, help="token is required!")
mailParser.add_argument('author', type=str, required=True, help="author is required!")
mailParser.add_argument('email', type=str, required=True, help="email is required!")


class MailingList(Resource):
    def post(self):
        args = mailParser.parse_args()
        if check_token(args['author'], args['token']):
            new_sub = add_to_subs_db(args['email'])
            return new_sub, 201
        else:
            return 'Not authorized', 401


api.add_resource(AlertsList, '/alerts')
api.add_resource(MailingList, '/subscribe')
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=get_orange_alerts_data, trigger="interval", seconds=15)
    scheduler.start()
    #insert_new_user('front-app')
    app.run(debug=True, host='0.0.0.0', port=5000)



