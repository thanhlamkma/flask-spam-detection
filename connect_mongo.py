from mongodbcn import ResultEmail, ResultModel
import json


def get_emaildb():     
    
    documents = ResultEmail.objects().all()
    data = []
    status_sent = ["Failure","Success"] #0 - Failure and  1 - Success
    status_spam = ["Ham","Spam"]
    for doc in documents:
        data.append({
                "id":doc.email_id,
                "time":doc.emailtime_at.strftime("%m/%d/%Y, %H:%M:%S"),
                "from":doc.from_email,
                "to":',\r\n'.join(doc.to_email),
                "subject":doc.subject,
                "sent":status_sent[int(doc.sent)],
                "model": doc.modelML["model"],                
                "spam_score":"%.2f"%doc.modelML["spam_score"],
                "non_spam_score":"%.2f"%doc.modelML["non_spam_score"],
                "predict":status_spam[doc.modelML["predict"]]
            }
        )
    return data