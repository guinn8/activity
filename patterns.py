import re

patterns_tags = [
    (re.compile(r"(wedding|bride|groom|marriage|nuptial|planning)", re.IGNORECASE), "Wedding Planning"),
    (re.compile(r"(rustic|venue|events|photographer|jewelry|bands)", re.IGNORECASE), "Wedding Planning"),
    (re.compile(r"(computer|technology|hardware|desktop|gaming|graphics cards|processors|cooling|motherboards|ssd|hdd)", re.IGNORECASE), "Computer Hardware and Technology"),
    (re.compile(r"(online|browsing|internet|web|email)", re.IGNORECASE), "Online Activities and Browsing"),
    (re.compile(r"(facilities|services|library|weather|inbox)", re.IGNORECASE), "Miscellaneous")
]
