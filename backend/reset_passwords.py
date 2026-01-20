"""Reset test user passwords to 'password123'"""
from dotenv import load_dotenv
load_dotenv()

from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash
import bcrypt

db = SessionLocal()

# Hash password123 with bcrypt (to match existing format)
new_password = "password123"
# Using bcrypt directly to match the existing format
new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print(f"New password: {new_password}")
print(f"New hash: {new_hash}")
print()

# Update all test users
test_users = ["testuser1", "testuser2", "testuser3"]
for username in test_users:
    user = db.query(User).filter(User.username == username).first()
    if user:
        old_hash = user.password[:30]
        user.password = new_hash
        print(f"✅ Updated {username}")
        print(f"   Old: {old_hash}...")
        print(f"   New: {new_hash[:30]}...")
    else:
        print(f"❌ User {username} not found")

db.commit()
print("\n✅ Password reset complete! All test users now have password: password123")

# Verify the update worked
print("\nVerifying passwords...")
for username in test_users:
    user = db.query(User).filter(User.username == username).first()
    if user:
        is_valid = bcrypt.checkpw(new_password.encode('utf-8'), user.password.encode('utf-8'))
        print(f"  {username}: {'✅ VALID' if is_valid else '❌ INVALID'}")

db.close()
