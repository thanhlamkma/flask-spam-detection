from mongoengine import connect, Document,EmbeddedDocument,fields
import datetime

db_store = "email_db"
host =f"mongodb://127.0.0.1:27017/{db_store}"
connect(host=host)

class ModelInfo(EmbeddedDocument):
    model = fields.StringField()
    spam_score = fields.FloatField()
    ham_score = fields.FloatField()
    predict = fields.IntField()

class EmailDB(Document):
    email_id = fields.SequenceField()
    message_id = fields.StringField()
    emailtime_at = fields.DateTimeField(default=datetime.datetime.now)
    from_email = fields.EmailField()
    to_email = fields.ListField()
    subject = fields.StringField()
    modelML = fields.EmbeddedDocumentField(ModelInfo)
    sent = fields.BooleanField(default=False)

