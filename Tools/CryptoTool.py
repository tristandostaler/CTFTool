from .CryptoToolkit import xor
from .CryptoToolkit import aes
from .CryptoToolkit import SubstitutionCipher
import enchant
from string import ascii_lowercase
import itertools
import re
try:
    from string import maketrans
except ImportError:
    maketrans = str.maketrans


def xor_with_fixed_length(s1, s2, keys_are_string_hex=True):
    assert (len(s1) == len(s2))
    if not keys_are_string_hex:
        s1 = s1.encode("utf-8").hex()
        s2 = s2.encode("utf-8").hex()
    b1 = bytes.fromhex(s1)
    b2 = bytes.fromhex(s2)
    xored = xor.xor_bytes(b1, b2)
    return xored


def break_single_byte_xor(cipher, cipher_is_string_hex=True):
    if not cipher_is_string_hex:
        cipher = cipher.encode("utf-8").hex()
    cipher = bytes.fromhex(cipher)
    key_found = xor.break_xor_char_key(cipher)
    message = xor.xor_single_char_key(cipher, key_found).decode('ascii')
    return message, key_found


def xor_repeating_key(message, key_received, message_and_key_is_string_hex=True):
    if not message_and_key_is_string_hex:
        message = message.encode("utf-8").hex()
        key_received = key_received.encode("utf-8").hex()
    message = message.encode('ascii')
    key_received = key_received.encode('ascii')
    xored = xor_repeating_key(message, key_received)
    return xored


def break_repeating_key_xor(cipher, cipher_is_string_hex=True):
    if not cipher_is_string_hex:
        cipher = cipher.encode("utf-8").hex()
    cipher = bytes.fromhex(cipher)
    key_len = xor.guess_key_lengths(cipher)
    key_found = xor.break_xor_repeating_key(cipher, key_len)
    decrypted = xor_repeating_key(cipher, key_found)
    message = decrypted.decode('ascii')
    return message


def aes_in_ecb_mode_decrypt(message, key_received, message_and_key_is_string_hex=True):
    if not message_and_key_is_string_hex:
        message = message.encode("utf-8").hex()
        key_received = key_received.encode("utf-8").hex()
    decryption_suite = aes.AES.new(key_received, aes.AES.MODE_ECB)
    msg_dec = decryption_suite.decrypt(message).decode('utf-8')
    return msg_dec


def cesar_encrypt(message, key):
    plaintext = ''
    for each in message:
        p = (ord(each) + key) % 126
        if p < 32:
            p += 95
        plaintext += chr(p)
    return plaintext


def cesar_decrypt(message, key):
    plaintext = ''
    for each in message:
        p = (ord(each) - key) % 126
        if p < 32:
            p += 95
        plaintext += chr(p)
    return plaintext


def break_letter_swapping(message):
    list_of_letters = []
    list_of_words = []
    d = enchant.Dict("en-US")
    for each in message.lower():
        if each in ascii_lowercase:
            list_of_letters.append(each)
    all_combinations = itertools.permutations(list_of_letters)
    for comb in all_combinations:
        new_message = ''.join(comb)
        word_counter = 0
        for i in range(0, len(new_message)):
            if d.check(new_message[word_counter:i+2]):
                list_of_words.append(new_message[word_counter:i+2])
                word_counter = i+2
    return list_of_words


def break_substitution_cipher(message, verbosity=0, modulo_level_to_print_verbosity_1=5,
                              max_len_word=SubstitutionCipher.WordList.MAX_WORD_LENGTH_TO_CACHE,
                              max_bad_words_rate=SubstitutionCipher.MAX_BAD_WORDS_RATE):
    enc_text = message.lower()
    enc_words = re.findall(r"[a-z']+", enc_text)

    # skip the words with apostrophs
    enc_words = [word for word in enc_words
                      if "'" not in word and
                         len(word) <= max_len_word
                ]
    enc_words = enc_words[:200]

    print("Loaded %d words in message, loading dicts" % len(enc_words))

    keys = SubstitutionCipher.KeyFinder(enc_words, max_len_word, max_bad_words_rate).find(verbosity, modulo_level_to_print_verbosity_1)
    if not keys:
        print("Key not founded, try to increase MAX_BAD_WORDS_RATE")
        return
    for key, bad_words in keys.items():
        print("Possible key: %s, bad words:%d" % (key, bad_words))
    best_key = min(keys, key=keys.get)
    print("Best key: %s, bad_words %d" % (best_key, keys[best_key]))
    trans = maketrans(SubstitutionCipher.ABC, best_key)
    decrypted = message.translate(trans)
    print(decrypted)