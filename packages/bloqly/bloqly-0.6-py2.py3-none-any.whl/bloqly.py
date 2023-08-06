"""Bloqly API"""

__version__ = '0.6'

import hashlib

import nacl.signing
from nacl.encoding import Base64Encoder, Base16Encoder


def encode64(value):
    return Base64Encoder.encode(value).decode('utf-8')


def encode16(value):
    return Base16Encoder.encode(value).decode('utf-8')


def sign_transaction(private_key, space, key, nonce, timestamp, value, memo='', tags=None):
    if tags is None:
        tags = []

    signing_key = nacl.signing.SigningKey(private_key, encoder=Base64Encoder)

    tags_bytes = bytearray("", encoding='utf8')
    tags.sort()

    for tag in tags:
        tags_bytes.extend(bytes(tag, encoding='utf8'))

    data = \
        space.encode('utf-8') + \
        key.encode('utf-8') + \
        nonce.to_bytes(8, 'big', signed=False) + \
        timestamp.to_bytes(8, 'big', signed=False) + \
        memo.encode('utf-8') + \
        tags_bytes + \
        value.encode('utf-8')

    m = hashlib.sha256()
    m.update(data)
    tx_hash = m.digest()

    signed_message = signing_key.sign(tx_hash, encoder=Base64Encoder)

    signature = signed_message.signature.decode('utf-8')

    verify_key = signing_key.verify_key

    public_key = encode64(bytes(verify_key))

    signed_transaction = {
        'space': space,
        'key': key,
        'nonce': nonce,
        'timestamp': timestamp,
        'tags': tags,
        'memo': memo,
        'value': value,
        'hash': encode16(tx_hash),
        'signature': signature,
        'public_key': public_key
    }

    return signed_transaction


def encode_transaction(signed_transaction):
    tx_json = str(signed_transaction).replace('\'', '"').encode('utf-8')

    tx_bytes = bytes(tx_json)

    encoded_transaction = encode64(tx_bytes)

    return encoded_transaction
