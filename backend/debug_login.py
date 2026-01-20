"""Debug password verification"""
from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from app.models import User
from app.auth import verify_password
import bcrypt

# Test credentials
test_username = "testuser1"
test_password = "password123"

db = SessionLocal()
user = db.query(User).filter(User.username == test_username).first()

if user:
    print(f"✅ Found user: {user.username}")
    print(f"📧 Email: {user.email}")
    print(f"🔑 Password hash: {user.password[:60]}...")
    print(f"🔐 Hash type: {'bcrypt' if user.password.startswith('$2') else 'other'}")
    print()
    
    # Test verification with bcrypt directly
    print("Testing password verification...")
    try:
        bcrypt_result = bcrypt.checkpw(test_password.encode('utf-8'), user.password.encode('utf-8'))
        print(f"  Direct bcrypt.checkpw(): {bcrypt_result}")
    except Exception as e:
        print(f"  Direct bcrypt.checkpw() ERROR: {e}")
    
    # Test with our verify_password function
    try:
        verify_result = verify_password(test_password, user.password)
        print(f"  verify_password() function: {verify_result}")
    except Exception as e:
        print(f"  verify_password() ERROR: {e}")
    
    # Test with wrong password
    try:
        wrong_result = verify_password("wrongpassword", user.password)
        print(f"  Wrong password test: {wrong_result}")
    except Exception as e:
        print(f"  Wrong password ERROR: {e}")
else:
    print(f"❌ User '{test_username}' not found!")
    print("\nAvailable users:")
    all_users = db.query(User).all()
    for u in all_users:
        print(f"  - {u.username} ({u.email})")

db.close()
