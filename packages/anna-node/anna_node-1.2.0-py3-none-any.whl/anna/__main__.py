#!/usr/bin/env python3

import argparse

import anna.worker
from anna_client.client import Client

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='End-to-end testing using selenium')
	parser.add_argument('-d', '--driver', required=True, help='The name of the driver to use. Currently only supports '
															  'chrome, firefox & ie. However, if run using the '
															  'API, you\'ll only be able to test chrome & firefox '
															  'since there isn\'t a docker container for selenium with '
															  'ie.')
	parser.add_argument('-s', '--site', required=True,
						help='Names of the sites to test (separate by space).')
	parser.add_argument('-v', '--verbose', action='store_true', help='Print exceptions and stack traces while running.')
	parser.add_argument('-H', '--headless', action='store_true', help='Run drivers in headless mode.')
	parser.add_argument('-r', '--resolution', required=False, help='Set the driver resolution (defaults to 1920x1080).')
	parser.add_argument('-t', '--token', required=False, help='Set the API token.')
	parser.add_argument('--host', required=True, help='Set the API host.')
	args = vars(parser.parse_args())
	worker = anna.worker.Worker(args)
	client = Client(endpoint=args['host'])
	try:
		url, tasks = client.get_tasks(namespace=args['site'])
		worker.run(url=url, tasks=tasks)
		worker.close()
	except ImportError:
		print('unable to fetch tasks for the specified site: ' + args['site'])
