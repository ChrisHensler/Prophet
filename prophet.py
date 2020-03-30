#!/usr/bin/env python3

from imports.docopt import docopt, DocoptExit
import cmd, sys, os

import app.scanner.scan_controller as scan_controller
from app.util import clean,info, workspaces, update, search, progress, knock, system
from app.cracker import crack_controller
from app.probe import connect, extract

#----ripped from docopt github
def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('YOUR COMMAND IS INVALID! THE PROPHET REJECTS YOUR INPUT!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn
#----end rip



class ProphetShell(cmd.Cmd):
	intro = "THE PROPHET AWAKENS"
	prompt="?>"

	def bootstrap(self):
		self.scanner = scan_controller.ScanController()

	def terminate(self):
		del self.scanner

		print("THE PROPHET SLEEPS")
		return True

	#--------------commands------------------
	def emptyline(self):
		pass

	@docopt_cmd
	def do_search(self, args):
		"""Usage:
	search [(--ports=<ports> | -p <ports>)] [((--windows | -w) | (--linux | -l) | --os=<OS>)]

	Options:
		--os --linux --windows    filter by OS, replace spaces with underscores
		--ports   filter by port
"""

		ports = None
		if(args['-p']):
			ports = args['<ports>']
		else:
			ports=args['--ports']

		os = None
		if(args['--windows'] or args['-w']):
			os = 'windows'
		elif(args['--linux'] or args['-l']):
			os = 'linux'
		elif(args['--os']):
			os = args['--os'].replace('_'," ")
		print(search.search(ports=ports, os=os))

	@docopt_cmd
	def do_crack(self, args):  #docopt made me name it this
		"""Usage:
	crack <host> [<service>] [(--default | --names | --wordlist=<wordlist>)]

	Options:
		proto    protocol to crack, ex: ftp, ssh
		--default   check default passwords (ironically, this is the default setting)
		--names		check common names against both username and password
		--wordlist   file location for wordlist, must follow user:pass format
"""
		#translation
		default = args['--default']
		names = args['--names']
		wordlist = args['<wordlist>']
		service = args['<service>']
		host = args['<host>']
		

		if default:
			if host:
				crack_controller.crackDefaults(service, host)
			else:
				crack_controller.crackDefaults(host)
		elif names:
			if not host:
				color.c_print(color.bad_color, 'Please select a host')
			else:
				crack_controller.crackSimpleNames(host)
		elif wordlist:
			if not host or not service:
				color.c_print(color.bad_color, 'Please select a host and service')
			else:
				crack(service, host, split_wordlist=wordlist, threads=4)
		else:
			color.c_print(color.bad_color, 'Something has gone very wrong. Get Mom.')

	@docopt_cmd
	def do_knock(self, args):
		"""Usage:
	knock <host> <ports>...
"""
		knock.knock(args['<host>'], args['<ports>'])

	@docopt_cmd
	def do_scan(self, args):
		"""Usage:
	scan <ip_range> [<scans>...]

	Scans IP range
"""
		ip_range=args['<ip_range>']
		scans=args['<scans>']
		self.scanner.RunAll(ip_range, scans)


	@docopt_cmd
	def do_parse(self, args):
		"""Usage:
	parse <scan_id>

	update reports based on the scan id
"""
		self.scanner.ParseScan(args['<scan_id>'])

	@docopt_cmd
	def do_info(self, args):
		"""Usage:
	info [<host>] [(<port>| --all)] [--script=<script_filter>]
"""
		host = args['<host>']
		port = args['<port>']
		if(args['--all']):
			port='all'

		script_filter= args['--script']

		print(info.getInfoString(host, port, script_filter))

	@docopt_cmd
	def do_connect(self, args):
		"""Usage:
	connect <host>

	connects to a host if there is an applicable connect script
"""
		host = args['<host>']

		connect.connect_interactive(host)

	@docopt_cmd
	def do_extract(self, args):
		"""Usage:
	extract <host>

	extracts local data from a host if there is an applicable connect script
"""
		host = args['<host>']

		extract.extract(host)
	def do_save(self, line):
		"""
	save <name>: saves a scan with the given name
"""
		args=line.split(' ')

		if(len(args) > 0):
			name = args[0]

		if len(name.strip()) > 0:
			workspaces.save(name)

	def do_load(self, line):
		"""
    load <name>: loads a saved scan
"""
		args=line.split(' ')

		if(len(args) > 0):
			name = args[0]

		workspaces.load(name)

	def do_workspaces(self, line):
		"lists saved workspaces"

		workspaces.printList()

	def do_clean(self, line):
		"""
	    clean: cleans the temporary files and current session
"""
		args=line.split(' ')

		clean.clean()

	def do_progress(self, line):
		progress.progress()

	def do_update(self, line):
		"""
	    update: updates dependants, such at NSE scripts
"""

		update.update()

	@docopt_cmd
	def do_quit(self, args):
		"""Usage:
	quit

	Quits
"""
		return self.terminate()

	@docopt_cmd
	def do_exit(self, args):
		"""Usage:
	exit [--ip_range=<ip_range>] [<swears>...]

	Autopwn target ip range
"""
		if(args['--ip_range']):
			print("Why did you think that would work?")
		else:
			return self.terminate()


if __name__ =='__main__':
	if os.geteuid() != 0:
		exit('I require root privileges. Take a leap of faith and give all of yourself to me.')

	shell = ProphetShell()
	shell.bootstrap()
	shell.cmdloop()

