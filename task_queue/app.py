from flask import Flask, escape, request, render_template, redirect, url_for, flash, session
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
def send_async_email(email_data):
    """Background task to send an email with flask-mail"""
    msg = Message(email_data['subject'],
                  sender=Config.MAIL_USERNAME,
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    with app.app_context():
        mail.send(msg)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', email=session.get('email', ''))
    
    email = escape(request.form['email'])
    session['email'] = email
    email_data = {
        'subject': 'Celery says hi',
        'to': email,
        'body': 'This is a test email sent from a background Celery task.'
    }

    if request.form['submit'] == 'Send':
        # send right away
        send_async_email.delay(email_data)
        flash(f'Sending email to {email}')
    else:
        # send in one minute
        send_async_email.apply_async(args=[email_data], countdown=60)
        flash(f'An email will be sent to {email} in 1 min')

    return redirect(url_for('index'))




if __name__ == "__main__":
    app.run()