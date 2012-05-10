import smtplib

def mail(serverURL=None, sender='', to='', subject='', text=''):
    """
    Usage:
    mail('somemailserver.com', 'me@example.com', 'someone@example.com', 'test', 'This is a test')
    """
    headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, to, subject)
    message = headers + text
    mailServer = smtplib.SMTP(serverURL)
    # If the server needs authentication
    #mailServer.login('USER', 'PASS')
    mailServer.sendmail(sender, to, message)
    mailServer.quit()

    
def test():
    mailMe = ('server','no-reply@server.com','my_email@gmail.com',"Test email","This is a test email from python\n--Brian")
    mail(*mailMe)
    
if __name__ == "__main__":
    test()
