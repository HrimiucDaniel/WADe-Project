import urllib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

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
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    current_seats = db.Column(db.Integer, nullable=False)
    plant_name = db.Column(db.String(100), nullable=False)


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)


@app.before_first_request
def create_tables():
    db.create_all()


class DatabaseHandler:
    @staticmethod
    def add_user(username, password, email):
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            return 0
        else:
            hashed_password = generate_password_hash(password, method='sha256')
            print("Parola înregistrare")
            print(password)
            print(hashed_password)
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            return 1

    @staticmethod
    def get_all_users():
        try:
            return User.query.all()
        except Exception as e:
            print(f"An error occurred while retrieving users: {str(e)}")
            return None

    @staticmethod
    def get_user_by_name(name):
        try:
            return User.query.filter_by(username=name).first()
        except Exception as e:
            print(f"An error occurred while retrieving user by name: {str(e)}")
            return None

    @staticmethod
    def add_exhibition(name, description, start_date, end_date, total_seats, plant_name):
        new_exhibition = Exhibition(name=name, description=description, start_date=start_date, end_date=end_date,
                                    total_seats=total_seats, plant_name=plant_name)
        new_exhibition.current_seats = 0
        db.session.add(new_exhibition)
        db.session.commit()

    @staticmethod
    def get_all_exhibitions():
        try:
            return Exhibition.query.all()
        except Exception as e:
            print(f"An error occurred while retrieving exhibitions: {str(e)}")
            return None

    @staticmethod
    def get_exhibition_by_name(name):
        try:
            return Exhibition.query.filter_by(name=name).first()
        except Exception as e:
            print(f"An error occurred while retrieving barcode by text: {str(e)}")
            return None

    @staticmethod
    def book_exhibition(username, exhibition_name):
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                exhibition = Exhibition.query.filter_by(name=exhibition_name).first()
                if exhibition and exhibition.current_seats < exhibition.total_seats:
                    exhibition.current_seats += 1
                    db.session.commit()
                    return True
                else:
                    print("Exhibition not found or no available seats.")
                    return False
            else:
                print("User not found.")
                return False
        except Exception as e:
            print(f"An error occurred while booking exhibition: {str(e)}")
            return False

    @staticmethod
    def check_user_credentials(username, password):
        try:
            user = User.query.filter_by(username=username).first()
            return check_password_hash(user.password, password)
        except Exception as e:
            print(f"An error occurred while retrieving barcode by text: {str(e)}")
            return None


if __name__ == "__main__":
    # Execută această secțiune doar când rulezi acest script, nu când îl importi în alt modul
    with app.app_context():
        create_tables()
