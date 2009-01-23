import smtplib
def mail(serverURL=None, sender='', to='', subject='', text=''):
	"""
	Usage:
	mail('somemailserver.com', 'me@example.com', 'someone@example.com', 'test', 'This is a test')
	"""
	headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, to, subject)
	message = headers + text
	mailServer = smtplib.SMTP(serverURL)
	mailServer.sendmail(sender, to, message)
	mailServer.quit()

	
def test():
    mailUser = ('bevs-hire.com','hardbyte@gmail.com','brian.thorne@uccc.org.nz',"Test to User","This is a test email from python\n--Brian")
    mailJob = ('bevs-hire.com','hardbyte@gmail.com','webmaster@uccc.org.nz',"Test to Job","This is a test email from python\n--Brian")
    mail(*mailUser)
    mail(*mailJob)
    
if __name__ == "__main__":
    test()
