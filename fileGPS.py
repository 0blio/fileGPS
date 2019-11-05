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

# Formatter class for argparse
formatter = lambda prog: argparse.HelpFormatter(prog, max_help_position=35, width=95)

# Initializing the parser
parser = argparse.ArgumentParser (description=print_logo(), usage="python %s -u <url[/path]> --file <filename> [options]" % sys.argv[0], add_help=False, formatter_class=formatter)

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
required.add_argument ("-f", "--file", metavar=("FILENAME"), help="Filename of the file uploaded on the target server", required=True)

# Setting up arguments in the "optional" group
optional.add_argument ("--modules", metavar=("MODULE1,[MODULE2..]"), help="Comma separated list of the modules to be imported (Use '*' to import all modules). By default, all modules will be used.", default="*")
optional.add_argument ("--proxy", metavar=("PROXY"), help="Use a proxy to connect to the target URL")
optional.add_argument ("--custom", metavar=("WORDS"), help="Comma separated list of the custom words to be used to find the file")
optional.add_argument ("--cookie", metavar=("COOKIE"), help="HTTP Cookie header value")
optional.add_argument ("--threads", metavar=("THREADS"), help="Max number of concurrent HTTP(s) requests (default: 1", type=int, default=1)
optional.add_argument ("--user-agent", metavar=('AGENT'), help="HTTP User-Agent header value")
optional.add_argument ("--match", metavar=('STRING'), help="Text pattern to match in the response (e.g. webshell)")
optional.add_argument ("--random-agent", action="store_true", help="Use randomly selected HTTP User-Agent header value")
optional.add_argument ("-o", "--output", metavar=("FILENAME"), help="Save all generated filenames in a file")
optional.add_argument ("-v", "--verbose", action="store_true", help="Verbose mode")
optional.add_argument ("-h", "--help", help="Show help message and exit")

# Setting up the list of available modules
modules.add_argument ("shame", action="store_true", help="Generates a list of hashed filenames. If the user doesn't specify a specific path to search the file in, it appends the generated values to a list of common upload directories.")
modules.add_argument ("timebomb", action="store_true", help="Generates various combinations of timestamps and filenames iterating up to 1 minute before the start of the script.")
modules.add_argument ("monkey", action="store_true", help="Generates various combinations of filenames, sequential numbers and custom words.")

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
file_output = args.output if args.output else ""
threads = args.threads
match = args.match if args.match else ""
user_agent = args.user_agent if args.user_agent else ""
random_agent = True if args.random_agent else False
verbose = True if args.verbose else False

if random_agent:
	notification ("Setting up random user agent..", "info")
	user_agent = random_user_agent()
	notification ("Selected user agent: %s" % (user_agent), "success")

elif args.user_agent == "" or not args.user_agent or not random_agent:
	verbose_message (notification("No user agent specified.\n", "added", False), verbose)
	try:
		notification ("Setting up default user agent..", "info")
		user_agent = "fileGPS_0blio"
		notification ("Selected user agent: %s" % (user_agent), "success")
	except:
		notification ("Error reading the user agents file.", "error")

print

# Checking if the target is up and running
notification ("Testing connection with the target.", "info")
verbose_message (notification("Sending an HTTP HEAD request to %s .." % base_url, "added", False), verbose)

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

    # Sort modules by relevance
    tmp = []
    for r in ["shame.py", "timebomb.py", "monkey.py"]:
        if r in modules:
            tmp.append(r)
    modules = tmp + [x for x in modules if x not in ['shame.py', 'timebomb.py', 'monkey.py']]
    del tmp

