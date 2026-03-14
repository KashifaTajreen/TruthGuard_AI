# prompt_detector.py
import re

def detect_prompt_injection(prompt):

    p = prompt.lower()

    threats = [

        # Prompt Injection
        (r"(ignore|forget|disregard|override).*(instruction|rule|system|prompt)", "Instruction Bypass"),
        (r"(reveal|show|display).*(system prompt|hidden prompt|internal instruction)", "System Prompt Leak"),
        (r"(act as|pretend to be|you are now)", "Persona Hijack"),
        (r"(jailbreak|dan mode|developer mode)", "Safety Override"),

        # Hacking / Security Misuse
        (r"(hack|hacking|exploit|breach).*(system|server|database)", "Hacking Attempt"),
        (r"(bypass|break).*(security|authentication|firewall)", "Security Bypass Attempt"),
        (r"(steal|extract).*(data|password|credentials)", "Data Theft Attempt"),
        (r"(malware|ransomware|virus)", "Malware Intent"),
        (r"(ddos|botnet|attack).*(server|network)", "Cyber Attack Intent"),

    ]

    for pattern, label in threats:

        if re.search(pattern, p):

            return True, label

    return False, None
# import re

# def detect_prompt_injection(prompt):
#     p = prompt.lower()
#     # Advanced patterns to catch "Forget instructions" or "Act as" attacks
#     threats = [
#         (r"(forget|ignore|disregard|override).*(instruction|previous|rule|system|prompt)", "Instruction Bypass"),
#         (r"(reveal|show|what is).*(system|internal|hidden).*(prompt|instruction)", "System Leak"),
#         (r"act as|you are now|pretend to be", "Persona Hijacking"),
#         (r"dan mode|jailbreak|unlock", "Safety Override")
#     ]
    
#     for pattern, label in threats:
#         if re.search(pattern, p):
#             return True, label
#     return False, None
