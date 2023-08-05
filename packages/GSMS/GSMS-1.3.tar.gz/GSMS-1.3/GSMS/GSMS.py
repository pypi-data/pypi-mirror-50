"""GSMS - send sms via python using gmail -
   Usage:
   From GSMS import GSMS
   GSMS.sms('email', 'password', 'phone_number', 'carrier', 'message'
   Current Carrier Support: att, verizon,,tmobile,sprint,virgin,uscellular,boost"""
import smtplib
def sms(email,password,number,carrier,txt):
    mailserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    mailserver.ehlo()
    mailserver.login(email,password)
    carrier = carrier.lower()
    if carrier == 'att':
        number = number + '@text.att.net'
    if carrier == 'verizon':
        number = number + '@vtext.com'
    if carrier == 'tmobile':
        number = number + '@tmomail.net'
    if carrier == 'sprint':
        number = number + '@messaging.sprintpcs.com'
    if carrier == 'virgin':
        number = number + '@vmobl.com'
    if carrier == 'uscellular':
        number = number + '@email.uscc.net'
    if carrier == 'boost':
        number = number + '@myboostmobile.com'
    mailserver.sendmail(email, number, txt)        


