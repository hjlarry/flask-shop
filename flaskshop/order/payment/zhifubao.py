import json
from pathlib import Path

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradeQueryModel import AlipayTradeQueryModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
from alipay.aop.api.util.SignatureUtils import verify_with_rsa

"""
支付宝沙盒环境相关配置：
1. 官方文档：https://opendocs.alipay.com/open/270/105898
2. 网关：https://openapi.alipaydev.com/gateway.do
3. app_id： 2016080400161922
4. 买家账号：abmaks2733@sandbox.com，商家账号：okavaq0242@sandbox.com。所有需要密码的地方都是111111
5. AlipayTradePagePayRequest接口直接返回跳转链接
6. AlipayTradeQueryRequest订单主动查询接口返回：
{"code":"10000","msg":"Success","buyer_logon_id":"abm***@sandbox.com","buyer_pay_amount":"0.00","buyer_user_id":"2088102170479214","buyer_user_type":"PRIVATE","invoice_amount":"0.00","out_trade_no":"167997094511","point_amount":"0.00","receipt_amount":"0.00","send_pay_date":"2023-03-28 10:36:28","total_amount":"0.02","trade_no":"2023032822001479210502487812","trade_status":"TRADE_SUCCESS"}
7. 支付宝往notify_url上返回：
{'gmt_create': '2023-03-28 15:09:40', 'charset': 'utf-8', 'gmt_payment': '2023-03-28 15:09:44', 'notify_time': '2023-03-28 15:09:46', 'subject': '订单48dc38aa-
cd24-4b79-b6d0-9e5634d7e284', 'sign': 'nk1xdHGU8nz/qPDASf6fEgWY0YPKui17uNYQcKZRFxT7YsOyLu5XVUfSBjV4SdpmXYh3KwwaLZE0UbVbxWq4f+7tyAFQKoriz8bMEfmQulObuaNGfqXy9GFZAqqcSBljVko
xvHzhq+sg774qkCI8QJkQwIXc4lWckDis6tJnY653KXb7I1MYalEMZ46ooMrvhoTJB+WOgpVklVZSfnaBlUEz/hSrcatMehdISjUDOBDJyN/AuGjnWJoLHRZMgEIADHwYNSnFbqoiXckjN8Aw44qucORaGJ29YFFYjT3iDqRd0
k/CHQQT8y0XRq/27ACkSVO6OzsqOXElifoSxv2nkA==', 'buyer_id': '2088102170479214', 'body': '支付宝测试', 'invoice_amount': '0.02', 'version': '1.0', 'notify_id': '202303280022
2150945079210522880588', 'fund_bill_list': '[{"amount":"0.02","fundChannel":"ALIPAYACCOUNT"}]', 'notify_type': 'trade_status_sync', 'out_trade_no': '167998736311', 'total
_amount': '0.02', 'trade_status': 'TRADE_SUCCESS', 'trade_no': '2023032822001479210502487814', 'auth_app_id': '2016080400161922', 'receipt_amount': '0.02', 'point_amount'
: '0.00', 'app_id': '2016080400161922', 'buyer_pay_amount': '0.02', 'sign_type': 'RSA2', 'seller_id': '2088102169849330'}
这时候验签要去掉sign和sign_type并字典排序，拼接字符串再encode再去验签
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
    alipay_client_config.server_url = "https://openapi.alipaydev.com/gateway.do"
    alipay_client_config.app_id = "2016080400161922"
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
    request.notify_url = "http://mg2e4t.natappfree.cc/orders/alipay/notify"
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


def verify_order(data):
    _, alipay_public_key_string = get_alipay_string()
    signature = data.pop("sign")
    data.pop("sign_type")
    s_data = dict(sorted(data.items(), key=lambda x: x[0]))
    msg = ""
    for key, value in s_data.items():
        msg = msg + key + "=" + value + "&"
    message = msg[:-1].encode("UTF-8")
    result = verify_with_rsa(alipay_public_key_string, message, signature)
    return result
