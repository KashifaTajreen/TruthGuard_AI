# prompt_detector.py
import re
dangerous_patterns = [
     r"ignore previous instructions",
     r"reveal system prompt",
     r"show hidden instructions",
     r"give me api key",
     r"bypass safety",
     r"pretend you are not an ai",
    r"jailbreak",
    r"act as system",
    r"reveal hidden prompt"
]

def detect_prompt_injection(prompt):
    prompt_lower = prompt.lower()

    for pattern in dangerous_patterns:
        if pattern in prompt_lower:
            return True, pattern

    return False, None
