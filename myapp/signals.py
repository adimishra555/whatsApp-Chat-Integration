
import json
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Product, Profile

def send_whatsapp_message(phone_number, message):
    url = "https://6gkkp8.api.infobip.com/whatsapp/1/message/template"
    payload = json.dumps({
        "messages": [
            {
                "from": "447860099299",
                "to": phone_number,
                "messageId": "a97b952e-ae14-4b5d-8560-5d6f0a2c5f73",
                "content": {
                    "templateName": "message_test",
                    "templateData": {
                        "body": {
                            "placeholders": [message]
                        }
                    },
                    "language": "en"
                }
            }
        ]
    })
    headers = {
        'Authorization': 'App 932c1b30462c3f6ed0fed9dafca533d0-a38ec055-a967-4487-8afa-00894222bcbe',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending WhatsApp message: {e}")

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Profile)
def send_welcome_message(sender, instance, created, **kwargs):
    if created:
        user_phone_number = instance.phone_number
        user_name = instance.user.username
        send_whatsapp_message(
            phone_number=user_phone_number,
            message=f"Your account is successfully created. Now you can upload and see your product in our website with full information, {user_name}."
        )

@receiver(post_save, sender=Product)
def send_product_upload_message(sender, instance, created, **kwargs):
    if created:
        user_phone_number = instance.user.profile.phone_number
        send_whatsapp_message(
            phone_number=user_phone_number,
            message="Your product is successfully uploaded."
        )
