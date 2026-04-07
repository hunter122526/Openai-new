from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Aliceblue Dev Portal API endpoint (replace with actual)
ALICEBLUE_DEV_PORTAL_URL = os.getenv('ALICEBLUE_DEV_PORTAL_URL', 'https://developers.aliceblueonline.com/api/update')
ALICEBLUE_API_KEY = os.getenv('ALICEBLUE_API_KEY')

@app.route('/webhook', methods=['POST'])
def git_webhook():
    """Handle Git webhook and redirect to Aliceblue dev portal."""
    data = request.json

    if not data:
        return jsonify({'error': 'No data received'}), 400

    # Extract relevant info from Git webhook (e.g., push event)
    if 'ref' in data and data['ref'] == 'refs/heads/main':
        # Trigger update to Aliceblue dev portal
        headers = {
            'Authorization': f'Bearer {ALICEBLUE_API_KEY}',
            'Content-Type': 'application/json'
        }

        payload = {
            'action': 'update',
            'repository': data.get('repository', {}).get('name'),
            'commit': data.get('after'),
            'pusher': data.get('pusher', {}).get('name')
        }

        try:
            response = requests.post(ALICEBLUE_DEV_PORTAL_URL, json=payload, headers=headers)
            response.raise_for_status()
            return jsonify({'status': 'success', 'aliceblue_response': response.json()}), 200
        except requests.RequestException as e:
            return jsonify({'error': f'Failed to update Aliceblue: {str(e)}'}), 500

    return jsonify({'status': 'ignored', 'reason': 'Not a main branch push'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)