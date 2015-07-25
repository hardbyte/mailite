Mailite - re-send emails to users in a database.

Currently only mysql databases are supported but SQLite should be much easier!
If you have a forum or shop or any database which has a table of names and email addresses  why not give all your users their own email address @yourDomain.com without ANY setup other than installing this program. When users leave your site and are removed from your database - the email is no longer redirected. When new users sign up, as soon as their names and emails are in your database any emails to their name@yourDomain.com will be sent to their given email address.

Typical usage:
someone emails some\_name@your\_server.com
This program reads the "to" address of the incoming email and searches through
your site's members table for anyone matching "some name", then looks up the email address of that user. Mailite resends the email, from the original sender to the actual email address looked up. If the user wasn't found mailite optionally looks through a second and third database table e.g. job titles and groups. If no match was found the mail is returned to sender with a user not found error.

How to use this program:
**make sure your web-server supports python.** if your web-server doesn't have the python module MySQLdb you will have to install it.
**change the database settings below - specifying how to find the names and how to link them to an email address** put this file on your web-server where people can't get to it eg: /home/username/bin/mailite.py
**redirect all unrouted emails to be piped to this script. If using cpanel see "Default Addresses" for help.**


Brian Thorne 2008