from flask_mail import Message
from app import mail

msg = Message('test mail', sender='diyorbekqodirboyev@gmail.com', recipients=['d.zcode4@gmail.com'])
msg.body = 'text body'
msg.html = 'text <b>html</b>'
mail.send(msg)