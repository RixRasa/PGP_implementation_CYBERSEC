import hashlib

def sha1_hash(message):
    # Create a SHA-1 hash object
    sha1 = hashlib.sha1()

    # Convert the message to bytes and update the hash object
    sha1.update(message.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hashed_message = sha1.hexdigest()

    return hashed_message


def truncate_hash(hash_value, desired_length):
    # Convert the hash value to bytes
    hash_bytes = bytes.fromhex(hash_value)

    # Truncate the hash value to the desired length
    truncated_bytes = hash_bytes[:desired_length // 8]

    # Convert the truncated bytes back to a hexadecimal string
    return truncated_bytes