import json
import os

from dotenv import load_dotenv
from flask import Flask, Response, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

app = Flask(__name__)
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# each message_sid corresponds to a template message created in Twilio Console
message_sids = {
    "menu": "HX08de16cf3e01dee790bb612632f6d230",
    "catalogo_web": "HX06c00b157f2567a380acd81201987ec4",
    "pedido_personalizado": "HXd5f51d3bcd6bb633f3b7a4313eedb2ad",
    "ayuda_reclamo": "HX230ad3f2cd7bfe8bb5f51b5105aafb3b",
    "error": "HXc1bb2767268134703d02886b0ea518d0",
}


@app.route("/reply_whatsapp", methods=["POST"])
def reply_whatsapp():
    receiver = request.values.get("From", "")
    button_id = request.values.get("ButtonPayload", "").strip()

    sid = message_sids["menu"]

    if message_sids.get(button_id):
        sid = message_sids.get(button_id)

    twilio_client.messages.create(
        content_sid=sid,
        to=receiver,
        from_=f"whatsapp:{TWILIO_PHONE_NUMBER}",
        content_variables=json.dumps({}),
    )

    return Response(str(MessagingResponse()), status=200, mimetype="text/xml")


if __name__ == "__main__":
    app.run(port=3000)
