import bcrypt

def hash_password(password):
    # Hash a password for the first time, with a randomly-generated salt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, password):
    # Check a hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)