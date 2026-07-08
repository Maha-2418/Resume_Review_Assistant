import re

def clean_text(text):
    replacements = {
        "": "",
        "ï": "",
        "§": "",
        "•": "-",
        "\xa0": " "
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()