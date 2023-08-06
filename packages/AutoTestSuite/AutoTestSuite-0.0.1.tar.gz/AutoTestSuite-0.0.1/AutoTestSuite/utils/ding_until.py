# _*_ coding:utf-8 _*_
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_email(SMTP_host, from_account, from_password, to_account, subject, content):
    # 1. 实例化SMTP
    smtp = smtplib.SMTP()

    # 2. 链接邮件服务器
    smtp.connect(SMTP_host)

    # 3. 配置发送邮箱的用户名和密码
    smtp.login(from_account, from_password)

    # 4. 配置发送内容msg
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject,'utf-8')
    msg['From'] = from_account
    msg['To'] = to_account

    # 5. 配置发送邮箱，接受邮箱，以及发送内容
    smtp.sendmail(from_account, to_account, msg.as_string())

    # 6. 关闭邮件服务
    smtp.quit()

if __name__ == '__main__':
    send_email("smtp.163.com", "from_account", "from_pssword","to_account", "I want to talk to u", "In this semester")