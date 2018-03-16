from checker_base import Checker_Base

view_aggregate_check_order = ["Num_Missing_Speakable_Test"]#, "Num_Not_Wide_Enough", "Num_Not_Tall_Enough",\
  # "Num_Editable_Textview_Cont_Desc"]

by_app_check_order = []
class App_Checker(Checker_Base):
	def __init__(self, app_arg):
		# the node this checker is checking
		self.app = app_arg
		Checker_Base.__init__(self)

		# in different dict since map to result, not a check object
		# feels overkill to make object for the aggregator checks
		self.view_aggregate_checks = {}

		self.__initialize_checks()


	## SETUP
	## MUST BE RUN IN INIT!!
	def __initialize_checks(self):
		self.view_aggregate_checks["Num_Missing_Speakable_Test"] = self.num_missing_speakable_test()


	### PRINTING

	def print_table(self, table_type):
		if table_type == "BY_APP":
			for c in view_aggregate_check_order:
				print(str(self.view_aggregate_checks[c])+",",end="")
			for c in by_app_check_order:
				print(str(self.checks[c].result)+",",end="")


	def print_debug(self):
		print("ID: "+self.id)

	## MUST BE IN SAME ORDER AS PUT IN __INITIALIZE_CHECKS
	# print aggregate checks first, then by app checks
	@staticmethod
	def print_header():
		# first comes aggregates, order matters
		for c in view_aggregate_check_order:
			print (str(c)+",", end="")
		# then by app checks
		for c in by_app_check_order:
			print (str(c)+",", end="")

	## Compile Node-Based Checks

	# counts number of nodes failing speakable text check
	def num_missing_speakable_test(self):
		result = 0
		for t in self.app.traces.values():
			for v in t.views.values():
				result += v.checker.get_result("Num_Missing_Speakable_Test")
		return result