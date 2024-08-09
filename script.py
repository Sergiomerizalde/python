import requests
from requests.auth import HTTPBasicAuth
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# This script is connected to the noreply@meico.us email and send en email based on the parameters sent
# All the authentication keys are the for Jira Automatic Email App on Azure App Portal
# If I wanted to use this function in another app. I would have to create a new API in Azure to get a new access

CLIENT_ID = "AGREGAR CLIENT INFO" 
CLIENT_SECRET = "AGREGAR CLIENT INFO"  # client secret value
TENANT_ID = "AGREGAR CLIENT INFO" 
FROM_EMAIL = 'noreply@meico.us'
USER_PRINCIPAL_NAME = "noreply@meico.us"  # The user principal name of the sender


def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'client_id': CLIENT_ID,
        'scope': 'https://graph.microsoft.com/.default',
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }

    print("Requesting access token...")
    response = requests.post(url, headers=headers, data=data)

    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content}")

    response.raise_for_status()
    return response.json()['access_token']


def send_email(to_email, subject, customer_name):
    token = get_access_token()
    url = f'https://graph.microsoft.com/v1.0/users/{USER_PRINCIPAL_NAME}/sendMail'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # HTML Email Body with Header Logo and Footer Icons
    body = f"""
    <html>
    <head></head>
    <body>
        <!-- Header with logo -->
        <div style="text-align: center; padding: 10px;">
            <img src="https://yourdomain.com/path/to/logo.png" alt="Meico Solar Logo" style="width: 200px; height: auto;">
        </div>
        
        <p>Dear {customer_name},</p>
        
        <p>At Meico Solar, we value your feedback. That’s why we would like to invite you to participate in a short survey about your recent experience.</p>
        
        <p>Click on the link below to share your opinion.</p>
        
        <p><a href="https://forms.office.com/Pages/ResponsePage.aspx?id=kixtoAN4f0GYEhavYA_uR63-MtvYqilDmFNNJjlAjg1UNjk3MjNBN0VTN09WU0VMQk1BNFNPS1o3NC4u&r7e60b30a415245fdb2d1cb837a812748={to_email}" style="color: #007bff;">Rate your experience</a></p>
        
        <p>Thank you for choosing Meico Solar and for your ongoing support. We look forward to hearing from you soon.</p>
        
        <p>Warm regards,</p>
        <p>Meico Solar</p>
        
        <!-- Footer with social media icons -->
        <div style="text-align: center; padding: 10px; margin-top: 20px;">
            <a href="https://www.yourwebsite.com" style="margin-right: 15px;">
                <img src="https://yourdomain.com/path/to/webpage_icon.png" alt="Webpage" style="width: 24px; height: auto;">
            </a>
            <a href="https://www.instagram.com/yourcompany" style="margin-right: 15px;">
                <img src="https://yourdomain.com/path/to/instagram_icon.png" alt="Instagram" style="width: 24px; height: auto;">
            </a>
            <a href="https://www.linkedin.com/company/yourcompany">
                <img src="https://yourdomain.com/path/to/linkedin_icon.png" alt="LinkedIn" style="width: 24px; height: auto;">
            </a>
        </div>
    </body>
    </html>
    """
    
    email = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "HTML",
                "content": body
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": to_email
                    }
                }
            ],
            "from": {
                "emailAddress": {
                    "address": FROM_EMAIL
                }
            }
        }
    }
    response = requests.post(url, headers=headers, json=email)
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content}")
    response.raise_for_status()
    print(f"Email sent successfully to {to_email}")


# Example usage of email sent
if __name__ == "__main__":
    to_email = 'femeisel@gmail.com'
    subject = 'Rate your experience with Meico Solar Support'
    customer_name = 'John Doe'  # Example customer name
    send_email(to_email, subject, customer_name)



