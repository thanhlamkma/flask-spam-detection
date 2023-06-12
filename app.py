from flask import Flask, render_template, request, redirect, url_for, jsonify, session,send_from_directory
from flask_paginate import Pagination, get_page_args, get_page_parameter
import json
from connect_mongo import get_emaildb
from datetime import datetime, timedelta
from mlsetting import getcurrent,setcurrent


app = Flask(__name__, template_folder="templates", static_url_path="/static")
app.secret_key = 'my_secret'

# Set session timeout to 10 minutes (600 seconds)
# Define the session timeout duration (10 minutes)
SESSION_TIMEOUT = timedelta(minutes=10)

# Route for serving favicon.ico
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, './icons/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/static/<path:filename>')
def serve_public_static(filename):
    return send_from_directory('static', filename)


# Decorator to check login status before each request
@app.before_request
def check_login():
    # Define a list of routes that do not require login
    exempt_routes = ['login']  # Add any routes that don't require login
    
    if request.endpoint and not request.endpoint.startswith('static') and not 'icons/favicon.ico':
	    if request.endpoint not in  exempt_routes and 'logged_in' not in session:
		    return redirect(url_for('login'))


def check_session_timeout():
    if 'last_activity' in session:
        last_activity_time = session['last_activity']
        current_time = datetime.now()

        # Check if the session has expired
        if (current_time - last_activity_time) > SESSION_TIMEOUT:
            session.pop('logged_in', None)  # Clear any logged_in session data
            session.pop('last_activity', None)  # Clear the last_activity session data
            return redirect(url_for('login'))

    # Update the last_activity time in the session
    session['last_activity'] = datetime.now()


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Tên đăng nhập hoặc mật khẩu không chính xác.'
		else:
			session['logged_in'] = True
			session.permanent = True

			return redirect(url_for('intro'))
	return render_template('login.html', error=error)


@app.route('/logout')
def logout():
	session.pop('logged_in', None)  # Clear the 'logged_in' key from the session
	return redirect(url_for('login'))


@app.route("/")
def intro():
	if 'logged_in' in session:
		return render_template("intro.html")
	else:
		return redirect(url_for('login'))
   

@app.route("/dashboard")
def dashboard():
	if 'logged_in' in session:
		emails = get_emaildb()

		COUNT_SPAM = 0
		COUNT_HAM = 0

		for email in emails:
			if email["predict"] == 1:
				COUNT_SPAM = COUNT_SPAM + 1
			else:
				COUNT_HAM = COUNT_HAM + 1

		spam_percent = round(COUNT_SPAM / len(emails) * 100, 2)

		return render_template("dashboard.html", total_emails=len(emails), total_spam=COUNT_SPAM, total_ham=COUNT_HAM, 
			 spam_percent=spam_percent)
	else:
		return redirect(url_for('login'))


def get_pagination_emails(offset=0, emails_per_page=10):
	emails = get_emaildb()
	emails.reverse()
	return emails[offset: offset + emails_per_page]


@app.route('/data', methods=['GET'])
def get_emal():
	if 'logged_in' in session:       
		data = get_emaildb()
		return jsonify(data)
	else:
		return redirect(url_for('login'))


@app.route("/apply")
def show_emails(): 
	if 'logged_in' in session:       
		# Pagination
		emails = get_emaildb()
		page, emails_per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")

		total_emails = len(emails)

		pagination_emails = get_pagination_emails(offset=offset, emails_per_page=emails_per_page)

		pagination = Pagination(page=page, per_page=emails_per_page, total=total_emails, css_framework="bootstrap4",
			   alignment="center")

		# Count email
		COUNT_SPAM = 0
		COUNT_HAM = 0
		
		for email in emails:
			if email["predict"] == 1:
				COUNT_SPAM = COUNT_SPAM + 1
			else:
				COUNT_HAM = COUNT_HAM + 1

		# Render the template and pass the messages to the template
		return render_template("apply.html", emails=pagination_emails, total_emails=total_emails, total_spam=COUNT_SPAM, 
			 total_ham=COUNT_HAM, page=page, emails_per_page=emails_per_page, pagination=pagination)
	else:
		return redirect(url_for('login'))


@app.route("/setting", methods=["GET", "POST"])
async def setting():
	if 'logged_in' in session:   
		if request.method == "GET":
			method='get'
			message=""
			success=0	       
			setting_value = await getcurrent()

			if setting_value is not None: 
				success=1
				message = setting_value
			else:      
				message = "Bị lỗi khi lấy thông tin cài đặt!"
				success=0
						
			return render_template("setting.html",method=method ,success=success, message=message)
		
		if request.method == "POST":
			method='post'     
			algorithm_type = request.form["algorithm_type"]     
			print("algorithm_type", algorithm_type)
			message = ""
			success_val =0
			mod = ""
			match algorithm_type:
				case 'svm': mod = 1
				case _:
					mod = 0

			if algorithm_type is not None:       
				res = await setcurrent(mod)
				if res :
					message = 'Cài đặt thành công!'
					success_val = 1
				else:
					message = 'Cập nhật thất bại!'
				render_template('setting.html', method=method,success_val=success_val, message=message)
		return redirect(url_for('setting'))	
	else:
		return redirect(url_for('login'))

@app.route("/chart")
def show_chart():
	if 'logged_in' in session:   
		return render_template("chart.html")
	else:
		return redirect(url_for('login'))


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
