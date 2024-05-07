from flask import Flask, request, jsonify, render_template, redirect, url_for,session
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from datetime import datetime
import requests
from datetime import timedelta
import random
import os 

def randstring(length):
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))

app = Flask(__name__)
app.secret_key = randstring(32)

app.permanent_session_lifetime = timedelta(minutes=30)


# Public RSA key (load this from a file or environment variable)
PUBLIC_KEY_PATH = 'public_key.pem'
PUBLIC_KEY_PATH = os.path.join(os.path.dirname(__file__), PUBLIC_KEY_PATH)
with open(PUBLIC_KEY_PATH, 'r') as key_file:
    public_key = RSA.import_key(key_file.read())

def fetch_json_8000():
    # Fetch JSON from the server running on port 8000
    try:
        response = requests.get("http://localhost:8000/2/summary")
        #get deatil of what the proxy server is doing
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        return {'error': str(e)}

def save_challenge(challenge):
    # Store the challenge in a file
    with open('challenge.txt', 'w') as f:
        f.write(challenge)

def load_challenge_compare(challenge):
    # Load the challenge from a file and compare it with the given challenge
    with open('challenge.txt', 'r') as f:
        return f.read().strip() == challenge

def is_authenticated():
    # Check if 'logged_in' key exists in the session and is True
    return session.get('logged_in', False)


@app.route('/status')
def status():

    if not is_authenticated():
        return 'Access denied', 403
    
    return render_template('status.html', data=fetch_json_8000())

@app.route('/request_challenge')
def request_challenge():
    challenge = randstring(64)+str(datetime.now().timestamp())
    #store the challenge in the session
    session['challenge'] = challenge
    save_challenge(challenge)
    return jsonify({'challenge': challenge})

@app.route('/xmr', methods=['POST'])
def xmr_route():
    signature = request.json.get('signature')
    challenge = request.json.get('challenge')

    if signature is None or challenge is None:
        return 'Missing signature or challenge', 400

    try:
        
        if challenge != session['challenge']:
            return 'Invalid challenge', 403
        
        if not load_challenge_compare(challenge):
            return 'Invalid challenge', 403
        
        hash_obj = SHA256.new(challenge.encode())
        signature_bytes = bytes.fromhex(signature)
        pkcs1_15.new(public_key).verify(hash_obj, signature_bytes)
        session.permanent = True  # Make the session permanent so it respects the lifetime
        session['logged_in'] = True
        return (jsonify({'message': 'Successfully authenticated'}), 200)

    except (ValueError, IndexError):
        return 'Invalid signature', 403

@app.route('/')
def home():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(port=8080)
