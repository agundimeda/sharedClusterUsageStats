import mysql.connector
import datetime
import cStringIO
from smtplib import SMTP as smtp
#import ldap

def listUsers(): # Returns a string list of all 'uma' users from the start of the fiscal year as both a list of usergroups and PI names 
	now = datetime.datetime.now()
	SoM = datetime.datetime(now.year,now.month,01)
	if (now.month < 07):
		SoY = datetime.datetime(now.year-1,07,01)
	else:
		SoY = datetime.datetime(now.year,07,01)

	shareddb = mysql.connector.connect(
		host = "ghpcc05",
		user = "uma",
		passwd = "",
		database = "lsf_acct")

	cursor = shareddb.cursor()

	cursor.execute("SELECT PI FROM uma WHERE endtime > '" + str(SoY) + "' GROUP by PI ORDER by cpuseconds DESC;")
	result = cursor.fetchall()
	res = []
	for name in range(len(result)):
		res.append(result[name][0].split('_')[1] + ' ' + result[name][0].split('_')[2])
	return result, res

def userQuery(name): # Returns monthly & yearly usage statistics for a single usergroup
	PI = "'" + name + "'"
	buff = cStringIO.StringIO()
	now = datetime.datetime.now()
	SoM = datetime.datetime(now.year,now.month,01)
	if (now.month < 07):
		SoY = datetime.datetime(now.year-1,07,01)
	else:
		SoY = datetime.datetime(now.year,07,01)

	
	shareddb = mysql.connector.connect(
		host = "ghpcc05",
		user = "uma",
		passwd = "",
		database = "lsf_acct")

	buff.write("PI: " + name + '\n')
	cursor = shareddb.cursor()

	cursor.execute("SELECT username, SUM(cpuseconds) FROM uma WHERE PI =" + PI + " AND endtime >='" + str(SoM) + "' GROUP by username ORDER by cpuseconds DESC;")
	MTD = cursor.fetchall()
	
	cursor.execute("SELECT username, SUM(cpuseconds) FROM uma WHERE PI =" + PI + " AND endtime >='" + str(SoY) + "' GROUP by username ORDER by cpuseconds DESC;")
	YTD = cursor.fetchall()

	buff.write("\nMonth-to-Date Total Usage: ")
	buff.write(str(round((sum(n for _, n in MTD)/31560000),3)) + " CPU Years\n")
	buff.write("\nMonth-to-Date Usage by User:")
	for entry in range(len(MTD)): 
		buff.write('\n'+str(MTD[entry][0]) + ": " + str(round((MTD[entry][1]/31560000),3)) + " CPU Years")
	buff.write('\n')
	
	buff.write("\nYear-to-Date Total Usage: ")
	buff.write(str(round((sum(n for _, n in YTD)/31560000),3)) + " CPU Years\n")
	buff.write("\nYear-to-Date Usage by User: ")
	for entry in range(len(YTD)): 
		buff.write('\n'+str(YTD[entry][0]) + ": " + str(round((YTD[entry][1]/31560000),3)) + " CPU Years")
	
	return buff.getvalue()
def mailLookup(name): # Pulls up user email by common name in campus LDAP
	con = ldap.initialize('ldaps://auth-ldap.umass.edu')
	con.simple_bind("cn=nss,ou=services,dc=umass,dc=edu", "")
	result = con.search_s('ou=people,dc=umass,dc=edu',
				ldap.SCOPE_SUBTREE,
				'displayname=*' + name + '*',
				["mail"])
	
	result = result[0][1].get('mail')[0]
	return result

def sendMail(user,msg): # Sends an email from the hpc account
	server = smtp('mail-auth.oit.umass.edu')
	server.starttls()
	server.login('', '')
	server.sendmail('',user,'Subject: Shared Cluster Usage Update \r\n\r\n' + msg)

def driver(): 
	usergroupList = listUsers()[0]
	userList = listUsers()[1]
	
	for person in range(len(userList)):
		sendMail(mailLookup(userList[person]),userQuery(usergroupList[person]))



