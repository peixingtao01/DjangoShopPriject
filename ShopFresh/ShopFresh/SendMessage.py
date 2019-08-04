# from qcloudsms_py import SmsSingleSender
# from qcloudsms_py.httpclient import HTTPError
#
# appid ='1400240005'
# appkey = 'd8af75c8a3a053d13dfb9f4ecfc97bde'
# phone_numbers = ['13906445972']
# template_id = ''
#
# sms_type = 0
# ssender = SmsSingleSender(appid,appkey)
#
# try:
#     result = ssender.send(sms_type,86,phone_numbers[0],'[小裴同学]',extend='',ext='')
# except HTTPError as e:
#     print(e)
# except Exception as e:
#     print(e)
# print(result)