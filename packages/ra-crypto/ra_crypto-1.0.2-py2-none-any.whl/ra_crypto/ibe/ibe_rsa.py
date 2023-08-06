import sys, os, json, codecs, io

sys.setrecursionlimit(5000)


def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcd(b % a, a)
		return (g, x - (b // a) * y, y)


def modinv(a, m):
	g, x, y = egcd(a, m)
	if g != 1:
		raise Exception('modular inverse does not exist')
	else:
		return x % m


def encrypt_using_rsa(message, recipient_public_key, public_param):
	message_int = int.from_bytes(message, byteorder="big")

	if recipient_public_key < 0:
		return pow(modinv(message_int, public_param), abs(recipient_public_key),
			public_param)

	return pow(message_int, recipient_public_key, public_param)


def decrypt_using_rsa(message, recipient_private_key, n):
	if recipient_private_key < 0:
		decrypted_message_int =  pow(
			modinv(message, n),
			abs(recipient_private_key),
			n)
	else:
		decrypted_message_int = pow(message, recipient_private_key, n)

	decrypted_message = decrypted_message_int.to_bytes(
		int(decrypted_message_int.bit_length() // 8) + 1, byteorder='big')

	return codecs.encode(decrypted_message, "hex")
