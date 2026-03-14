# prompt_detector.py
import re

def detect_prompt_injection(prompt):

    p = prompt.lower()

    hacking_words = ["hack","hacking","exploit","breach","attack"]
    security_words = ["security","system","server","database","api","api key","token"]
    bypass_words = ["bypass","disable","break","crack"]
    steal_words = ["steal","extract","leak","dump"]

    patterns = [
        (r"(ignore|forget|override).*(instruction|system|prompt)", "Instruction Bypass"),
        (r"(reveal|show).*(system prompt|hidden prompt)", "System Prompt Leak"),
        (r"(act as|pretend to be|you are now)", "Persona Hijack"),
        (r"(jailbreak|dan mode|developer mode)", "Safety Override")
    ]

    for pattern,label in patterns:
        if re.search(pattern,p):
            return True,label

    if any(w in p for w in hacking_words) and any(s in p for s in security_words):
        return True,"System Hacking Attempt"

    if any(w in p for w in bypass_words) and "security" in p:
        return True,"Security Bypass Attempt"

    if any(w in p for w in steal_words) and any(s in p for s in security_words):
        return True,"Credential Theft Attempt"

    return False,None
# import re

# def detect_prompt_injection(prompt):

#     p = prompt.lower()

#     threats = [

#         # Prompt Injection
#         (r"(ignore|forget|disregard|override).*(instruction|rule|system|prompt)", "Instruction Bypass"),
#         (r"(reveal|show|display).*(system prompt|hidden prompt|internal instruction)", "System Prompt Leak"),
#         (r"(act as|pretend to be|you are now)", "Persona Hijack"),
#         (r"(jailbreak|dan mode|developer mode)", "Safety Override"),

#         # Hacking / Security Misuse
#         (r"(hack|hacking|exploit|breach).*(system|server|database)", "Hacking Attempt"),
#         (r"(bypass|break).*(security|authentication|firewall)", "Security Bypass Attempt"),
#         (r"(steal|extract).*(data|password|credentials)", "Data Theft Attempt"),
#         (r"(malware|ransomware|virus)", "Malware Intent"),
#         (r"(ddos|botnet|attack).*(server|network)", "Cyber Attack Intent"),

#     ]

#     for pattern, label in threats:

#         if re.search(pattern, p):

#             return True, label

#     return False, None
