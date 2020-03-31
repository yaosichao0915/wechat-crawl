import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def QRscan():
    subject = "微信公众号需要登录"  # 主题
    # *************发送html的邮件**********
    msg = MIMEMultipart()

    boby = """
        <h3>Hi，all</h3>
        <p>微信公众号自动登录</p>
        <p>
        <br><img src="cid:image1"></br> 
        </p>
    """
    mail_body = MIMEText(boby, _subtype='html', _charset='utf-8')  
    msg.attach(mail_body)
    fp = open("QR.png", 'rb')
    images = MIMEImage(fp.read())
    fp.close()
    images.add_header('Content-ID', '<image1>')
    msg.attach(images)

    # 放入邮件主题
    msg['Subject'] = subject
    auto_mail(msg)
    
def AlertMsg(subject,text):
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['Subject'] = subject
    auto_mail(msg)
    
def auto_mail(msg):
    msg_from = 'sichao.yao@tgene.com.cn'  # 发送方邮箱
    passwd = ''  # 填入发送方邮箱的授权码(填入自己的授权码，相当于邮箱密码)
    msg_to = ['sichao.yao@tgene.com.cn']  # 收件人邮箱
    # 放入发件人
    msg['From'] = msg_from

    try:
        # 通过ssl方式发送
        s = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        # 登录到邮箱
        s.login(msg_from, passwd)
        # 发送邮件：发送方，收件方，要发送的消息
        s.sendmail(msg_from, msg_to, msg.as_string())
        print('邮件发送成功')
    except s.SMTPException as e:
        print(e)
    finally:
        s.quit()
#AlertMsg("test","quit")