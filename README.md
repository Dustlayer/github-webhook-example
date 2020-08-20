# github-webhook-example
This is an example implementation for GitHub Webhooks using python3 with flask.

## Preparation
You have to configure three webhooks on your repository.
So that
- 'push' events end up in /push
- 'issue' events end up in /issue 
- 'pull' events end up in /pull

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
