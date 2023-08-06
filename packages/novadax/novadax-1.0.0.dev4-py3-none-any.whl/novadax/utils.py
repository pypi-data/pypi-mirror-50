import hmac
import hashlib
import base64

def hmac_sha1_hex(key, text):
    return hmac.new(bytes(key, 'UTF-8'), bytes(text, 'UTF-8'), hashlib.sha1).hexdigest()

def md5_base64(text):
    obj = hashlib.md5()
    obj.update(bytes(text, 'UTF-8'))
    return base64.b64encode(obj.digest()).decode('ascii')
