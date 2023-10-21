import json
from ast import literal_eval

from flask.sessions import SessionInterface, SecureCookieSession, SessionMixin
from itsdangerous import base64_decode, base64_encode, BadSignature


class InsecureSession(SessionInterface):
    """The default session interface that stores sessions in signed cookies
    through the :mod:`itsdangerous` module.
    """

    #: the salt that should be applied on top of the secret key for the
    #: signing of cookie based sessions.
    salt = "cookie-session"
    #: the hash function to use for the signature.  The default is sha1
    #: the name of the itsdangerous supported key derivation.  The default
    #: is hmac.
    key_derivation = "hmac"
    #: A python serializer for the payload.  The default is a compact
    #: JSON derived serializer with support for some extra Python types
    #: such as datetime objects or tuples.
    session_class = SecureCookieSession

    def open_session(self, app: "Flask", request: "Request"):

        val = request.cookies.get(self.get_cookie_name(app))
        if not val:
            return self.session_class()
        # max_age = int(app.permanent_session_lifetime.total_seconds())
        try:
            plain = base64_decode(val)
            data = json.loads(plain)
            return self.session_class(data)
        except BadSignature:
            return self.session_class()

    def save_session(
            self, app: "Flask", session: SessionMixin, response: "Response"
    ) -> None:
        name = self.get_cookie_name(app)
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        secure = self.get_cookie_secure(app)
        samesite = self.get_cookie_samesite(app)
        httponly = self.get_cookie_httponly(app)

        # If the session is modified to be empty, remove the cookie.
        # If the session is empty, return without setting the cookie.
        if not session:
            if session.modified:
                response.delete_cookie(
                    name,
                    domain=domain,
                    path=path,
                    secure=secure,
                    samesite=samesite,
                    httponly=httponly,
                )

            return

        # Add a "Vary: Cookie" header if the session was accessed at all.
        if session.accessed:
            response.vary.add("Cookie")

        if not self.should_set_cookie(app, session):
            return

        expires = self.get_expiration_time(app, session)
        val = base64_encode(json.dumps(dict(session)))  # type: ignore
        response.set_cookie(
            name,
            val,  # type: ignore
            expires=expires,
            httponly=httponly,
            domain=domain,
            path=path,
            secure=secure,
            samesite=samesite,
        )
