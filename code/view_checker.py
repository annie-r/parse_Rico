
class View_Checker:
	def __init__(self, view_arg):
		# the hierachy this checker is checking
		self.view = view_arg
		self.log = []


		# set of Checks that are to be performed
		# maps Check object to the overall_check result, aka Labeled check to num_unlabeled
		self.checks = {}

	def add_check(self, check):
		self.checks[check] = {check.get_id(), check.get_default_overall()}
