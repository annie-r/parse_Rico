class Checker_Base():
	def __init__(self):
		# the node this checker is checking
		self.log = []

		# list of node_checks to perform on node
		# in list because want to ensure prints out in order
		self.checks = []
		## TODO: figure out how to do this with inhertiance, I think I'm too classy (hehe) and overcomplicated the structure
		#self.__initialize_checks()

	def __initialize_checks(self):
		raise NotImplementedError()

	def perform_checks(self):
		for check in self.checks:
			check.perform()

	@staticmethod
	def print_header():
		raise NotImplementedError()
