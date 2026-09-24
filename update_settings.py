from core.database import SessionLocal
from src.settings import load_settings, save_settings
import json

db = SessionLocal()
settings = load_settings(db, owner=None)

# Browse
# Generate Image
# Write and Edit File
# Sending Emails
# Approving Skills

# The user wants to *allow* these.
# "approving skills" -> auto_approve_skills = True
settings["auto_approve_skills"] = True

# "sending emails" -> agent_email_confirm = False (so it doesn't require confirmation)
settings["agent_email_confirm"] = False

save_settings(db, settings, owner=None)
print("Settings updated")
