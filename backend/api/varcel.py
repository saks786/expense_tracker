import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.main import app as handler  # Vercel needs "handler"
