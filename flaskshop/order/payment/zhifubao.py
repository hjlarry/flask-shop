import json
from pathlib import Path

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradeQueryModel import AlipayTradeQueryModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest

"""
支付宝沙盒环境相关配置：
1. 官方文档：https://opendocs.alipay.com/open/270/105898
2. 网关：https://openapi.alipaydev.com/gateway.do
3. app_id： 2016080400161922
4. 买家账号：abmaks2733@sandbox.com，商家账号：okavaq0242@sandbox.com。所有需要密码的地方都是111111
5. AlipayTradePagePayRequest接口直接返回跳转链接
6. AlipayTradeQueryRequest订单主动查询接口返回：
{"code":"10000","msg":"Success","buyer_logon_id":"abm***@sandbox.com","buyer_pay_amount":"0.00","buyer_user_id":"2088102170479214","buyer_user_type":"PRIVATE","invoice_amount":"0.00","out_trade_no":"167997094511","point_amount":"0.00","receipt_amount":"0.00","send_pay_date":"2023-03-28 10:36:28","total_amount":"0.02","trade_no":"2023032822001479210502487812","trade_status":"TRADE_SUCCESS"}
"""


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
    response = client.execute(request)
    return json.loads(response)
#
#
# def verify_order(data, signature):
#     success = pay_obj.verify(data, signature)
#     if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
#         return True
#     return False
