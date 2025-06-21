import hashlib

def encrypt_data(password): 
    return hashlib.md5(password.encode('utf-8')).hexdigest()
