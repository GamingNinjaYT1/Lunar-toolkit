class ReportEngine:
    VIOLATION_SCHEMA = {
        "1": "I don't like it / Other",
        "2": "Child Abuse Material",
        "3": "Violence or Explicit Threat",
        "4": "Illegal Goods Traffic",
        "5": "Illegal Adult Pornography",
        "6": "Personal Identity Theft / Doxxing",
        "7": "Terrorism / Safe Space Threat",
        "8": "Deceptive Fraud Scam / Advertising Spam",
        "9": "Copyright Infringement",
        "10": "Other Violations"
    }

    @classmethod
    def compile_report_manual(cls) -> str:
        text = (
            "⚖️ **Telegram Reporting Service Index Protocols** ⚖️\n\n"
            "Heavy multi-account automated report floods require persistent user account `.session` tokens via local terminal executions.\n\n"
            "📋 **Reason Code Mappings Reference:**\n"
        )
        for key, value in cls.VIOLATION_SCHEMA.items():
            text += f"🔹 `{key}` — {value}\n"
        text += "\n💡 *Usage:* Pass these standardized lookup keys directly inside your standalone script tasks."
        return text

