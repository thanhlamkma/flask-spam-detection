from flask import Flask, render_template, request, redirect, url_for
from flask_paginate import Pagination, get_page_args, get_page_parameter
import json
from connect_mongo import get_emaildb

app = Flask(__name__, template_folder="templates", static_url_path="/static")


def get_pagination_emails(offset=0, emails_per_page=10):
  emails = get_emaildb()
  return emails[offset: offset + emails_per_page]

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Tên đăng nhập hoặc mật khẩu không chính xác.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/apply")
def show_emails():
  emails = get_emaildb()

  # Pagination
  page, emails_per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")
  
  total_emails = len(emails)
  
  pagination_emails = get_pagination_emails(offset=offset, emails_per_page=emails_per_page)
  
  pagination = Pagination(page=page, per_page=emails_per_page, total=total_emails, css_framework="bootstrap4", alignment="center")

  # Render the template and pass the messages to the template
  return render_template("apply.html", emails=pagination_emails, page=page, emails_per_page=emails_per_page, pagination=pagination)

@app.route("/setting", methods=["GET", "POST"])
def setting():
  if request.method == "POST":
    algorithm_type = request.form["algorithm_type"]
    
    print("algorithm_type", algorithm_type)
    
  return render_template("setting.html")

@app.route("/chart")
def show_chart():
  return render_template("chart.html")

@app.route("/result")
def show_result():
  return render_template("setting.html")

if __name__ == '__main__':
  app.run(host="0.0.0.0",debug=True)
