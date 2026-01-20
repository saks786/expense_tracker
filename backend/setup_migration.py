"""
Automated Supabase Migration Setup Script
This script helps you set up the .env file interactively
"""
import os
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_step(number, text):
    print(f"\n📍 Step {number}: {text}")
    print("-" * 60)

def get_input(prompt, default=""):
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        while True:
            user_input = input(f"{prompt}: ").strip()
            if user_input:
                return user_input
            print("❌ This field is required. Please try again.")

def main():
    print_header("Supabase Migration Setup Wizard")
    
    print("This wizard will help you set up your .env file for Supabase PostgreSQL.")
    print("\nYou'll need:")
    print("  1. Supabase project credentials (from Supabase Dashboard)")
    print("  2. Optional: Stripe and SendGrid credentials")
    
    input("\nPress Enter to continue...")
    
    # Check if .env already exists
    env_path = Path(".env")
    if env_path.exists():
        print(f"\n⚠️  Warning: .env file already exists!")
        overwrite = input("Do you want to overwrite it? (yes/no): ").strip().lower()
        if overwrite not in ['yes', 'y']:
            print("❌ Setup cancelled. Your existing .env file was not modified.")
            return
    
    # Collect Supabase credentials
    print_step(1, "Supabase Database Configuration")
    print("\n📖 How to find these values:")
    print("   1. Go to https://supabase.com/dashboard")
    print("   2. Select your project")
    print("   3. Go to Settings → Database")
    print("   4. Find 'Connection String' section\n")
    
    database_url = get_input("Enter your DATABASE_URL (PostgreSQL connection string)")
    
    print_step(2, "Supabase API Configuration")
    print("\n📖 How to find these values:")
    print("   1. In Supabase Dashboard, go to Settings → API")
    print("   2. Copy 'Project URL' and 'anon/public key'\n")
    
    supabase_url = get_input("Enter your SUPABASE_URL")
    supabase_key = get_input("Enter your SUPABASE_KEY (anon/public key)")
    
    print_step(3, "Authentication Configuration")
    print("\n🔐 This is used for JWT token generation.")
    
    import secrets
    suggested_secret = secrets.token_urlsafe(32)
    secret_key = get_input(
        "Enter SECRET_KEY (or press Enter to generate a random one)",
        suggested_secret
    )
    
    algorithm = get_input("Enter ALGORITHM", "HS256")
    token_expire = get_input("Enter ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    
    print_step(4, "Optional Services")
    print("\n⚡ These are optional. Press Enter to skip.")
    
    # SendGrid
    print("\n📧 SendGrid (for email notifications):")
    sendgrid_key = get_input("Enter SENDGRID_API_KEY (optional)", "your_sendgrid_api_key_here")
    from_email = get_input("Enter FROM_EMAIL (optional)", "noreply@yourdomain.com")
    
    # Stripe
    print("\n💳 Stripe (for payment processing):")
    stripe_secret = get_input("Enter STRIPE_SECRET_KEY (optional)", "sk_test_your_stripe_secret_key_here")
    stripe_public = get_input("Enter STRIPE_PUBLISHABLE_KEY (optional)", "pk_test_your_stripe_publishable_key_here")
    stripe_webhook = get_input("Enter STRIPE_WEBHOOK_SECRET (optional)", "whsec_your_webhook_secret_here")
    
    print_step(5, "Application Settings")
    
    frontend_url = get_input("Enter FRONTEND_URL", "http://localhost:5173")
    debug = get_input("Enable DEBUG mode? (True/False)", "False")
    environment = get_input("Enter ENVIRONMENT", "production")
    
    # Create .env content
    env_content = f"""# ==========================================
# Database Configuration
# ==========================================
DATABASE_URL={database_url}

# ==========================================
# Supabase Configuration
# ==========================================
SUPABASE_URL={supabase_url}
SUPABASE_KEY={supabase_key}

# ==========================================
# Authentication
# ==========================================
SECRET_KEY={secret_key}
ALGORITHM={algorithm}
ACCESS_TOKEN_EXPIRE_MINUTES={token_expire}

# ==========================================
# Email Service (SendGrid)
# ==========================================
SENDGRID_API_KEY={sendgrid_key}
FROM_EMAIL={from_email}

# ==========================================
# Payment Gateway (Stripe)
# ==========================================
STRIPE_SECRET_KEY={stripe_secret}
STRIPE_PUBLISHABLE_KEY={stripe_public}
STRIPE_WEBHOOK_SECRET={stripe_webhook}

# ==========================================
# Frontend URL (for CORS)
# ==========================================
FRONTEND_URL={frontend_url}

# ==========================================
# Application Settings
# ==========================================
DEBUG={debug}
ENVIRONMENT={environment}
"""
    
    # Write .env file
    with open(".env", "w") as f:
        f.write(env_content)
    
    print_header("✅ Setup Complete!")
    print("Your .env file has been created successfully!")
    print("\n📋 Next steps:")
    print("   1. Run the migration SQL script in Supabase Dashboard:")
    print("      → SQL Editor → Paste contents of supabase_migration.sql → Run")
    print("\n   2. Install dependencies:")
    print("      → pip install -r requirements.txt")
    print("\n   3. Test the migration:")
    print("      → python test_migration.py")
    print("\n   4. Start the application:")
    print("      → uvicorn app.main:app --reload")
    print("\n📖 For detailed instructions, see MIGRATION_GUIDE.md")
    print("")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
    except Exception as e:
        print(f"\n\n❌ Error during setup: {e}")
        print("Please check your inputs and try again.")
