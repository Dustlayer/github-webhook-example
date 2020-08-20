# github-webhook-example
This is an example implementation for GitHub Webhooks using python3 with flask.

## Usage
Copy "config.example.py" to "config.py" and provide fitting values.
Then you can start by using 
~~~
docker-compose up
~~~

## Notes
If started directly, the flask development server is used.
This is not suitable for production purposes.
Cf. https://flask.palletsprojects.com/en/master/deploying/

For production the WSGI-server gunicorn is used.
