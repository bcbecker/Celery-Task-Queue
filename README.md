# Celery-Task-Queue
Task queue using celery and Redis as the broker. This simple example was built with celery to compare/contrast to rq, and explore the functionalities of both (see Redis-Task-Queue for rq), though this barely scratches the surface!

## Setup
Ensure python 3.9 is installed.

Configure your environment variables, setting up your email account to be used. You will also need to change the MAIL_SERVER and MAIL_PORT (in Config) if not using gmail
```
SECRET_KEY=
EMAIL_USER=
EMAIL_PASS=
```

Install requirements:
```bash
pip install -r requirements.txt
```

Or, access virtual environment:
```bash
pip install pipenv
pipenv shell
```

### Running the Server
In separate terminal windows, you must set up Redis (needs to be installed locally), run a celery worker, and run the flask server.
Linux/Mac:
```
redis-server
```

```
cd task_queue
celery -A app.queue worker --loglevel=INFO
```

```
cd task_queue
python app.py
```
