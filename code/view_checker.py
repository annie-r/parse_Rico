from checker_base import Checker_Base

node_aggregate_check_order = ["Num_Missing_Speakable_Test"]#, "Num_Not_Wide_Enough", "Num_Not_Tall_Enough",\
  # "Num_Editable_Textview_Cont_Desc"]

by_view_check_order = []

class View_Checker(Checker_Base):
	def __init__(self, view_arg):
		# the node this checker is checking
		self.view = view_arg
		Checker_Base.__init__(self)

		# in different dict since map to result, not a check object
		# feels overkill to make object for the aggregator checks
		self.node_aggregate_checks = {}

		self.__initialize_checks()


	## SETUP
	## MUST BE RUN IN INIT!!
	def __initialize_checks(self):
		self.node_aggregate_checks["Num_Missing_Speakable_Test"] = self.num_missing_speakable_test()


	### PRINTING

	def print_table(self, table_type):
		if table_type == "BY_APP":
			for c in node_aggregate_check_order:
				print(str(self.node_aggregate_checks[c])+",",end="")
			for c in by_view_check_order:
				print(str(self.checks[c].result)+",",end="")

	# need to add checking aggregate checks not just per_app checks
	def get_result(self, check_name):
		if check_name in self.node_aggregate_checks.keys():
			return self.node_aggregate_checks[check_name]
		else:
			Checker_Base.get_result(self,check_name)

	def print_debug(self):
		print("ID: "+self.id)

	## MUST BE IN SAME ORDER AS PUT IN __INITIALIZE_CHECKS
	# print aggregate checks first, then by app checks
	@staticmethod
	def print_header():
		# first comes aggregates, order matters
		for c in node_aggregate_check_order:
			print (str(c)+",", end="")
		# then by app checks
		for c in by_view_check_order:
			print (str(c)+",", end="")

	## Compile Node-Based Checks

	# counts number of nodes failing speakable text check
	def num_missing_speakable_test(self):
		result = 0
		for n in self.view.nodes:
			if not n.checker.get_result("Speakable_Text_Present"):
				result +=1
		return result