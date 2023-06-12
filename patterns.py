import re

patterns_tags = [
    (re.compile(r"\b(computer|desktop|gaming|MSI|Lenovo|Acer|Asus|memory express|clearance|AMD|PassMark|GeForce|RTX|Vancouver|power supplies)\b", re.IGNORECASE), "COMPUTER HARDWARE AND TECHNOLOGY"),
    (re.compile(r"\b(library|weather|inbox|email)\b", re.IGNORECASE), "MISCELLANEOUS"),
    (re.compile(r"\b(wedding|bride|groom|marriage|planning|rustic|venue|events|photographer|jewelry|bands|DJ|photography|cake)\b", re.IGNORECASE), "WEDDING PLANNING")
]
