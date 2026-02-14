import hashlib
from typing import Any, Optional


def hash_sha256(value: Any, salt: str = "default_salt") -> Optional[str]:
    """
    Hashes a value using a salted SHA256 hash.

    Args:
        value: The value to hash.
        salt: The salt string to use for hashing.

    Returns:
        The hexadecimal digest of the salted hash,
        or None if the input is None.
    """
    if value is None:
        return None

    # distinct separator to prevent collision attacks
    # (e.g. "salt" + "val" vs "sal" + "tval")
    # strictly speaking not critical for this simple use case but good practice
    salted_input = f"{salt}|{str(value)}".encode("utf-8")
    return hashlib.sha256(salted_input).hexdigest()


# Aliases for different semantic uses of the same underlying primitive
mask_value = hash_sha256
pseudonymize_value = hash_sha256
