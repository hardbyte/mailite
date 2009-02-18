database_host = "localhost"
database_name = ""
database_user = ""              # user needs at least read access.
database_passwd = ""

name_tb = "members"             #the table in the database that contains names
name_tb_name = "Name"           #the field in name_table that contains all the names 
name_tb_id = "mid"              #if the member is refered to by a number enter the field found on the name table here
name_tb_filter = ""             #add a mysql where() clause if not all names in the table will be connected to emails.

email_tb = name_tb              #if the emails are stored in a differant table change this field
email_table_id = name_tb_id     #the field to link emails to names (used if data is across tables)
email_table_filter = ""
email_tb_email = "eMail"        #the field name for email addresses in the email_table

redirect_jobs = True
if redirect_jobs:
    job_tb = "officers"           #the table containing any jobs...
    job_tb_name = "Office"        #field to search through for job
    job_tb_email = "eMail"        #field in table for email NOTE: may actually be a memberID or something (CHANGE ME... later)

redirect_groups = True
if redirect_groups:    
    #Group redirects are for messaging lists of people
    #Currently set up for a table of mapping each user to each group.
    group_redirects = True
    groups_tb = "groups"
    groups_tb_index = "gid"         #Group ID, set to None if map is done on title alone.
    groups_tb_title = "name"        #field to search through for group title.

    #Table that maps line by line user (by ID) to group (by ID)
    groupmap_tb = "group_map"
    groupmap_tb_group_index = "gid"
    groupmap_tb_member_index = "mid"

loggingDir = "/home/bevs/bin/"
logFileName = loggingDir + "mailite.log"

save_emails_on_server = False