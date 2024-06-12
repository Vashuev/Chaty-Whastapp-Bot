import logging
from time import sleep
from flask import current_app, jsonify
import json
import requests
from .models import (
    get_message_id, 
    save_message_progress,
)
from app.models import (
    save_message_progress,
    save_start_date,
    save_end_date,
    save_budget,
    save_company,
    save_job,
    save_email,
    save_otp,

    get_message_id,
    get_start_date,
    get_end_date,
    get_budget,
    get_company,
    get_job,
    get_email,
    get_otp,
    verfity_otp,

    delete_user,
)
# from app.services.openai_service import generate_response
import re

MESSAGES = [
    # 0 : intial reply
    [
        (
            "Hello, I'm a Purchasing Bot, to help you here",
            0
        ),
        (
            "You can start purchasing by typing *Purchase*",
            0
        )
    ],
    
    # 1: Purchasing option
    [
        (
            'Purchasing Order123\n{"orderId" : 1, "value" : 22.2}',
            1
        ),
    ],
    
    # 2: Purchase
    [
        (
            "Order with id '1' is purchased",
            0
        ),
        (
            "All done! Do you want to Purchase again?",
            3
        )
    ],
    
    # 3: Cancel
    [
        (
            "Order with id '1' is cancelled",
            0
        ),
        (
            "All done! Do you want to Purchase again?",
            3
        )
    ],
    
    # 4: Proper format at any place
    [
        (
            "Please enter in proper format (or what has been asked above)! Thanks",
            0
        )
    ],

    # 5: Happy day to you!
    [
        (
            "Happy Day to you!!",
            0
        )
    ]
]

def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )

def get_button_message_input(recipient, text, buttons):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": text
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )

def generate_buttons(button_identifier):
    if button_identifier == 1:
        return [
            {
                "type": "reply",
                "reply": {
                    "id": "purchase",
                    "title": "Purchase"
                }
            },
            {
                "type": "reply",
                "reply": {
                    "id": "cancel",
                    "title": "Cancel"
                }
            }
        ]
    elif button_identifier == 2:
        return [
            {
                "type": "reply",
                "reply": {
                    "id": "otp",
                    "title": "Resend OTP"
                }
            },
            {
                "type": "reply",
                "reply": {
                    "id": "email",
                    "title": "Enter another email"
                }
            }
        ]
    elif button_identifier == 3:
        return [
            {
                "type": "reply",
                "reply": {
                    "id": "start",
                    "title": "Start Again"
                }
            },
            {
                "type": "reply",
                "reply": {
                    "id": "finish",
                    "title": "Finish"
                }
            }
        ]
    elif button_identifier == 4:
        return [
            {
                "type": "reply",
                "reply": {
                    "id": "one",
                    "title": "Just a one day shoot"
                }
            }
        ]
    else:
        print("No button identifier is identified")
        pass
    return None

def valid_date(date_str):
    # Implement date validation logic
    return True  # Placeholder for demonstration

def format_availability_message(dates):
    if not dates:
        return "No availability dates provided."
    elif len(dates) == 1:
        dates_str = str(dates[0])
    else:
        dates_str = '\n'.join([str(d) for d in dates])
    message = f"Hooray - Kato is available on \n{dates_str}"
    return message

def generate_response(msg_id, user_response, user_id):
    if msg_id == 0:  # Relpy Hello
        if user_response.lower() == "hi":
            return MESSAGES[0], 1
        else:
            return MESSAGES[4], 0 
    elif msg_id == 1:  
        if user_response.lower() == "purchase":
            return MESSAGES[1], 2
        else:
            return MESSAGES[4], 1
    elif msg_id == 2:
        if user_response.lower() == "purchase":
            return MESSAGES[2], 3
        elif user_response.lower() == "cancel":
            return MESSAGES[3], 3
        else:
            return MESSAGES[4], 2
    elif msg_id == 3:
        if user_response == "start":
            return MESSAGES[0], 1 
        elif user_response == "finish":
            return MESSAGES[5], 4 
        else:
            return MESSAGES[4], 3
        
def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=10
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response


def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text


def process_whatsapp_message(body):
    user_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    
    # Check if the message is a text message or an interactive button reply
    if "text" in message:
        message_body = message["text"]["body"]
    elif "interactive" in message:
        message_body = message["interactive"]["button_reply"]["id"]
    else:
        logging.error("Unsupported message type")
        return jsonify({"status": "error", "message": "Unsupported message type"}), 400
    
    msg_id = get_message_id(user_id)

    print("msg_id = ", msg_id)

    responses, new_msg_id = generate_response(msg_id, message_body, user_id)
    for response in responses:
        if response[1] == 0:
            data = get_text_message_input(user_id, response[0])
        else:
            buttons = generate_buttons(response[1])
            data = get_button_message_input(user_id, response[0], buttons)
        send_message(data)
        sleep(3)
    if new_msg_id == 4:
        delete_user(user_id)
    else:
        save_message_progress(user_id, new_msg_id)


def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )
 