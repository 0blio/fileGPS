#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import requests
import os
from multiprocessing import Pool, Queue
from Helpers.graphic import *
from Helpers.connections import *
from Helpers.utilities import *
from functools import partial
import Helpers

# Don't write .pyc files
sys.dont_write_bytecode = True

# Initializing the parser
parser = argparse.ArgumentParser (description=print_logo(), usage="python %s [options]" % sys.argv[0], add_help=False)

# Removing the default arguments group (to customize the --help parameter)
parser._action_groups.pop()

# Creating three groups of arguments (required arguments, optional arguments and modules)
required = parser.add_argument_group ("\033[1mRequired arguments\033[0m")
optional = parser.add_argument_group ("\033[1mOptional arguments\033[0m")

# These are not valid arguments, it is just to print usefull data in a formatted way
modules = parser.add_argument_group ("\033[1mModules\033[0m")
examples = parser.add_argument_group ("\033[1mExamples\033[0m")

# Setting up arguments in the "required" group
required.add_argument ("-u", "--url", metavar=("URL"), help="Target URL (e.g \"http://target.com/uploads\")", required=True)
required.add_argument ("--file", metavar=("FILENAME"), help="Filename of the file you uploaded on the target server", required=True)

# Setting up arguments in the "optional" group
optional.add_argument ("--modules", metavar=("MODULES"), help="Comma separated list of the modules to be imported (Use '*' to import all modules)", default="*")
optional.add_argument ("--proxy", metavar=("PROXY"), help="Use a proxy to connect to the target URL")
optional.add_argument ("--custom", metavar=("WORDS"), help="Comma separated list of the custom words to be used to find the file")
optional.add_argument ("--cookie", metavar=("COOKIE"), help="HTTP Cookie header value")
optional.add_argument ("--threads", metavar=("THREADS"), help="Max number of concurrent HTTP(s) requests (default: 1, max: 10)", type=int, choices=range(1,11,1), default=1)
optional.add_argument ("--user-agent", metavar=('AGENT'), help="HTTP User-Agent header value")
optional.add_argument ("--random-agent", action="store_true", help="Use randomly selected HTTP User-Agent header value")
optional.add_argument ("-o", metavar=("FILENAME"), help="Save all generated filenames in a file")
optional.add_argument ("-h", "--help", help="Show help message and exit")

# Setting up the list of available modules
modules.add_argument ("shame", action="store_true", help="Generates basic filenames")
modules.add_argument ("timebomb", action="store_true", help="Generates various combinations of timestamps and filenames iterating up to 5 minutes before the start of the script")

# Setting up the list of examples
examples.add_argument ("fileGPS -u http://target.com/upload/images --file shell.php", action="store_true")
examples.add_argument ("fileGPS -u http://target.com/upload/images --file shell.php --modules shame,mytestmodule", action="store_true")
examples.add_argument ("fileGPS -u http://target.com/upload/images --file shell.php --proxy 127.0.0.1:9050 --cookie mycookies", action="store_true")

# If there aren't arguments passed to the program  or user requested an help print the help message and exit
if len(sys.argv[1:]) == 0 or len(sys.argv[1:]) == 1 and sys.argv[1] in ["-h", "--help"]:
	parser.print_help()
	print
	exit()

# Parsing the arguments
args = parser.parse_args()

# Assigning all used arguments to respective data structures
url = make_host_valid(args.url)
base_url = get_base_hostname (url)
filename = args.file
modules = args.modules.replace(" ", "")
custom_words = args.custom.replace(" ", "").split(",") if args.custom else []
session_cookie = args.cookie if args.cookie else ""
proxy = args.proxy if args.proxy else ""
file_output = args.o if args.o else ""
threads = args.threads
user_agent = args.user_agent if args.user_agent else ""

if args.random_agent or args.user_agent == "" or not args.user_agent:
	try:
		notification ("Setting up random agent..", "info")
		user_agent = random_user_agent()
		notification ("Selected user agent: %s" % (user_agent), "success")
	except:
		notification ("Error reading the user agents file.", "error")

print

