#!/usr/bin/python
""" 
Mailite - to re-send emails to users in a database.

Typical usage:
someone emails some_name@yourclub.com 
This program reads the "to" address of the incoming email and searches through
your sites members for anyone matching "some name", then looks up the email address of that user.
It resends the email, from the original sender to the actual email address looked up.
If the user wasn't found it optionally looks through a jobs database then at groups. If still
not found the mail is returned to sender with a user not found error.

How to use this program:
* make sure your webserver supports python.
* if your webserver doesn't have the python module MySQLdb you will have to install it.
* change the database settings below - specifing how to find the names and how to link them to an email address
* put this file on your webserver where people can't get to it eg: /home/username/bin/mailite.py
* redirect all unrouted emails to be piped to this script. see cpanel Default Addresses for help


Brian Thorne 2008

TODO:
* test alot
* clean up - OO it
* add filtering
* add groups - simple mailing lists
* make a mqs function - connect to db and select a single item and return it...
"""


###############################################################################
# Customize these settings to suit your needs:
###############################################################################
database_host = "localhost"
database_name = ""
database_user = ""    # user needs at least read access.
database_passwd = ""

name_tb = "members"             #the table in the database that contains names
name_tb_name = "Name"           #the field in name_table that contains all the names 
name_tb_id = "mid"              #if the member is refered to by a number enter the field found on the name table here
name_tb_filter = ""             #add a mysql where() clause if not all names in the table will be connected to emails.

email_tb = name_tb              #if the emails are stored in a differant table change this field
email_table_id = name_tb_id     #the field to link emails to names (used if data is across tables)
email_table_filter = ""
email_tb_email = "eMail"        #the field name for email addresses in the email_table

group_tb = "officers"           #the table containing any jobs...
group_tb_name = "Office"        #field to search through for job
group_tb_email = "eMail"        #field in table for email NOTE: may actually be a memberID or something (CHANGE ME... later)

loggingDir = "/home/bevs/bin/"
logFileName = loggingDir + "mailite.log"
wildcard = "%"                  #the character or string used as a wildcard by your database 

###############################################################################
# Settings end here - Do NOT Modify below unless you know what you are doing!
###############################################################################
import sys,logging,time
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s %(levelname)s %(message)s',filename=logFileName)
logging.info("Starting mailite script")

class NameNotFound(Exception):
    pass
class JobNotFound(Exception):
    pass
class EmailMalformed(Exception):
    pass

def mqs(query):
    """Query the database and select an item."""
    logging.debug("Mysql query: '%s'" % query)
    try:
        cursor.execute(query)
        row = cursor.fetchone()
        return row[0]
    except Exception, e:
        logging.error('error occured in mysql query. \nQuery:%s \n Error: %s' % (query,e))
        raise SystemExit

def lookupUser(email):
    """
    We must split up the email address and try determine if its addressed 
    to a name in our tables... ie Brian.Thorne@blah.com looks for a brian thorne
    Also may see if its in a job table eg president@blah.com looks up president in the jobs table
    """
    logging.debug("looking up email: %s" % email)
    try:
        section = email.split('@')[0]
        logging.debug("first section of email: %s" % section)
    except Exception, e:
        logging.error("failed to split email.")
        raise EmailMalformed
    try:
        newEmail = emailFromName(section)
        assert newEmail is not None
    except:
        logging.debug("email was not a name")
        try:
            newEmail = emailFromJob(section)
            assert newEmail is not None
        except:
            logging.debug("email was not a job either")
            print """
            Hello,
            We are sorry, but the email address (%s) was not found.
            %s
            """ % (section, email.split('@')[1])
            raise SystemExit
    return newEmail

def strReplace(s,old,new):
    """
    Utility string function that python really should have!
    For a given string s, replace any instances found of chars in the string old with new
    """
    import string
    if len(new) != len(old):
        new = len(old)*new
    tranTable = string.maketrans(old,new)
    s2 = string.translate(s, tranTable)
    return s2

