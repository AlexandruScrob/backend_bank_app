import string
from secrets import SystemRandom


rand = SystemRandom()


def generate_wallet_id() -> str:
    return "".join(rand.choice(string.ascii_lowercase) for _ in range(10))
