import subprocess

DEBUG=False


def update():
	for cmd in ['nmap --script-updatedb','updatedb']:
		print cmd
		subprocess.call(cmd, shell=True)
