from alipay import AliPay

alipay_public_key_string ="""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsUz6B1oA0tJkDIg3nvKbUggu3FswnBQ6e5kj1MSxrbAKJF1s2+6fK0tpBD5VWaRCyKCf73ulC0BQv2WFKRxQ+ud3r08JuKr0a6u2aBnua7+Zbw34kbqoNYJ0LZitGdJQnotbDc2GgyxOO2Bd3WjvInB4otjXS2y3jNDQRh2fV2Rml4C5RcTIsbeivcvNw3/pvNTP6x45neD1JpPxeFvgT/Y9aj/Xytw52mYLycblZ++fto48zzCSrxKzotyJR5b5shFdOjheTKb1SMGAiXKh03MmRjMqwR8iNn/7j9oreCykzxKcSewrshXpnjslBqZDlpWoUGJU09kfhMiO1espKwIDAQAB
-----END PUBLIC KEY-----"""

app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAsUz6B1oA0tJkDIg3nvKbUggu3FswnBQ6e5kj1MSxrbAKJF1s2+6fK0tpBD5VWaRCyKCf73ulC0BQv2WFKRxQ+ud3r08JuKr0a6u2aBnua7+Zbw34kbqoNYJ0LZitGdJQnotbDc2GgyxOO2Bd3WjvInB4otjXS2y3jNDQRh2fV2Rml4C5RcTIsbeivcvNw3/pvNTP6x45neD1JpPxeFvgT/Y9aj/Xytw52mYLycblZ++fto48zzCSrxKzotyJR5b5shFdOjheTKb1SMGAiXKh03MmRjMqwR8iNn/7j9oreCykzxKcSewrshXpnjslBqZDlpWoUGJU09kfhMiO1espKwIDAQABAoIBAQCf7JkSjIJ1p0SLcUsKWjbzdWIfbTmZbz2ZQvbo8kp6KnHbf1Gzx7dWq/yb0UXXR6zdntTkhRjH30l2erHz9RCuYJ66SIayRbGWdRphKBLAqeBSJb3yZPVY3sTAZBivU99YQsbs2lfcddhTAodoMUCSRfTqnsEDzZp6r9dNh2a0weA38JKHr16VHLtQ1U7mzpyjvyWUNQSpeyPw2crl2Xo/WobnhJW9MsPsmtgRg9HtBfBaOCz68t4EwCWaviIYZ8VBiu/h1v8QFoE8bY3M6ClrUGxy/G86KwdFF5V+OrQ1Aw+4o2wn4POERdtsdh94HZNUhLjgCFXsSUfh8bQJVmGBAoGBAOGW6jqCJkYk6yIrlOX1wP+vWwRqqy+jKB27+b+d6D5kEN8/MrWP9uATcBnOcfSETBVCrzKD4z+8nhdUdqHGOEwK0b6Cu1QwK5byRQTuc4D9L3JfnXR5tOAVQB594X87Yc7b7DThU8qO6IIkXXzATCmycCBbVbIUX+1XevXI7z4LAoGBAMkznc2fn6BIK5MgGZ1F9ztjgjmoeGe59Eb/xGbp4C7sNoxm0OXn0LBU45SctVWQT0l+Iez6y+vI6mAzvWwkH6SzWPBzDV///zriJSsAhhGfF9WqLXSzwd59lUln2vRIZsucDm9T9ZpW7BmO5+vSnbaOHUeQ/VTfQ3pzGxO04VVhAoGABxLbX2BLYPGxac3iCl/tYFcYTIgnvAOqs1v8ldSWvrYWjVmG9oiAHkCdyEFf82HenOANbFEUZCA++M5ONf5oL4I7V3Tz+MzV4RLRtTjg6E+IGFcFMezLDie8bfhWhM3Q4FKnEnVqUjSu9726LLo+6SPOPkV+52maJHAUy/Y0AkcCgYB5BjhMoFCHPAIh/HQL2zMMoR2LCyBp3DvonR6JfPKhpupk58+OCzPHbTh7gwu8TRK0NU+42V7iFDeO6HBvZQc3rb243KvV7AmdZLxQsn7yiIzws+2lvh7GcyniPrtAp3BV1ygDpTAdx107Pm+YtVayoadRDhCkBav0Mtq9rta/4QKBgBjJoQsbs0YNTWgsPJB+Sj3j2g/0EGgVkbuf8M89VKc9RnKpgRxCRRqcJu/gVQHR5OvHkUen1mJwXwRIRRDfbo1bFdlVRJswXox05kTXQZRNxOQ0FJPAIxp47xTMnvUQnPR8KKBIaR56evBkkBGzCzvly98MntNn5Wn5l2XRPLUG
-----END RSA PRIVATE KEY-----"""

alipay = AliPay(
    appid = '2016101000652494',
    app_notify_url = None,
    app_private_key_string = app_private_key_string,
    alipay_public_key_string = alipay_public_key_string,
    sign_type = 'RSA2'
)
# 网页支付请求
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no = '33453',#订单号,
    total_amount = str(5000.00),#支付金额
    subject = '生鲜交易',
    return_url= None,
    notify_url=None
)

# 给定的支付宝网关
print('https://openapi.alipaydev.com/gateway.do?'+order_string)