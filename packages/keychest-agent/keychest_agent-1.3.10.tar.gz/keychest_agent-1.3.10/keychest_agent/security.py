#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***
Module:
***

 Copyright (C) Smart Arcs Ltd, registered in the United Kingdom.
 This file is owned exclusively by Smart Arcs Ltd.
 Unauthorized copying of this file, via any medium is strictly prohibited
 Proprietary and confidential
 Written by Dan Cvrcek <support@keychest.net>, 2019
"""
import base64
import hashlib
import hmac
import json
import time

from keychest_agent.logger import logger
from keychest_agent.pyaes.aespy import AESModeOfOperationCBC
from keychest_agent.pyaes.blockfeeder import Encrypter, Decrypter

__copyright__ = 'Smart Arcs Ltd'
__email__ = 'support@keychest.net'
__status__ = 'Development'


class Security(object):
    """
    A simple static class to secure and "unsecure" JSON data
    """

    @classmethod
    def secure(cls, data, key):
        """
        It takes a JSON structure, searches for "payload", encrypts it and adds a new
        item "signature" and "iv", which is HMAC of the encrypted data.
        1. check the data
        2. encryption
        3. encrypted string is base64-d
        4. HMAC
        5. HJMAC is based64
        :param data:
        :param key
        :return:
        """
        data_key = None
        # check the data
        try:
            if 'payload' in data:
                _plaintextdata = json.dumps(data['payload']).encode()
                data_key = 'payload'
            else:
                _plaintextdata = json.dumps(data['data']).encode()
                data_key = 'data'
            _ = json.loads(_plaintextdata)
        except Exception as ex:
            logger.error("Error checking data for encryption", cause=str(ex))
            return None
        else:
            try:
                # create diversified keys
                raw_key_enc = "ENC" + key
                raw_key_mac = "MAC" + key
                _hash = hashlib.sha256()
                _hash.update(raw_key_enc.encode())
                key_enc = _hash.digest()[:16]

                _hash = hashlib.sha256()
                _hash.update(raw_key_mac.encode())
                key_mac = _hash.digest()[:16]

                # prepare IV - from timestamp
                _hash = hashlib.sha256()
                raw_iv = "%f" % time.time()
                _hash.update(raw_iv.encode())
                iv = _hash.digest()[:16]

                # create an encryptor and encrypt the data
                aes = Encrypter(AESModeOfOperationCBC(key_enc, iv=iv))
                encrypted = aes.feed(_plaintextdata)
                encrypted += aes.feed()
                data_out = base64.b64encode(encrypted)

                # HMAC of the encrypted data
                _hmac = hmac.new(key_mac, data_out, hashlib.sha256)
                _hmaced = _hmac.digest()
                signature_out = base64.b64encode(_hmaced)

                # and prepare the output
                iv_out = base64.b64encode(iv).decode()
                data[data_key] = data_out.decode()
                data['signature'] = {'iv': iv_out, 'hmac': signature_out.decode()}

                return data
            except Exception as ex:
                logger.error("Exception when encrypting data", cause=str(ex))
                return None

    @classmethod
    def extract(cls, data, key):
        """
        It takes a JSON structure and searches for "data" and "signature" if either is not
        found, nothing happens and it returns data intact. If both exist
        1. de-base64 signature
        2. verifies the signature = HMAC
        3. base64 decode of data
        4. data decryption
        :param data:
        :param key:
        :return:
        """

        # check the data
        data_key = None
        try:
            if 'payload' in data:
                _encrypted_data = data['payload']
                data_key = 'payload'
            else:
                _encrypted_data = data['data']
                data_key = 'data'
        except Exception as ex:
            logger.info("Error checking data for decryption", cause=str(ex))
            return None
        else:

            if ('signature' not in data) or (not isinstance(data['signature'],dict)) \
                    or ('iv' not in data['signature']) or ('hmac' not in data['signature']):
                logger.info("Data not encrypted or the signature is missing")
                return data

            try:
                # create diversified keys
                raw_key_enc = "ENC" + key
                raw_key_mac = "MAC" + key
                _hash = hashlib.sha256()
                _hash.update(raw_key_enc.encode())
                key_enc = _hash.digest()[:16]

                _hash = hashlib.sha256()
                _hash.update(raw_key_mac.encode())
                key_mac = _hash.digest()[:16]

                # HMAC of the encrypted data
                data_in = _encrypted_data.strip().encode()  # type: str
                _hmac = hmac.new(key_mac, data_in, hashlib.sha256)
                _hmaced = _hmac.digest()
                local_signature = base64.b64encode(_hmaced).decode()
                msg_signature = data['signature']['hmac']

                # exit if the HMAC is incorrect
                if local_signature != msg_signature:
                    logger.info("Message signature is invalid")
                    return None

                # get the IV from the message
                raw_iv = data['signature']['iv']
                iv = base64.b64decode(raw_iv.encode())

                _encrypted_data = base64.b64decode(data_in)
                # create an encryptor and encrypt the data
                aes = Decrypter(AESModeOfOperationCBC(key_enc, iv=iv))
                data_out = aes.feed(_encrypted_data)
                data_out += aes.feed()  # type: bytes

                data[data_key] = json.loads(data_out.decode())
                data['signature'] = None

                return data
            except Exception as ex:
                logger.error("Exception when decrypting data", cause=str(ex))
                return None
