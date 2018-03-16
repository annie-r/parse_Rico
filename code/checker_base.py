class Checker_Base():
	def __init__(self):
		# the node this checker is checking
		self.log = []

		# list of node_checks to perform on node
		# map test name to test object
		self.checks = {}
		## TODO: figure out how to do this with inhertiance, I think I'm too classy (hehe) and overcomplicated the structure
		#self.__initialize_checks()

	def __initialize_checks(self):
		raise NotImplementedError()

	def perform_checks(self):
		for check in self.checks.values():
			check.perform()

	def get_result(self, check_name):
		if check_name not in self.checks.keys():
			raise AssertionError("No such node check: "+str(check_name))
		return self.checks[check_name].result

	def print_table(self,table_type):
		raise NotImplementedError()

	@staticmethod
	def print_header():
		raise NotImplementedError()
