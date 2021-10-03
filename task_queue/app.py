from flask import Flask
from flask_mail import Mail, Message
from celery import Celery
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

queue = Celery(app.name, broker=Config.CELERY_BROKER_URL)
#only needed if storing tasks/results
queue.conf.update(app.config)

mail = Mail(app)


@queue.task
def func(param):
    return result





if __name__ == "__main__":
    app.run()