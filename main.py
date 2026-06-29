import sys
import config
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logic imports from separated sub-files
from lookup import LookupEngine
from instagram import InstagramEngine
from bomber import BomberEngine
from report import ReportEngine

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "⚔️ **Unified Operations Cyber Toolkit Dashboard** ⚔️\n\n"
        "Your automated multi-tool server instance interface is online.\n\n"
        "🛠 **Operational Manual Command Structure:**\n"
        "🛰 `/lookup <target>` — Track registration entries database references\n"
        "💣 `/bomb <phone> [count]` — Dispatch load testing high-density stress packets\n"
        "📸 `/insta <session> <user>` — Replicate profiles parsing web fields layout\n"
        "⚖️ `/report` — View structured report framework numerical indexes\n\n"
        "💡 *Input clean, well-formed variables to execute tasks without runtime friction.*"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

async def lookup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ **Usage Format:** `/lookup <@username_or_id>`")
        return
    
    target = context.args[0].strip()
    notif = await update.message.reply_text("🔍 *Querying centralized OSINT databases...*", parse_mode="Markdown")
    
    out = await LookupEngine.query_target(target)
    # FIXED: Avoid markdown encoding crash if raw json strings have unescaped characters
    await notif.edit_text(f"📱 **Lookup Output Data Vector Matrix:**\n\n{out}")

async def bomb_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ **Usage Format:** `/bomb <10_digit_phone> [packet_amount]`")
        return
    
    phone = context.args[0].strip()
    if not phone.isdigit() or len(phone) != 10:
        await update.message.reply_text("❌ **Validation Error:** Target string sequence must contain exactly 10 numerals.")
        return
    
    try:
        count = int(context.args[1]) if len(context.args) > 1 else 15
        count = min(count, 50)  # Caps workload threads for production memory safety
    except ValueError:
        count = 15

    notif = await update.message.reply_text(f"🚀 *Deploying workload injection threads... [{count} Requests]*", parse_mode="Markdown")
    await BomberEngine.deploy_flood_matrix(phone, count)
    await notif.edit_text(f"✅ **Sequence Completed Successfully.**\nMonitor endpoint parameters finalized cleanly via:\n{BomberEngine.DECODED_CHANNEL}")

async def insta_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("❌ **Usage Format:** `/insta <session_id> <target_username>`")
        return
    
    session_id = context.args[0].strip()
    username = context.args[1].strip()
    notif = await update.message.reply_text("🔄 *Authenticating session blocks against Instagram API endpoints...*")

    res = await InstagramEngine.extract_profile(session_id, username)
    if not res["success"]:
        await notif.edit_text(f"❌ **Extraction Error:** {res['msg']}")
        return

    summary = (
        f"👤 **Instagram Identity Extraction Object Matrix:**\n\n"
        f"🔹 **Full Identifier:** {res['full_name']}\n"
        f"🔹 **Biography Details:** {res['biography']}\n"
        f"🔹 **External Pointer:** {res['external_url']}\n"
        f"🔹 **Direct Profile Asset Link:** [Extract Asset Image]({res['profile_pic']})"
    )
    await notif.edit_text(summary, parse_mode="Markdown", disable_web_page_preview=False)

async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payload_text = ReportEngine.compile_report_manual()
    await update.message.reply_text(payload_text, parse_mode="Markdown")

def main():
    if not config.BOT_TOKEN or config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("[CRITICAL] Deployment failed: Enter a valid live variable token string configuration.")
        sys.exit(1)

    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # Mapped core interfaces routing
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("lookup", lookup_command))
    app.add_handler(CommandHandler("bomb", bomb_command))
    app.add_handler(CommandHandler("insta", insta_command))
    app.add_handler(CommandHandler("report", report_command))

    print("[SUCCESS] Application framework listener online. Polling long updates loops...")
    app.run_polling()

if __name__ == "__main__":
    main()

