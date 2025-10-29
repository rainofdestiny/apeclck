import re
import secrets
import string


URL_RE = re.compile(
    r"^(https?://)"
    r"(([A-Za-z0-9\-]+\.)+[A-Za-z]{2,}|localhost)(:\d+)?"
    r"(/[^\s]*)?$",
    re.IGNORECASE,
)


def is_url(text: str) -> bool:
    return bool(URL_RE.match(text.strip()))


def random_code(length: int = 6) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))
