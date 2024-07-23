from flask import Flask, request, redirect, url_for, session
import requests, os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def load_common_passwords():
    url = 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000.txt'
    response = requests.get(url)
    return set(response.text.splitlines())

common_passwords = load_common_passwords()

# Password verification function
def is_password_valid(password):
    if len(password) < 8:
        return False
    if any(char.isdigit() for char in password) is False:
        return False
    if any(char.isupper() for char in password) is False:
        return False
    if password in common_passwords:
        return False
    return True

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        password = request.form.get('password')
        if is_password_valid(password):
            session['password'] = password
            return redirect(url_for('welcome'))
        else:
            return '''
                <!DOCTYPE html>
                <html>
                <head><title>Home Page</title></head>
                <body>
                    <h1>Login Page</h1>
                    <form method="post">
                        <input type="password" name="password" placeholder="Enter password" required>
                        <button type="submit">Login</button>
                    </form>
                    <p style="color:red;">Password does not meet requirements or is too common.</p>
                </body>
                </html>
            '''
    return '''
        <!DOCTYPE html>
        <html>
        <head><title>Home Page</title></head>
        <body>
            <h1>Login Page</h1>
            <form method="post">
                <input type="password" name="password" placeholder="Enter password" required>
                <button type="submit">Login</button>
            </form>
        </body>
        </html>
    '''

@app.route('/welcome')
def welcome():
    if 'password' not in session:
        return redirect(url_for('home'))
    return f'''
        <!DOCTYPE html>
        <html>
        <head><title>Welcome Page</title></head>
        <body>
            <h1>Welcome</h1>
            <p>Your password is: {session['password']}</p>
            <a href="{url_for('logout')}">Logout</a>
        </body>
        </html>
    '''

@app.route('/logout')
def logout():
    session.pop('password', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