def emailFromName(name):
    """
    Given a name search a table in a db for it and return the email address 
    return None if no match found
    """
    searchStr = wildcard + strReplace(name,"*.-_+1234567890",wildcard) + wildcard
    query = "SELECT " + email_tb_email + " FROM " + name_tb + " WHERE " + name_tb_name + ' LIKE "' + searchStr + '" LIMIT 1'
    return mqs(query)
    
def emailFromJob(job):
    """Given a job title find the email addy in a db or return None"""
    job = wildcard + strReplace(job,"*.-_+1234567890",wildcard) + wildcard
    
    query = "SELECT " + group_tb_email + " FROM " + group_tb + " WHERE LOWER(" + group_tb_name + ') LIKE "' + job.lower() + '" LIMIT 1'
    return mqs(query)

def connectToDB():
    logging.debug("importing MySQLdb")
    try:
        import MySQLdb
    except Exception, e:
        logging.error("Failed to import MySQLdb, error was: %s" %e)
        import os
        logging.debug("ENV data: %s" % "\n".join(os.environ.data))
        raise SystemExit

    logging.debug("Connecting to the database")
    try:
        conn = MySQLdb.connect(host = database_host,
            user = database_user,
            passwd = database_passwd,
            db = database_name)
        cursor = conn.cursor()
    except MySQLdb.Error, e:
        logging.error( "Error %d: %s" % (e.args[0], e.args[1]))
        raise SystemExit
    return (conn, cursor)

def saveEmailToFile():
    logging.debug("first save the email that is being piped in...")
    try:
        raw_email = sys.stdin.read() #read the email from stdin
    except Exception, e:
        logging.error("Couldn't get email from std in...")
        raise SystemExit

    logging.debug("save the email in a text file...")
    try:
        filename = loggingDir + 'emailScriptTestEmail'+time.ctime().replace(" ", "-")+'.txt'
        tmpfile = file(filename,'w')
        tmpfile.write(raw_email)
        logging.debug("email save as: %s" % filename)    
        tmpfile.close()
    except Exception, e:
        logging.error("Couldn't save email to temp file...")
        raise SystemExit
    return filename

def openEmailFromFile(filename):
    logging.debug("open the saved email")
    try:
        import email
        email_file = file(filename,'r')
        email_data = email.message_from_file(email_file)
        email_file.close()
    except Exception, e:
        logging.error("either couldn't open email from temp file or parse file into email...")
        raise SystemExit
    return email_data

def redirectEmail(email_data):    
    logging.debug("changing the recipient address based on db lookup")
    try:
        email_data.replace_header('To',lookupUser(email_data['To']))
    except:
        logging.error("Couldn't set new address.")
        raise SystemExit
    return email_data
    
def sendEmail(email_data):
    logging.debug("about to send the email onwards...")
    try:
        import smtplib
        smtp_conn = smtplib.SMTP()
        smtp_conn.connect()
        smtp_conn.sendmail(email_data['From'], email_data['To'], email_data.as_string())
        logging.debug("email was sent... from: %s to: %s" % (email_data['From'],email_data['To']))
        smtp_conn.close()
    except Exception, e:
        logging.error("Couldn't send email")
        raise SystemExit    

def closeConnection(conn,cursor):
    logging.debug("Closing Connection")        
    cursor.close()
    conn.commit()
    conn.close()
    

conn, cursor = connectToDB()
filename = saveEmailToFile()
email_data = openEmailFromFile(filename)
new_email_data = redirectEmail(email_data)
sendEmail(new_email_data)
closeConnection(conn,cursor)


#Misc bits for testing
#version = mqs("SELECT VERSION()")
#logging.info("MySql Version is: %s" % version)

#cursor.execute ("SELECT name, eMail FROM members")
#rows = cursor.fetchall()
#for row in rows:
#    logging.debug("%s, %s" % row)
#logging.debug("Number of rows returned: %d" % cursor.rowcount)


