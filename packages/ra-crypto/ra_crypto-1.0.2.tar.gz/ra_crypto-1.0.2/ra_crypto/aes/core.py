import os, codecs, io

import pyaes


def generate_aes_key(n=32):
	return os.urandom(n)


def encrypt_file_using_aes_as_stream(plain_text_file_bytes, key):
	counter = pyaes.Counter(initial_value=5)
	aes = pyaes.AESModeOfOperationCTR(key, counter)
	return aes.encrypt(plain_text_file_bytes)


def decrypt_file_using_aes_as_stream(encrypted_file_bytes, key):
	counter = pyaes.Counter(initial_value=5)
	aes = pyaes.AESModeOfOperationCTR(key, counter)
	return aes.decrypt(encrypted_file_bytes)