# Checking if the target is up and running
notification ("Testing connection with the target.", "info")
notification ("Sending an HTTP request to %s .." % base_url, "notify")

if check_target_connection (url, user_agent):
    notification ("The target appears to be up and running!", "success")
else:
    notification ("The target seems to be down. Quitting..\n", "error")
    exit()

print

# If the user want to import all modules (or he didn't specified any modules)
if modules == "*":
    modules = []

    # If there are no modules
    if len(os.listdir("Modules")) == 0:
        notification ("No modules found. Quitting..", "error")
        exit()

    # Add all .py contained in Modules/ to the list of modules to use
    for m in os.listdir ("Modules"):
        if m.endswith (".py"):
            modules.append(m)

# Else if the user specified the modules to import
else:
    argument_values = modules.split (",")
    argument_values = [s + ".py" for s in argument_values]
    modules = []

    # If the module exists append it to the list of valid modules
    for argument in argument_values:
        if os.path.isfile ("Modules/" + argument):
            modules.append(argument)
        else:
            notification ("Module '%s' not found" % argument.strip(".py"), "error")

    del argument_values

# Checking if there some modules
if len(modules) == 0:
	notification ("No modules found. Quitting..", "error")
	exit()
else:
	notification ("Running all %s modules." % str(len(modules)), "info")

# Executing valid modules
filenames = []
for module in modules:
    notification ("Running module '%s' .." % module.strip(".py"), "notify")
    execfile ("Modules/" + module)

    # Checking if the module generated an output (allocated list of filenames to search for)
    if 'output' in locals():
        notification ("'%s' generated %s possible filenames" % (module.strip(".py"), str(len(output))), "success")
        filenames += output
        del output

    else:
        notification ("Invalid module: '%s'" % module.strip(".py"), "error")

# If the modules generated some filenames
if len(filenames) > 0:
	# If the user want to output the filenames in a file
	if file_output != "":
		print
		notification ("Writing the generated filenames to '%s'" % file_output, "info")

		try:
			with open (file_output, "w") as fp:
				for filename in filenames:
					fp.write("%s\n" % filename)

			notification ("File written successfully!", "success")
		except:
			notification ("Error writing the file!", "error")

	print

	while 1:
		try:
			proceed = raw_input ("[\033[1m\033[94m?\033[0m] Do you want to test %s filename against %s [y/n]? " % (str(len(filenames)), url)).lower().replace(" ", "")
			if proceed == 'y':
				break
			elif proceed == 'n':
				notification ("Stopped", "removed")
				exit()
		except KeyboardInterrupt:
			print
			notification ("Stopped", "removed")
			exit()

	print

	if threads == 1:
		notification ("Testing all %s generated filenames with 1 thread.." % str(len(filenames)), "info")
		requester (url, filenames, session_cookie, user_agent, proxy)
	elif threads > 1:
		notification ("Testing all %s generated filenames with %s threads.." % (str(len(filenames)), threads), "info")

		# Allocating shared memory between processes
		queue = Queue()

		# Allocating a pool of N threads
		p = Pool (threads, worker_init, [queue])

		# Creating a partial function with the fixed arguments
		r = partial (requester3, url, session_cookie, user_agent, proxy)

		# Mapping asynchronously the function on the spawned processes
		workers = p.map_async (r, filenames)

		i = 0
		len_filenames = len(filenames)

		# Accessing the shared memory until something happen
		while 1:
			try:
				if i == len_filenames:
					notification ("File not found..", "error")
					break

				# Getting a result from the shared memory
				result = queue.get()

				print "[%s%s%s] %s" % (bcolors.PINK, percentage(i, len_filenames) + "%", bcolors.ENDC, result[0])

				sys.stdout.write("\033[F")
				sys.stdout.write("\033[K")

				# If fileGPS found the file
				if result[1] == 200:
					notification ("FileGPS found your file! It is here: \033[4m%s\033[0m" % result[0], "found")
					break

				i += 1
			except KeyboardInterrupt:
				notification ("Stopped", "removed")
				break

		p.terminate()
		p.join()
		exit()
