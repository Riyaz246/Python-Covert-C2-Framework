# Python Covert C2 Framework (via Discord)

This is a portfolio project demonstrating the creation of a simple, but effective, covert Command and Control (C2) framework. This project was built to practice offensive TTPs (Tactics, Techniques, and Procedures) from a threat-actor perspective.

## Project Goal

The goal was to bypass standard network detection (like firewall rules) by tunneling C2 traffic over the API of a trusted, high-reputation application (Discord).

This directly applies skills from my resume, such as **Python (Advanced)**, **REST APIs**, and **Threat Actor Tracking**.

## How It Works

The framework consists of two main Python scripts:

1.  **`c2_console.py` (The Server):**
    * Provides an attacker-facing console.
    * Takes simple bash commands (e.g., `ls /etc/`).
    * Uses Python's `base64` library to obfuscate the command into a payload.
    * Uses the Discord Bot API (via `requests`) to post the payload to a private `#tasking` channel.

2.  **`implant.py` (The Victim):**
    * Runs on the "compromised" machine.
    * Periodically polls the `#tasking` channel by reading messages via the Discord API.
    * When it finds a new payload, it decodes the `base64` string and executes the command locally using `subprocess.run()`.
    * It captures the command's output and posts it back to the `#results` channel for exfiltration.

## Project Screenshots & Workflow

Here is the step-by-step visual documentation of the project.

### 1. Lab Setup
The lab was built using three Kali Linux VMs in VirtualBox on a host-only network.
* `kali-c2-server` (Attacker)
* `kali-victim-implant` (Victim)
* (A third VM was originally for an AI-engine, but this was pivoted away from).

![Lab Setup - VM IPs](Screenshot%20(270).png)

---

### 2. C2 Channel Setup
A private Discord server was created, and a new Bot was "invited." This bot's API token is the key to the C2 channel.

![Discord Bot Setup](Screenshot%202025-11-11%20123639.png)

---

### 3. Implant VM Preparation
On the victim VM, a Python virtual environment (`venv`) was created to isolate the script and its `requests` dependency.

![Implant VM Setup](Screenshot%20(273).png)

---

### 4. Final End-to-End Test
This screenshot shows the final, successful test using the `c2_console.py` (Version 6, Local Encode) on the right and the `implant.py` on the left.
1.  The attacker runs `whoami`, `ls /etc/`, and `uname -a`.
2.  The console encodes them locally into base64.
3.  The implant VM receives the tasks, executes them, and posts the results back.

![Final C2 Test](Screenshot%20(277).png)

---

### 5. C2 Channel (Tasking)
The Discord `#tasking` channel shows the raw `base64` payloads sent by the C2 server. This is the only traffic that would be seen by network monitoring, blending in as "Discord API traffic."

![Tasking Channel](Screenshot%202025-11-11%20141110.png)

---

### 6. C2 Channel (Results & Exfiltration)
The Discord `#results` channel shows the exfiltrated data sent back from the implant, including the directory listing of `/etc/` and the output of `uname -a`.

![Results Channel](Screenshot%202025-11-11%20141155.png)

---

*(This project is for educational and portfolio purposes only.)*
