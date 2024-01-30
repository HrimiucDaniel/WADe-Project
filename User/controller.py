from flask import request, jsonify, render_template

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

            response = {
                'username': username,
                'email': email
            }

            return jsonify(response)
        else:
            return jsonify({'error': 'Invalid request. Missing required parameters.'}), 400

    return render_template('register.html')


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


if __name__ == '__main__':
    app.run(debug=True)
