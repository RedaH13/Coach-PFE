import json
import os
from datetime import datetime

def log_telegram_message(state: dict):
    """Sauvegarde le message brut dans memory.json (Identique à ton flow n8n)"""
    file_path = "data/memory.json"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Extraction du dernier message user
    last_message = state["messages"][-1].content
    
    log_data = {
        "chatId": state.get("chat_id"),
        "timestamp": state.get("timestamp", int(datetime.now().timestamp())),
        "message": last_message
    }
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_data, ensure_ascii=False) + "\n")