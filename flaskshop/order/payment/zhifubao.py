from pathlib import Path

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradeQueryModel import AlipayTradeQueryModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest


def get_alipay_string():
    current_dir = Path(__file__).resolve().parent
    app_private_key = current_dir / "app_private_key.pem"
    ali_public_key = current_dir / "ali_public_key.pem"

    with open(app_private_key) as f:
        app_private_key_string = f.read()

    with open(ali_public_key) as f:
        alipay_public_key_string = f.read()

    return app_private_key_string, alipay_public_key_string


def get_payclient():
    app_private_key_string, alipay_public_key_string = get_alipay_string()
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'
    alipay_client_config.app_id = '2016080400161922'
    alipay_client_config.app_private_key = app_private_key_string
    alipay_client_config.alipay_public_key = alipay_public_key_string
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config)
    return client


def send_order(no, payment_no, total_amount):
    client = get_payclient()
    model = AlipayTradePagePayModel()
    model.out_trade_no = payment_no
    model.total_amount = str(total_amount)
    model.subject = "订单" + no
    model.body = "支付宝测试"
    model.product_code = "FAST_INSTANT_TRADE_PAY"
    request = AlipayTradePagePayRequest(biz_model=model)
    request.notify_url = "http://a5d267a6.ngrok.io/orders/alipay/notify"
    request.return_url = "http://127.0.0.1:5000/orders/payment_success"
    response = client.page_execute(request, http_method="GET")
    return response


def query_order(payment_no):
    client = get_payclient()
    model = AlipayTradeQueryModel()
    model.out_trade_no = payment_no
    request = AlipayTradeQueryRequest(biz_model=model)
    response = client.page_execute(request)
    return response
#
#
# def verify_order(data, signature):
#     success = pay_obj.verify(data, signature)
#     if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
#         return True
#     return False
