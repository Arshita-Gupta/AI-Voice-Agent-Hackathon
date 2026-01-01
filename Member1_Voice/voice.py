from twilio.rest import Client
from flask import Flask, Response
import threading
import time

app = Flask(__name__)

# Twilio webhook that sends voice response
@app.route('/voice', methods=['GET', 'POST'])
def voice():
    response = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-IN">
        Hello. This is an AI voice agent prototype.
        This is a test call from our hackathon project.
        Thank you.
    </Say>
    <Pause length="2"/>
    <Hangup/>
</Response>"""
    return Response(response, mimetype='text/xml')


def make_call():
    # THESE MUST BE FILLED DURING LIVE DEMO
    account_sid = "YOUR_TWILIO_ACCOUNT_SID"
    auth_token = "YOUR_TWILIO_AUTH_TOKEN"
    twilio_number = "YOUR_TWILIO_PHONE_NUMBER"
    user_number = "DESTINATION_PHONE_NUMBER"
    webhook_url = "YOUR_NGROK_URL"

    client = Client(account_sid, auth_token)

    try:
        call = client.calls.create(
            url=webhook_url,
            to=user_number,
            from_=twilio_number,
            method="GET"
        )

        print("Call started successfully")
        print("Call SID:", call.sid)
        print("Calling:", user_number)

    except Exception as e:
        print("Error while making call:", e)


if __name__ == "__main__":
    print("Starting Voice Server...")
    print("Run: ngrok http 8000")
    print("Paste ngrok HTTPS URL in webhook_url")

    server_thread = threading.Thread(
        target=lambda: app.run(port=8000, debug=False, use_reloader=False)
    )
    server_thread.daemon = True
    server_thread.start()

    time.sleep(3)
    make_call()

    while True:
        time.sleep(1)
