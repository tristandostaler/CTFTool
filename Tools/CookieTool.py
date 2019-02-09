from hashlib import sha512, sha1
from flask.sessions import session_json_serializer
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature
from itsdangerous import base64_decode
import base64
import zlib
import json

def decode_cookie_payload(payload, return_as_dic=False):
    """Decode a Flask cookie."""
    """ 
        https://www.kirsle.net/wizards/flask-session.cgi
        .eJwlj0FuwzAMBP-icw4iJdFiPmNQ5BINArSAnZyK_j0Get_BzP6WPQ-cX-X-Ot64lf0R5V5s1sEBClFMY-qWvACMJFelBKp6o1hWVRJC050Cm4oNSCNp2aXpUIfVMbeexKjcPRKrL2dJulYDxDW56aVL1RgZQtUqlVvx88j99fPE99UTGTxyTYQsUV5kdeNltnX22cJ1CNs2-eLeJ47_E9LL3wdmwz_i.DbwCXg.HQ1RqyWO8SVCgiL5zC-weeD3AjkdGVWTpXSl_PUyC4nnK7kvKrzX6uv1pwxWzx6VaukHjzb5Dkf8vTo3yNmHEA
        .eJwljztqRDEMAO_iegvJ-tl7mYdsSSQEEnhvtwq5ezakmmpg5rsddeb11u6P85m3drxHu7fSZEfUATiD0JaRhO9ZQ0BpRPbenZdgKRRmcqmWJW-DyShiY3SqaZmqLIuHL8e-BQd1Wp5jv2hrE0lVVKJO3o4gSqG-Zru1fZ11PL4-8vOvx8EhhHzB8B5ppZSTKzqLdiuEMgDfL-955fk_we3nF1IVPrU.Dz_anQ.STkX9fcYNgrAKg7um1wtSHYiGoA
    """
    try:
        compressed = False

        if payload.startswith('.'):
            compressed = True
            payload = payload[1:]

        data = payload.split(".")[0]

        data = base64_decode(data)
        if compressed:
            data = zlib.decompress(data)

        if return_as_dic:
            return json.loads(data.decode("utf-8"))
        else:
            return data.decode("utf-8")
    except Exception as e:
        return "[Decoding error: are you sure this was a Flask session cookie? {}]".format(e)

def encode_cookie_payload(payload_dict, secret_key):
    signer = URLSafeTimedSerializer(
        secret_key, salt='cookie-session',
        serializer=session_json_serializer,
        signer_kwargs={'key_derivation': 'hmac', 'digest_method': sha1}
    )
    gen_payload = signer.dumps(payload_dict)
    return gen_payload
