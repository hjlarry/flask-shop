from flask import g, current_app
from flask.sessions import SecureCookieSessionInterface
from flask_login import user_loaded_from_header
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_restplus import Namespace, Resource, fields
import requests

from flaskshop.extensions import login_manager
from flaskshop.account.models import User

WECHAT_LOGIN_URL = ""
WECHAT_APP_SECRET = ""
WECHAT_APP_ID = ""

api = Namespace("user", description="User Login Api")
parser = api.parser()
parser.add_argument("code", type=str, required=True, help="The code")


def generate_token(user_id):
    serializer = Serializer(current_app.config["SECRET_KEY"], expires_in=36000)
    return serializer.dumps({"user_id": user_id})


def verify_token(token):
    try:
        serializer = Serializer(current_app.config["SECRET_KEY"], expires_in=36000)
        data = serializer.loads(token)
    except:
        return False
    return data["user_id"]


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""

    def save_session(self, *args, **kwargs):
        if g.get("login_via_header"):
            return
        return super().save_session(*args, **kwargs)


@user_loaded_from_header.connect
def user_loaded_from_header(self, user=None):
    g.login_via_header = True


@login_manager.request_loader
def load_user_from_request(request):
    token = request.headers.get("Authorization")
    try:
        user_id = verify_token(token)
        user = User.get_by_id(user_id)
        if user:
            return user
    except:
        return None


@api.route("/login")
class UserLogin(Resource):
    @api.doc(parser=parser)
    def post(self):
        args = parser.parse_args()
        res = requests.get(
            WECHAT_LOGIN_URL.format(WECHAT_APP_ID, WECHAT_APP_SECRET, args["code"])
        ).json()
        open_id, session_key = res["openid"], res["session_key"]
        user = User.query.filter_by(open_id=open_id).first()
        if not user:
            user = User.create(
                username=open_id,
                email=open_id,
                password=open_id,
                open_id=open_id,
                session_key=session_key,
            )
        data = {
            "token": generate_token(user.id).decode(),
            "cart_lines": len(user.cart.lines),
        }
        return data
