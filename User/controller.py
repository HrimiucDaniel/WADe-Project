import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import plant_url
from flask import request, jsonify, render_template, url_for, session
from werkzeug.utils import redirect
import requests
from database import DatabaseHandler, app as base_app
from SPARQLWrapper import SPARQLWrapper, JSON

app = base_app
app.config['SECRET_KEY'] = 'secret_key_here'  # Adaugă o cheie secretă pentru sesiuni


@app.before_first_request
def clear_sessions():
    session.clear()


@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if username and password and email:
            if DatabaseHandler.add_user(username, password, email):
                session['logged_in'] = True
                session['username'] = username
                send_username_to_port_5000(username)
                return redirect(url_for('get_main_page'))
            else:
                error_message = 'Username or email already exist!'

    return render_template('register.html', error_message=error_message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            if DatabaseHandler.check_user_credentials(username, password):
                session['logged_in'] = True
                session['username'] = username
                send_username_to_port_5000(username)
                return redirect(url_for('get_main_page'))
            else:
                error_message = 'Username or password not found!'

    return render_template('login.html', error_message=error_message)


def send_username_to_port_5001(username):
    url = 'http://127.0.0.1:5001/receive-username'
    data = {'username': username}
    print(username)
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print('Username sent successfully to port 5001')
    else:
        print('Failed to send username to port 5001')


def send_username_to_port_5000(username):
    url = 'http://127.0.0.1:5000/receive-username'
    data = {'username': username}
    print(username)
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print('Username sent successfully to port 5000')
    else:
        print('Failed to send username to port 5000')
    send_username_to_port_5001(username)


@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        if not session.get('logged_in'):
            return jsonify({'error': 'Not logged in'}), 401

        users = DatabaseHandler.get_all_users()
        users_list = []

        for user in users:
            user_info = {
                'username': user.username,
                'password': user.password,
                'email': user.email
            }
            users_list.append(user_info)

        return jsonify({'users': users_list})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500





@app.route('/', methods=['GET'])
def get_main_page():
    try:
        if not session.get('logged_in'):
            return render_template('main.html')
        username = session['username']
        # print(username)
        # print(username)
        user = DatabaseHandler.get_user_by_name(username)
        elements = plant_url.get_all_plants()
        urls = {}
        for element in elements:
            urls[element] = plant_url.get_url(element)

        return render_template('user_profile.html', username=user.username, email=user.email, elements=elements, urls=urls)

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('get_main_page'))


@app.route('/exhibitions', methods=['GET'])
def get_all_exhibitions():
    try:
        if not session.get('logged_in'):
            return jsonify({'error': 'Not authorized'}), 403
        exhibitions = DatabaseHandler.get_all_exhibitions()
        exhibitions_list = []
        user = DatabaseHandler.get_user_by_name(session['username'])

        for exhibition in exhibitions:
            exhibition_info = {
                'name': exhibition.name,
                'plant_name': exhibition.plant_name,
                'start_date': exhibition.start_date,
                'end_date': exhibition.end_date,
                'curent_seats': exhibition.current_seats,
                'total_seats': exhibition.total_seats
            }
            exhibitions_list.append(exhibition_info)

        return render_template('exhibitions_list.html', exhibitions=exhibitions, user=user)

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/exhibitions/<name>', methods=['GET'])
def get_exhibition_by_name(name):
    try:
        if not session.get('logged_in'):
            return jsonify({'error': 'Not authorized'}), 403
        exhibition = DatabaseHandler.get_exhibition_by_name(name)
        plant_name = exhibition.plant_name
        url_plant = plant_url.get_plant_name(plant_name)
        user = DatabaseHandler.get_user_by_name(session['username'])
        if exhibition is None:
            return jsonify({'error': f'Exhibition with name {name} not found'}), 404

        return render_template('exhibition.html', exhibition=exhibition, user=user, plant_url=url_plant)

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/reserve/<name>', methods=['GET'])
def reserve_exhibition(name):
    try:
        if not session.get('logged_in'):
            return jsonify({'error': 'Not authorized'}), 403

        exhibition = DatabaseHandler.get_exhibition_by_name(name)

        if exhibition is None:
            return jsonify({'error': f'Exhibition with name {name} not found'}), 404

        if DatabaseHandler.book_exhibition(session['username'], name):
            user = DatabaseHandler.get_user_by_name(session['username'])
            send_confirmation_email(user.username, user.email, exhibition.name, exhibition.start_date)
            return render_template('reservation.html', text="Exhibition successfully booked")
        else:
            return render_template('reservation.html', text="Exhibition not found or no available seats.")
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def send_confirmation_email(user_username, user_email, exhibition_name, start_date):
    try:
        smtp_server = 'smtp.mail.yahoo.com'
        smtp_port = 587
        smtp_username = 'sabin.sabin2048@yahoo.com'
        smtp_password = 'blgjvyccfwiwgflm'

        subject = 'Exhibition Booking Confirmation'
        html_body = f'''
            <html>
            <body>
                <p>Hi <strong>{user_username}</strong>!</p>
                <p>Thank you for booking the exhibition: <strong>{exhibition_name}</strong>. Your reservation has been confirmed.</p>
                <p>You are expected at the exhibition on {start_date}.</p>
                <p>For more details, please visit our website.</p>
            </body>
            </html>
        '''

        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = user_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, user_email, msg.as_string())

    except Exception as e:
        print(f"Error sending confirmation email: {str(e)}")


if __name__ == '__main__':
    app.run(port=5002, debug=True)
