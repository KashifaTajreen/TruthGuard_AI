# prompt_detector.py
import re

def detect_prompt_injection(prompt):
    p = prompt.lower()
    
    # Advanced patterns used by hackers
    threat_patterns = {
        r"ignore (all|previous|said) instructions": "Instruction Bypass",
        r"(reveal|show) (system|hidden) prompt": "Data Extraction",
        r"api key": "Credential Theft",
        r"act as": "Roleplay Attack",
        r"jailbreak": "Safety Override"
    }
    
    for pattern, label in threat_patterns.items():
        if re.search(pattern, p):
            return True, label
            
    return False, None
# import re

# dangerous_patterns = [
#     r"ignore (all|previous) instructions",
#     r"system prompt",
#     r"as a (dev|developer|admin)",
#     r"reveal secret",
#     r"bypass",
#     r"jailbreak",
#     r"sql injection",
#     r"<script>",
#     r"decode this base64"
# ]

# def detect_prompt_injection(prompt):
#      p = prompt.lower()
#     # Check for keywords even if words are between them
#     if "ignore" in p and "instruction" in p:
#         return True, "Instruction Override Attempt"
#     if "secret" in p or "system prompt" in p:
#         return True, "Data Leak Attempt"
#     return False, None
    # for pattern in dangerous_patterns:
    #     if re.search(pattern, prompt, re.IGNORECASE):
    #         return True, pattern
    # return False, None
# import re
# dangerous_patterns = [
#      r"ignore previous instructions",
#      r"reveal system prompt",
#      r"show hidden instructions",
#      r"give me api key",
#      r"bypass safety",
#      r"pretend you are not an ai",
#     r"jailbreak",
#     r"act as system",
#     r"reveal hidden prompt"
# ]

# def detect_prompt_injection(prompt):
#     prompt_lower = prompt.lower()

#     for pattern in dangerous_patterns:
#         if pattern in prompt_lower:
#             return True, pattern

#     return False, None
