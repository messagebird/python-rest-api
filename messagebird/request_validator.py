import hashlib
import hmac

import jwt

from messagebird.error import ValidationError


class RequestValidator:
    ALLOWED_ALGOS = ["HS256", "HS384", "HS512"]

    def __init__(self, signature_key):
        super().__init__()
        self.signature_key = signature_key

    def __str__(self) -> str:
        return super().__str__()

    def validate_signature(self, signature, url, request_body):
        try:
            decoded = jwt.decode(
                jwt=signature,
                key=self.signature_key,
                algorithms=RequestValidator.ALLOWED_ALGOS,
                options={
                    "require": ["iss", "nbf", "exp", "url_hash"],
                    "verify_iat": False,
                },
                issuer="MessageBird",
                leeway=1
            )
        except jwt.InvalidTokenError as err:
            raise ValidationError(str(err)) from err

        expected_url_hash = hashlib.sha256(url.encode("latin-1")).hexdigest()
        if not hmac.compare_digest(expected_url_hash, decoded["url_hash"]):
            raise ValidationError("invalid jwt: claim url_hash is invalid")

        payload_hash = decoded.get("payload_hash")
        if not request_body and payload_hash:
            raise ValidationError("invalid jwt: claim payload_hash is set but actual payload is missing")
        elif request_body and not payload_hash:
            raise ValidationError("invalid jwt: claim payload_hash is not set but payload is present")
        elif request_body and not hmac.compare_digest(hashlib.sha256(request_body.encode("latin-1")).hexdigest(),
                                                      payload_hash):
            raise ValidationError("invalid jwt: claim payload_hash is invalid")

        return decoded