# Else if the user specified the modules to import
else:
    argument_values = modules.split (",")

	# If there are some duplicates specified by the user filegps will not re-execute an already executed module
    if len(argument_values) != len(set(argument_values)):
		verbose_message (notification("You have selected duplicates modules. Removing them automatically..\n", "added", False), verbose)
		argument_values = list(dict.fromkeys(argument_values))

    argument_values = [s + ".py" for s in argument_values]
    modules = []

    # If the module exists append it to the list of valid modules
    for argument in argument_values:
        if os.path.isfile ("Modules/" + argument):
            modules.append(argument)
        else:
			notification ("Module '%s' not found\n" % argument.replace(".py", ""), "error")

    del argument_values

# Checking if there some modules
if len(modules) == 0:
	notification ("No modules found. Quitting..", "error")
	exit()
else:
	notification ("Running all %s valid modules." % str(len(modules)), "info")

# Executing valid modules
filenames = []
for module in modules:
    notification ("Running module '%s' .." % module.replace(".py", ""), "notify")
    execfile ("Modules/" + module)

    # Checking if the module generated an output (allocated list of filenames to search for)
    if 'output' in locals():
        notification ("'%s' generated \033[1m%s\033[0m possible filenames.\n" % (module.replace(".py", ""), str(len(output))), "success")
        filenames += output
        del output

    else:
        notification ("Invalid module: '%s'" % module.replace(".py", ""), "error")

# If the modules generated some filenames
if len(filenames) > 0:
	# If the user want to output the filenames in a file
	if file_output != "":
		notification ("Writing the generated filenames to '%s'" % file_output, "info")

		try:
			# If the file already exists raise an exception
			if os.path.isfile(file_output) and question_yn ("[\033[1m\033[94m?\033[0m] %s already exists! Do you want to override it" % (file_output)) == 'n':
				raise Exception ('test')

			with open (file_output, "w") as fp:
				for filename in filenames:
					fp.write("%s\n" % filename)

			verbose_message (notification("Number of lines: %s" % str(len(filenames)), "added", False), verbose)
			notification ("File written successfully!\n", "success")
		except:
			notification ("Error writing the file!\n", "error")
        else:
                verbose_message(notification("No output file specified. Proceeding without saving filenames..\n", "added", False), verbose)

	# Asking to the user if he wants to proceed with the test
	if question_yn ("[\033[1m\033[94m?\033[0m] Do you want to test %s filenames on %s" % (str(len(filenames)), url)) == 'n':
		notification ("Stopped\n", "removed")
		exit()

	print

	notification ("Testing all %s generated filenames with %s threads.." % (str(len(filenames)), threads), "info")

	# Allocating shared memory between processes
	queue = Queue()

	# Allocating a pool of N threads
	p = Pool (threads, worker_init, [queue])

	# Creating a partial function with the fixed arguments
	r = partial (requester, url, session_cookie, user_agent, proxy, match)

	# Mapping asynchronously the function on the spawned processes
	workers = p.map_async (r, filenames)

	i = 0
	len_filenames = len(filenames)

	# Accessing the shared memory until something happen
	while 1:
		try:
			if i == len_filenames:
				notification ("File not found. Have you an idea on how to find it? Ask for a feature on \033[94m\033[4mhttps://github.com/0blio/filegps\033[0m.\n", "error")
				break

			# Getting a result from the shared memory
			result = queue.get()

			print "[%s%s%s] %s" % (bcolors.PINK, percentage(i, len_filenames) + "%", bcolors.ENDC, result[0])

			sys.stdout.write("\033[F")
			sys.stdout.write("\033[K")

			if (result[1] == 200 and match == "") or (result[1] == 200 and match != "" and match in result[2]):
				notification ("FileGPS found your file! It is here: \033[4m%s\033[0m.\n" % result[0], "found")
				break
			# Else if fileGPS got a 200 but the response doesn't contain the word to match
			elif result[1] == 200 and match != "" and match not in result[2]:
				notification ("FileGPS found a file (\033[4m%s\033[0m) but the response doesn't contain the word to match." % result[0], "found")


			i += 1
		except KeyboardInterrupt:
			notification ("Stopped", "removed")
			break

	p.terminate()
	p.join()
	exit()
