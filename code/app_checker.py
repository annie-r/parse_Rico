from checker_base import Checker_Base
# MUST ADD AGGREGATE CHECK HERE AND PERFORM CHECK IN __run_aggregate_tests()
# if needs to be initialized to something other than 0, must set in initialize checks
view_aggregate_check_order = ["Num_Missing_Speakable_Test", "Num_Not_Wide_Enough", "Num_Not_Tall_Enough",\
    "Num_Editable_Textview_Cont_Desc"]

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
		self.__run_aggregate_tests()


	## SETUP
	## MUST BE RUN IN INIT!!
	def __initialize_checks(self):
		for ag_check in view_aggregate_check_order:
			self.view_aggregate_checks[ag_check] = 0


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

	## View-Based Aggregated Per App Checks
	def __run_aggregate_tests(self):
		for t in self.app.traces.values():
			for v in t.views.values():
				# counts number of nodes failing speakable text check
				self.view_aggregate_checks["Num_Missing_Speakable_Test"] += v.checker.get_result("Num_Missing_Speakable_Test")
				self.view_aggregate_checks["Num_Not_Wide_Enough"] += v.checker.get_result("Num_Not_Wide_Enough")
				self.view_aggregate_checks["Num_Not_Tall_Enough"] += v.checker.get_result("Num_Not_Tall_Enough")
				self.view_aggregate_checks["Num_Editable_Textview_Cont_Desc"] += v.checker.get_result("Num_Editable_Textview_Cont_Desc")
