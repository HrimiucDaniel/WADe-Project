from flask import request, jsonify, render_template, url_for
from werkzeug.utils import redirect

from database import DatabaseHandler
from database import app as base_app

app = base_app


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        email = request.form.get('email')

        if username and password and email:

            DatabaseHandler.add_user(username, password, email)

            return redirect(url_for('get_user_by_username', username=username))

        else:
            return jsonify({'error': 'Invalid request. Missing required parameters.'}), 400

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:

            if DatabaseHandler.check_user_credentials(username, password):
                return redirect(url_for('get_user_by_username', username=username))
            else:
                return jsonify({'error': 'Invalid credentials'}), 401
        else:
            return jsonify({'error': 'Invalid request. Missing required parameters.'}), 400

    return render_template('login.html')


@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = DatabaseHandler.get_all_users()
        users_list = []

        for user in users:
            barcode_info = {
                'username': user.username,
                'passowrd': user.password,
                'email': user.email
            }
            users_list.append(barcode_info)

        return jsonify({'users': users_list})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/users/<username>', methods=['GET'])
def get_user_by_username(username):
    try:
        user = DatabaseHandler.get_user_by_name(username)

        if user is None:
            return jsonify({'error': f'User with username {username} not found'}), 404

        return render_template('user_profile.html', username=user.username)

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(port=5002, debug=True)
