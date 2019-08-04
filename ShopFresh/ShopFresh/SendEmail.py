import smtplib
from email.mime.text import MIMEText

subject = '邮件标题'
content = '邮件内容'
sender = '13906445972@163.com'
recver = '1307128051@qq.com'
password = 'duoyan3wei'#客户端授权码

message = MIMEText(content,'plain','utf-8')
message['Subject'] = subject
message['TO'] = recver
message['From'] = sender

smtp = smtplib.SMTP_SSL('smtp.163.com',994)
smtp.login(sender,password)
smtp.sendmail(sender,recver,message.as_string())
smtp.close()