from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args, get_page_parameter
import json
import connect_db as db

app = Flask(__name__, template_folder="templates", static_url_path="/static")

def get_emails():
  with open('email.json') as json_file:
    emails = json.load(json_file)
    
  return emails

def get_pagination_emails(offset=0, emails_per_page=10):
  emails = db.get_emails()
  return emails[offset: offset + emails_per_page]

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/apply")
def show_emails():
  emails = db.get_emails()

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
  return render_template("setting.html")

@app.route("/result")
def show_result():
  return render_template("setting.html")

if __name__ == '__main__':
  app.run(debug=True)
