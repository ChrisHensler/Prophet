import os
import app.scanner.generic_scanner as generic_scanner
import app.util.fileutil as fileutil

APP_ROOT = '.'


def crackDefaults(host):
	for service in ['ftp','ssh','mssql','mysql','oracle','telnet','snmp']:
		crackDefault(service, host)
		

def crackSimpleNames(service, host):
		#quick test of standard names
		standard_list=os.path.join(fileutil.getConfigPath(), 'wordlists','common','names_lower.txt')
		crack(service, host, user_list=standard_list)


def crackDefault(service, host):
	split_wordlist = os.path.join(fileutil.getConfigPath(), 'wordlists','defaults',service + '.split.txt -o {outfile}')
	crack(service, host, split_wordlist)


def crack(service, host, split_wordlist=None, user_list=None, password_list=None, threads = 1):
	if not service in ['ftp','ssh','mssql','mysql','oracle','telnet']:
		print("crack: Unsupported service: " + service)
		return

	if split_wordlist:
		lists = '-C {0} '.format(split_wordlist)
	elif password_list is None:  #checking only usernames
		lists = ' -L {0} -e nsr '.format(user_list)
	else:
		lists = ' -L {0} -P {1} '.format(user_list, password_list)

	cmd = 'hydra {3} -u -f -t {4} {1}://{0}  -o {2}'.format('{host}', service, '{outfile}', lists, threads)
	
	generic_scanner.ScanHost(name = service.upper() + "_Crack",host = host,action = cmd, valid_services = [service])


