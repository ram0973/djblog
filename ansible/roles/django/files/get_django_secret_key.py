#!/bin/bash

import random
import string
KEY_LENGTH = 50
allowed_chars = string.ascii_letters+string.digits
secret_key = ''.join(random.choice(allowed_chars) for _ in range(KEY_LENGTH))
print(secret_key)
