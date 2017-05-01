import os
from app.scanner import generic_scanner
from app.util import fileutil

APP_ROOT = '.'


def crackDefaults(host):
	for service in ['ftp','ssh','mssql','mysql','oracle','telnet']:
		crackDefault(service, host)

def crackDefault(service, host):
	split_wordlist = os.path.join(fileutil.getConfigPath(), 'wordlists','defaults',service + '.split.txt -o {outfile}')
	crack(service, host, split_wordlist)


def crack(service, host, split_wordlist=None, user_list=None, password_list=None):
	if not service in ['ftp','ssh','mssql','mysql','oracle','telnet']:
		print "crack: Unsupported service: " + service
		return

	threads = 16
	if(service == 'ssh'): threads = 4

	if split_wordlist:
		lists = '-C {0} '.format(split_wordlist)
	else:
		lists = ' -L {0} -P {1} '.format(user_list, password_list)

	cmd = 'hydra {3} -t {4} {1}://{0}  -o {2}'.format('{host}', service, '{outfile}', lists, threads)
	
	generic_scanner.ScanHost(name = service.upper() + "_Crack",host = host,action = cmd, valid_services = [service])
