import urllib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# LOCAL DB ON MSSMS
params = urllib.parse.quote_plus(
    'Driver={ODBC Driver 18 for SQL Server};'
    'Server=tcp:sharefactory.database.windows.net,1433;'
    'Database=Wade;'
    'Encrypt=yes;TrustServerCertificate=no;'
    'Uid=sharefactory;'
    'Pwd=AsetDatabbase#;'
    'ConnectionTimeout=30;'
)

app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Exhibition(db.Model):
    __tablename__ = 'Exibitions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)


@app.before_first_request
def create_tables():
    db.create_all()


class DatabaseHandler:
    @staticmethod
    def add_user(ursename, password, email):

        new_user = User(username=ursename,password=password,email=email)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def get_all_users():
        try:
            return User.query.all()
        except Exception as e:
            print(f"An error occurred while retrieving barcodes: {str(e)}")
            return None

    @staticmethod
    def get_user_by_name(name):
        try:
            return User.query.filter_by(username=name).first()
        except Exception as e:
            print(f"An error occurred while retrieving barcode by text: {str(e)}")
            return None


if __name__ == "__main__":
    # Execută această secțiune doar când rulezi acest script, nu când îl importi în alt modul
    with app.app_context():
        create_tables()
