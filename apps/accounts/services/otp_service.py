import secrets
import os
import sib_api_v3_sdk
from django.conf import settings
from sib_api_v3_sdk.rest import ApiException

def generate_otp():
    return ''.join(secrets.choice("0123456789") for _ in range(6))

def send_email_otp(email, otp):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY')
    
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    # Email Content Setup
    sender = {"name": "Trendism", "email": "pureheart70156@gmail.com"}
    to = [{"email": email}]
    subject = "Trendism - Your OTP Code"
    html_content = f"<h4>Your Trendism verification code is {otp}. This code valid for 5 minutes</h4>"
    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to, 
        html_content=html_content, 
        sender=sender, 
        subject=subject
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        return True
    except ApiException as e:
        print(f"Brevo API Error: {e}")
        return False

