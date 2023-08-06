import sys, traceback, os
from pprint import pprint
from typing import List

import anna.colors as colors
from anna_lib.selenium import driver
from anna_lib.task.abstract_task import AbstractTask
from anna_lib.task.factory import load_task


class Worker:
	tasks: List
	task: AbstractTask

	def __init__(self, options: dict):
		self.passed = None
		self.tasks = []
		self.driver = None
		self.options = options
		if self.options['resolution'] is None:
			self.options['resolution'] = (1920, 1080)
		else:
			self.options['resolution'] = tuple(int(a) for a in self.options['resolution'].split('x'))

	def close(self):
		self.driver.close()

	def run(self, url: str, tasks: list):
		self.driver = driver.create(driver=self.options['driver'], headless=self.options['headless'],
									resolution=self.options['resolution'])
		self.driver.get(url)
		for task in tasks:
			name, task = load_task(self.driver, task)
			self.execute_task(url, name, task)
			self.tasks.append(task)
		self.print_result()

	def execute_task(self, url, name, task):
		self.task = task
		print('Running %s @ %s on %s' % (name, url, self.driver.name))
		try:
			task.execute()
		except KeyboardInterrupt:
			return
		except:
			self.handle_exception(task)
		self.screenshot(name)
		if task.passed:
			print(colors.green + 'passed' + colors.white)
		else:
			self.passed = False
			print(colors.red + 'failed' + colors.white)

	def print_result(self):
		if self.options['verbose']:
			self.print_task_summary()
		passed = len([task for task in self.tasks if task.passed])
		if self.passed is None:
			self.passed = passed == len(self.tasks)
		print(str(passed) + '/' + str(len(self.tasks)))

	def print_task_summary(self):
		print(colors.red)
		for task in self.tasks:
			self.print_task_result(task)
		print(colors.white)

	@staticmethod
	def print_task_result(task):
		if not task.passed:
			pprint(task.result)

	def handle_exception(self, task):
		task.passed = False
		task.result = traceback.format_exc()
		if self.options['verbose']:
			traceback.print_exc(file=sys.stdout)

	def screenshot(self, name):
		screenshot_dir = self.get_screenshot_dir()
		try:
			os.makedirs(screenshot_dir)
		except FileExistsError:
			pass
		except IOError:
			return False
		file = screenshot_dir + '/' + name + '.png'
		return self.driver.get_screenshot_as_file(file)

	@staticmethod
	def get_screenshot_dir():
		return '/tmp/anna/'
