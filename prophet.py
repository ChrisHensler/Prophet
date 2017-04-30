#!/usr/bin/env python

from docopt import docopt, DocoptExit
import cmd
import sys

import app.scanner.scan_controller as scan_controller
from app.util import clean,info, workspaces, update, search


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


	#--------------commands------------------
	@docopt_cmd
	def do_search(self, args):
		"""Usage:
	search [(--ports=<ports> | -p <ports>)] [((--windows | -w) | (--linux | -l) | --os=<OS>)]

	Options:
		--os --linux --windows    filter by OS, replace spaces with underscores
		--ports   filter by port
"""
		print(args)

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

	def do_scan(self, line):
		"""Usage:
	scan <ip_range>
"""
		args=line.split(' ')

		if(len(args) > 0):
			scan_controller.RunAll(args[0])
		else:
			scan_controller.RunAll()

	def do_parse(self, line):
		"""
	parse <scan id>: update reports based on the scan id
"""
		args=line.split(' ')
		scan_controller.ParseScan(args[1])
	@docopt_cmd
	def do_info(self, args):
		"""Usage:
	info <host> [(<port>| --all)] [--script=<script_filter>]
"""
		print args
		host = args['<host>']
		port = args['<port>']
		if(args['--all']):
			port='all'

		script_filter= args['--script']

		print info.getInfoString(host, port, script_filter)

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

	def do_clean(self, line):
		"""
	    clean: cleans the temporary files and current session
"""
		args=line.split(' ')

		clean.clean()

	def do_update(self, line):
		"""
	    update: updates dependants, such at NSE scripts
"""
		args=line.split(' ')

		update.update()

	@docopt_cmd
	def do_exit(self, args):
		"""Usage:
	exit [--ip_range=<ip_range>] [<swears>...]

	Autopwn target ip range
"""
		if(args['--ip_range']):
			print "Why did you think that would work?"
		else:
			print "THE PROPHET SLEEPS"
			return True

	#def do_help(self, line):
	#	print __doc__


if __name__ =='__main__':
	ProphetShell().cmdloop()

