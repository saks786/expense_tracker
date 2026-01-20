"""Check password hash types in database"""
from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from app.models import User

db = SessionLocal()
users = db.query(User).all()

if users:
    print(f"Found {len(users)} users in database\n")
    for user in users[:5]:  # Show first 5 users
        password_hash = user.password[:40] if user.password else "None"
        print(f"User: {user.username}")
        print(f"  Hash: {password_hash}...")
        
        # Detect hash type
        if user.password:
            if user.password.startswith('$2a$') or user.password.startswith('$2b$'):
                print(f"  Type: bcrypt\n")
            elif user.password.startswith('$argon2'):
                print(f"  Type: argon2\n")
            elif user.password.startswith('$pbkdf2'):
                print(f"  Type: pbkdf2\n")
            else:
                print(f"  Type: unknown/plain\n")
else:
    print("No users found in database")

db.close()
