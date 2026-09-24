from core.database import SessionLocal
from src.settings import load_settings, save_settings

db = SessionLocal()
settings = load_settings()

# Fix action confirmations
settings["auto_approve_skills"] = True
settings["agent_email_confirm"] = False

# Make sure none of these tools are disabled
tools_to_enable = {
    "web_search", "web_fetch",
    "generate_image",
    "write_file", "edit_file",
    "send_email", "read_email", "list_emails", "reply_to_email", "delete_email", "archive_email", "mark_email_read", "bulk_email"
}

disabled = set(settings.get("disabled_tools", []))
disabled -= tools_to_enable
settings["disabled_tools"] = list(disabled)

save_settings(settings)
print("Updated settings successfully!")
