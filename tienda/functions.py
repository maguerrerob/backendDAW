import base64
import requests

PAYPAL_CLIENT_ID = 'Adx3P3esicSyz81xOltFtOqUCDNWdyCGvvMKDyShLTOQLw1ZBd8VnLwZ20Ojb8GAqgAGGX1Z1ZNPvQ73'
PAYPAL_CLIENT_SECRET = 'ED1TRkCDmlVrlNt1lLlzKr0ilMqfPGrh9WFyE6j3ZwW8CvQLjN3xbAIjC_wJmWwMdP7CrrzugCzRhtPF'
BASE_URL = 'https://api-m.sandbox.paypal.com'  # Cambia a la URL de producción para el entorno de producción
# BASE_URL = 'https://sandbox.paypal.com'

def generateAccessToken():
    if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
        raise ValueError("PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET must be set.")
    
    auth = f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}"
    auth = base64.b64encode(auth.encode()).decode('utf-8')

    response = requests.post(
        "https://api-m.sandbox.paypal.com/v1/oauth2/token",
        data={"grant_type": "client_credentials"},
        headers={"Authorization": f"Basic {auth}"}
    )

    data = response.json()
    return data['access_token']