# -*- encoding: utf-8 -*-
"""
Modified for GRID, 2021

Copyright (c) 2019 - present AppSeed.us
"""
 
import hashlib, binascii, os

# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/

def hash_pass( password ):
    """Hash mot de passe SHA-256"""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash) # return bytes

def verify_pass(provided_password, stored_password):
    """Verification du mot de passe par Hash"""
    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

