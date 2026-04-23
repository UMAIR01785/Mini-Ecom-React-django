from django.contrib.auth.hashers import PBKDF2PasswordHasher

class FastHasher(PBKDF2PasswordHasher):
    iterations= 180000