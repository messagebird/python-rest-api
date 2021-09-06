import hashlib
import hmac
import jwt

from typing import Union, Dict
from messagebird.error import ValidationError


class RequestValidator:
    """
    RequestValidator validates request signature signed by MessageBird services.

    See https://developers.messagebird.com/docs/verify-http-requests
    """

    ALLOWED_ALGOS = ["HS256", "HS384", "HS512"]

    def __init__(self, signature_key: str, skip_url_validation: bool = False):
        """
        :param signature_key: customer signature key. Can be retrieved through
        <a href="https://dashboard.messagebird.com/developers/settings">Developer Settings</a>. This is NOT your API key.
        :param skip_url_validation: whether url_hash claim validation should be skipped.
        Note that when true, no query parameters should be trusted.
        """
        super().__init__()
        self._signature_key = signature_key
        self._skip_url_validation = skip_url_validation

    def __str__(self) -> str:
        return super().__str__()

    def validate_signature(self, signature: str, url: str, request_body: Union[bytes, bytearray]) -> Dict[str, str]:
        """
        This method validates provided request signature, which is a JWT token.
        This JWT is signed with a MessageBird account unique secret key, ensuring the request is from MessageBird and
        a specific account.

        The JWT contains the following claims:

        *   "url_hash" - the raw URL hashed with SHA256 ensuring the URL wasn't altered.
        *   "payload_hash" - the raw payload hashed with SHA256 ensuring the payload wasn't altered.
        *    "jti" - a unique token ID to implement an optional non-replay check (NOT validated by default).
        *    "nbf" - the not before timestamp.
        *    "exp" - the expiration timestamp is ensuring that a request isn't captured and used at a later time.
        *    "iss" - the issuer name, always MessageBird.

        :param signature: the actual signature taken from request header "MessageBird-Signature-JWT".
        :param url: the raw url including the protocol, hostname and query string, e.g. "https://example.com/?example=42".
        :param request_body: the raw request body.
        :returns: raw signature payload.
        :raises: ValidationError if signature is invalid.
        """
        if not signature:
            raise ValidationError("Signature is empty")
        if not self._skip_url_validation and not url:
            raise ValidationError("URL is empty")

        try:
            claims = jwt.decode(
                jwt=signature,
                key=self._signature_key,
                algorithms=RequestValidator.ALLOWED_ALGOS,
                options={
                    "require": ["iss", "nbf", "exp"],
                    "verify_iat": False,
                },
                issuer="MessageBird",
                leeway=1
            )
        except jwt.InvalidTokenError as err:
            raise ValidationError(str(err)) from err

        if not self._skip_url_validation:
            expected_url_hash = hashlib.sha256(url.encode("utf-8")).hexdigest()
            if not hmac.compare_digest(expected_url_hash, claims["url_hash"]):
                raise ValidationError("invalid jwt: claim url_hash is invalid")

        payload_hash = claims.get("payload_hash")
        if not request_body and payload_hash:
            raise ValidationError("invalid jwt: claim payload_hash is set but actual payload is missing")
        if request_body and not payload_hash:
            raise ValidationError("invalid jwt: claim payload_hash is not set but payload is present")
        if request_body and not hmac.compare_digest(hashlib.sha256(request_body).hexdigest(), payload_hash):
            raise ValidationError("invalid jwt: claim payload_hash is invalid")

        return claims
