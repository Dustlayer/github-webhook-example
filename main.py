#!/usr/bin/env python3

from flask import Flask, request
import json
import requests
import telegram
import config

app = Flask(__name__)
bot = telegram.Bot(token=config.TELEGRAM_API_TOKEN)

API_HEADERS = {
    'Accept': 'application/vnd.github.v3+json'
}

def send_message(text):
    print("Send message: " + text.replace('\n', '\\n'), flush=True)
    for chat_id in config.CHAT_IDS:
        try:
            # crop the message at max length (currently 4096)
            bot.send_message(chat_id=chat_id, text=text[:telegram.constants.MAX_MESSAGE_LENGTH])
        except telegram.error.BadRequest as e:
            # this error occurred sometimes by mistake though the message was sent successfully
            if not e.message == 'Message is too long':
                raise


@app.route('/push',methods=['POST'])
def handle_push():
    """
    Handles 'push' events from Github. 
    """
    data = json.loads(request.data)
    
    # Request all commits
    api_url = data['repository']['commits_url'].replace('{/sha}', '')
    response = requests.get(api_url, headers=API_HEADERS)
    if(response.ok):
        # check if the commits of current push are verified
        verified_bools = []
        all_commits = json.loads(response.content)
        # build lookup to ease verification checking
        all_commits_lookup = {}
        for index, commit_verify in enumerate(all_commits):
            all_commits_lookup[commit_verify['sha']] = index
        
        for commit in data['commits']:
            commit_verify = all_commits[all_commits_lookup[commit['id']]]
            verified_bools.append(commit_verify['commit']['verification']['verified'])

        # send message if not all commits are signed
        if not all(verified_bools):
            send_message(f"Push von {data['pusher']['name']}.\nDie Commits sind nicht vollständig signiert!")
    else:
        send_message(f"Push von {data['pusher']['name']}.\nDie Signatur kann derzeit nicht geprüft werden.")

    return {}

@app.route('/issue',methods=['POST'])
def handle_issue():
    """
    Handles 'issue' events from Github. 
    """
    data = json.loads(request.data)
    if data['action'] in ('opened', 'reopened'):
        send_message("\n".join((f"Ein Issue mit dem Titel '{data['issue']['title']}' wurde (wieder)eröffnet.",
                     f"Link: {data['issue']['html_url']}")))
    
    return {}


@app.route('/pull',methods=['POST'])
def handle_pull():
    """
    Handles 'pull_request' events from Github. 
    """
    data = json.loads(request.data)
    if data['action'] in ('opened', 'reopened') and data['sender']['login'] != config.GITHUB_USERNAME:
        send_message("\n".join((f"Pull request von {data['sender']['login']}.",
                                f"Titel: {data['pull_request']['title']}",
                                f"Link: {data['pull_request']['html_url']}")))
    return {}

@app.errorhandler(404)
def not_found(error):
    return {"status": "not found"}, 404

# development server is used if main.py is executed directly
# otherwise e.g. gunicorn acts as WSGI server
if __name__ == '__main__':
    app.run()