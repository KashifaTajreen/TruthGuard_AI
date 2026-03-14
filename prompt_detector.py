# prompt_detector.py
import re

def detect_prompt_injection(prompt):
    p = prompt.lower()
    # Advanced patterns to catch "Forget instructions" or "Act as" attacks
    threats = [
        (r"(forget|ignore|disregard|override).*(instruction|previous|rule|system|prompt)", "Instruction Bypass"),
        (r"(reveal|show|what is).*(system|internal|hidden).*(prompt|instruction)", "System Leak"),
        (r"act as|you are now|pretend to be", "Persona Hijacking"),
        (r"dan mode|jailbreak|unlock", "Safety Override")
    ]
    
    for pattern, label in threats:
        if re.search(pattern, p):
            return True, label
    return False, None
