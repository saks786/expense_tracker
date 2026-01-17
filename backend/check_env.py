from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("SENDGRID_API_KEY") is not None)
print(os.getenv("FROM_EMAIL"))
