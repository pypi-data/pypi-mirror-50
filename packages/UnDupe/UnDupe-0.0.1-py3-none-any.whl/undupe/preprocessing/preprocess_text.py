import re

# REGULAR EXPRESSIONS

# -----------------------------EMAILS------------------------------------------
# All non-whitespace characters before and after @ sign
EMAIL_REGEX = r"\S*@\S*"

# --------------------------HYPERLINKS-----------------------------------------
HYPERLINK_REGEXS = {
    # http://www.abc123.abc123/folder/subfolder
    # https://www.abc123.abc123/
    "HYPERLINK_REGEX1": r"(http|https)\:\/\/www.\w+.\w+\/\S*\/\S*",

    # http://www.abc123.abc123.abc123/folder/subfolder
    # https://www.abc123.abc123.abc123/
    "HYPERLINK_REGEX2": r"(http|https)\:\/\/www.\w+.\w+.\w+\/\S*\/\S*",

    # http://www.abc123.abc123/folder
    # https://www.abc123.abc123/
    "HYPERLINK_REGEX3": r"(http|https)\:\/\/www.\w+.\w+\/\S*",

    # http://www.abc123.abc123.abc123
    "HYPERLINK_REGEX4": r"(http|https)\:\/\/\w+.\w+.\w+",

    # www.website.com
    "HYPERLINK_REGEX5": r"www.\S*.com",

    # facebook.com/folder
    "FACEBOOK_REGEX": r"facebook.com/\S*"
}

# ----------------------------CHAINS-------------------------------------------
# Chains of hyphens, equal to, dots, underscores
CHAINS = {
    "HYPHEN_REGEX": r"(-)(-)+",
    "EQUALS_REGEX": r"(=)+",
    "UNDERSCORE_REGEX": r"(_)+",
    "DOT_REGEX": r"(\.)(\.)+"
}

# --------------------------PHONE NUMBERS--------------------------------------
PHONE_REGEXS = {
    # (XXX) XXX - XXXXX (whitespace variations)
    "PHONE_REGEX1": r"\(\d{3}\)(\s*\d{3}|\d{3})\s*(-)*(\s*\d{4}|\d{4})",
    # (XXX) XXX-XXXXX
    "PHONE_REGEX2": r"\(\d{3}\)\d{3}-\d{4}",
    # (XXX)-XXX-XXXX
    "PHONE_REGEX3": r"\(\d{3}\)-\d{3}-\d{4}",
    # XXX-XXX-XXXX
    "PHONE_REGEX4": r"d{3}-\d{3}-\d{4}",
    # XXXXXXXXXX
    "PHONE_REGEX5": r"\d{10}",
    # XXX.XXX.XXXX
    "PHONE_REGEX6": r"\d{3}.\d{3}.\d{4}"
}

# -----------------------SPECIAL CHARS-----------------------------------------
SPL_CHARS_REGEXS = {
    "SPL_CHAR1": r"\[\w+ \w+\]",
    "SPL_CHAR2": r"[,;@\\#?|!+_*=~<>&$]",
    "SPL_CHAR3": r"[A-Za-z]+-[A-Za-z]+",
    "SPL_CHAR4": r"[/][A-Za-z]"
}


def remove_email_ids(text: str) -> str:
    """
    Remove email ids from the text using regex

    :param text:
    :return:
    """
    return re.sub(EMAIL_REGEX, ' ', text)


def remove_hyperlinks(text: str) -> str:
    """
    Remove all hyperlinks from the text using regex

    :param text:
    :return:
    """
    for regex in HYPERLINK_REGEXS.values():
        text = re.sub(regex, ' ', text)

    return text


def remove_chains(text: str) -> str:
    """
    Remove chains of hyphens, periods, underscores, and equal signs from the text using regex

    :param text:
    :return:
    """
    for regex in CHAINS.values():
        text = re.sub(regex, ' ', text)

    return text


def remove_phone_numbers(text: str) -> str:
    """
    Remove phone numbers of different formats from the text using regex

    :param text:
    :return:
    """
    for regex in PHONE_REGEXS.values():
        text = re.sub(regex, ' ', text)

    return text


def remove_special_chars(text: str) -> str:
    """
    Remove special characters from the text using regex

    :param text:
    :return:
    """
    for regex in SPL_CHARS_REGEXS.values():
        text = re.sub(regex, ' ', text)

    ind = re.search(SPL_CHARS_REGEXS["SPL_CHAR4"], text)
    while ind:
        text = list(text)
        text[ind.start()] = ' '

        text = "".join(text)
        ind = re.search(SPL_CHARS_REGEXS["SPL_CHAR4"], text)

    return text


def preprocess(text: str) -> str:
    """
    Preprocess the text text using regular expressions

    :param text:
    :return:
    """

    text = text.lower().strip()

    text = remove_email_ids(text)

    text = remove_hyperlinks(text)

    text = remove_chains(text)

    text = remove_phone_numbers(text)

    text = remove_special_chars(text)

    text = ' '.join(text.split())

    return text + '\n'
