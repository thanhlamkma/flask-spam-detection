from mongoengine import connect

connect = connect(host="mongodb://127.0.0.1:27017/spam_detection")

print("connect", connect)