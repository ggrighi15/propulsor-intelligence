from dotenv import load_dotenv
import os


def get_config():
    load_dotenv()
    return {
        'SECRET_KEY': os.getenv('APP_SECRET_KEY', 'propulsor_secret_key_2025'),
        'DEFAULT_USERNAME': os.getenv('DEFAULT_USERNAME', 'gustavo'),
        'DEFAULT_PASSWORD': os.getenv('DEFAULT_PASSWORD', 'propulsor2025'),
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', ''),
        'WHATSAPP_TOKEN': os.getenv('WHATSAPP_TOKEN', ''),
    }
