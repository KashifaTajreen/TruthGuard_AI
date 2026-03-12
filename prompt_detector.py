# prompt_detector.py

dangerous_patterns = [
    "ignore previous instructions",
    "reveal system prompt",
    "show hidden instructions",
    "give me api key",
    "bypass safety",
    "pretend you are not an ai",
    "jailbreak",
]

def detect_prompt_injection(prompt):
    prompt_lower = prompt.lower()

    for pattern in dangerous_patterns:
        if pattern in prompt_lower:
            return True, pattern

    return False, None
