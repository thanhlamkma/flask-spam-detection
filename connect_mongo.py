from mongodbcn import EmailDB
import json


def get_emaildb():     
    documents = EmailDB.objects().all()
    data = []
    status_sent = ["Failure","Success"] #0 - Failure and  1 - Success
    # status_spam = ["Ham","Spam"]
    for doc in documents:
        try:
            data.append({
                    "id":doc.email_id,
                    "time":doc.emailtime_at.strftime("%m/%d/%Y, %H:%M:%S"),
                    "from":doc.from_email,
                    "to":',\r\n'.join(doc.to_email),
                    "subject":doc.subject,
                    "sent":status_sent[int(doc.sent)],
                    "model": doc.modelML["model"],                
                    "spam_score":"%.2f"%doc.modelML["spam_score"],
                    "ham_score":"%.2f"%doc.modelML["ham_score"],
                    "predict":doc.modelML["predict"]
                }
            )
        except: 
            pass
    return data
