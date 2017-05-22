import base64
import binascii
import itertools
from Crypto.Util.strxor import strxor_c

#x = b'this is a test'
#y = b'wokka wokka!!!'
#expectedD = 37
#d = getHammingDistance(x, y)
#if d != expectedD:
#    raise Exception(encodedD + ' != ' + encodedExpectedD)

# From http://www.data-compression.com/english.html
freqs = {
    'a': 0.0651738,
    'b': 0.0124248,
    'c': 0.0217339,
    'd': 0.0349835,
    'e': 0.1041442,
    'f': 0.0197881,
    'g': 0.0158610,
    'h': 0.0492888,
    'i': 0.0558094,
    'j': 0.0009033,
    'k': 0.0050529,
    'l': 0.0331490,
    'm': 0.0202124,
    'n': 0.0564513,
    'o': 0.0596302,
    'p': 0.0137645,
    'q': 0.0008606,
    'r': 0.0497563,
    's': 0.0515760,
    't': 0.0729357,
    'u': 0.0225134,
    'v': 0.0082903,
    'w': 0.0171272,
    'x': 0.0013692,
    'y': 0.0145984,
    'z': 0.0007836,
    ' ': 0.1918182 
}

def getHammingDistance(x, y):
    #print('Y: ' + str(y) + " lenX: " + str(len(x)) + " lenY: " + str(len(y)))
    #min(len(x),len(y))
    if len(y) < len(x):
        return 0
    return sum([bin(x[i] ^ y[i]).count('1') for i in range(len(x))])

def score(s):
    score = 0
    for i in s:
        c = chr(i).lower()
        if c in freqs:
            score += freqs[c]
    return score

def breakSingleByteXOR(s):
    def key(p):
        return score(p[1])
    return max([(i, strxor_c(s, i)) for i in range(0, 256)], key=key)

def encodeRepeatingKeyXor(s, key):
    return bytes([s[i] ^ key[i % len(key)] for i in range(len(s))])

def breakRepeatingKeyXor(x, k):
    blocks = [x[i:i+k] for i in range(0, len(x), k)]
    transposedBlocks = list(itertools.zip_longest(*blocks, fillvalue=0))
    key = [breakSingleByteXOR(bytes(x))[0] for x in transposedBlocks]
    return bytes(key)

def normalizedEditDistance(x, k):
    #print("X: " + str(x) + " K:" + str(k))
    blocks = [x[i:i+k] for i in range(0, len(x), k)][0:4]
    #print("blocks: " + str(blocks))
    pairs = list(itertools.combinations(blocks, 2))
    #print("pairs: " + str(pairs))
    scores = [getHammingDistance(p[0], p[1])/float(k) for p in pairs][0:6]
    return sum(scores) / len(scores)

def brute_force_multi_char_xor(base64_payload):
    x = base64.b64decode(base64_payload)

    k = min(range(2, 41), key=lambda k: normalizedEditDistance(x, k))

    key = breakRepeatingKeyXor(x, k)
    y = encodeRepeatingKeyXor(x, key)
    
    print(key, y)
