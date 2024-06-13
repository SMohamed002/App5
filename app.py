from flask import Flask, request, jsonify, Response
import requests
import json
import chardet

app = Flask(__name__)

# معلومات المشروع والمستخدم
voiceflow_api_key = 'VF.DM.666b4abe052473471e12e5a9.KdDB6qO3QEz4uJde'
user_id = '666b3c4417fa190a84e61d99'
project_id = '666b3c4417fa190a84e61d9a'

# إعداد الHeaders
headers = {
    'Authorization': voiceflow_api_key,
    'Content-Type': 'application/json'
}

# دالة لإرسال رسالة إلى Voiceflow والحصول على الرد
def send_message_to_voiceflow(user_id, message):
    url = f'https://general-runtime.voiceflow.com/state/{project_id}/user/{user_id}/interact'

    payload = {
        "request": {
            "type": "text",
            "payload": message
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    detected_encoding = chardet.detect(response.content)['encoding']
    response_text = response.content.decode(detected_encoding)
    response_json = json.loads(response_text)
    return response_json

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    if not data or 'message' not in data:
        return "No message provided", 400

    user_message = data['message']
    response = send_message_to_voiceflow(user_id, user_message)

    if 'error' in response:
        return response['error'], 500

    messages = []
    for message in response:
        if message['type'] == 'text':
            messages.append(message['payload']['message'])

    # إرجاع الرد كنص عادي
    return '\n'.join(messages)

if __name__ == '__main__':
    app.run(debug=True)
