import smtplib
smtp=smtplib.SMTP('cathaymail.linyuan.com.tw', 587)
smtp.ehlo()
smtp.starttls()
smtp.login('layx@cathaylife.com.tw','Lay9821529')
from_addr='layx@cathaylife.com.tw'
to_addr="lay9412206@gmail.com"
msg="Subject:Gmail sent by Python scripts\nHello World!"
status=smtp.sendmail(from_addr, to_addr, msg)#加密文件，避免私密信息被截取
if status=={}:
    print("郵件傳送成功!")
else:
    print("郵件傳送失敗!")
smtp.quit()

