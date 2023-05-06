from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args, get_page_parameter
import json

app = Flask(__name__, template_folder="templates", static_url_path="/static")

def get_emails():
  with open('email.json') as json_file:
    emails = json.load(json_file)
    
  return emails

def get_pagination_emails(offset=0, emails_per_page=10):
  emails = get_emails()
  return emails[offset: offset + emails_per_page]

@app.route("/")
def home():
  return render_template("home.html")

@app.route('/apply')
def show_emails():
  emails = get_emails()

  # Pagination
  page, emails_per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")
  
  total_emails = len(emails)
  
  pagination_emails = get_pagination_emails(offset=offset, emails_per_page=emails_per_page)
  
  pagination = Pagination(page=page, per_page=emails_per_page, total=total_emails, css_framework="bootstrap4", alignment="center")

  # Render the template and pass the messages to the template
  return render_template("apply.html", emails=pagination_emails, page=page, emails_per_page=emails_per_page, pagination=pagination)

if __name__ == '__main__':
  app.run(debug=True)
