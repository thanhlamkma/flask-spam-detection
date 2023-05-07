import redis
import json

# Tự động decode tất cả giá trị trả về thành string, sử dụng utf-8.
client = redis.Redis(host='localhost', port=6379, db=0)

def set_email():
  with open("email.json") as json_file:
    emails = json.load(json_file)

  client.json().set("totalEmails", "$", emails)

def get_emails():
  result = client.json().get("totalEmails", "$")
  
  print(result[0])
  
  return result[0]
    
if __name__ == "__main__":
  set_email()
  get_emails()