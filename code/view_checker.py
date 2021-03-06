from checker_base import Checker_Base
from num_clickable_full_overlap_check import Num_Clickable_Full_Overlap_Check
from duplicate_text_clickable_check import Duplicate_Text_Clickable_Check
from duplicate_text_non_clickable_check import Duplicate_Text_Non_Clickable_Check
# MUST ADD AGGREGATE CHECK HERE AND PERFORM CHECK IN __run_aggregate_tests()
# if needs to be initialized to something other than 0, must set in initialize checks
node_aggregate_check_order = ["Num_Missing_Speakable_Text", "Num_Not_Wide_Enough", "Num_Not_Tall_Enough",\
  "Num_Editable_Textview_Cont_Desc", "Num_Redundant_Description"]

by_view_check_order = ["Num_Fully_Overlapping_Clickable", "Num_Clickable_Duplicate_Text","Num_Non_Clickable_Duplicate_Text"]

class View_Checker(Checker_Base):
	def __init__(self, view_arg):
		# the node this checker is checking
		self.view = view_arg
		Checker_Base.__init__(self)

		# in different dict since map to result, not a check object
		# feels overkill to make object for the aggregator checks
		self.node_aggregate_checks = {}
		#self.node_aggregate_checks_denom
		self.__initialize_checks()

		# to not have to do the same loop repeatedly
		self.__run_aggregate_tests()



	## SETUP
	## MUST BE RUN IN INIT!!
	def __initialize_checks(self):
		for ag_check in node_aggregate_check_order:
			self.node_aggregate_checks[ag_check] = {"count":0,"denom":0}

		self.checks["Num_Fully_Overlapping_Clickable"] = Num_Clickable_Full_Overlap_Check("Num_Fully_Overlapping_Clickable", self.view)
		self.checks["Num_Clickable_Duplicate_Text"] = Duplicate_Text_Clickable_Check("Num_Clickable_Duplicate_Text",self.view)
		self.checks["Num_Non_Clickable_Duplicate_Text"] = Duplicate_Text_Non_Clickable_Check("Num_Non_Clickable_Duplicate_Text",self.view)

	### PRINTING

	def print_table(self, table_type, fd):
		if table_type == "BY_APP":
			for c in node_aggregate_check_order:
				fd.write(str(self.node_aggregate_checks[c])+",")
			for c in by_view_check_order:
				fd.write(str(self.checks[c].result)+",")

	# need to add checking aggregate checks not just per_app checks
	#returns a dict if from agg checks
	# else just returns value (may need to rethink that, but we're at the point of making it work!
	def get_result(self, check_name):
		if check_name in self.node_aggregate_checks.keys():
			return self.node_aggregate_checks[check_name]
		else:
			return Checker_Base.get_result(self,check_name)

	def print_debug(self,fd):
		fd.write("num full overlap:" + str(self.checks['Num_Fully_Overlapping_Clickable'].result)+"\n")
		fd.write("num clickable dupl: "+ str(self.checks['Num_Clickable_Duplicate_Text'].result)+"\n")

	## MUST BE IN SAME ORDER AS PUT IN __INITIALIZE_CHECKS
	# print aggregate checks first, then by app checks
	@staticmethod
	def print_header(fd):
		# first comes aggregates, order matters
		for c in node_aggregate_check_order:
			fd.write(str(c)+",")
		# then by app checks
		for c in by_view_check_order:
			fd.write(str(c)+",")

	## Compile Node-Based Checks

	# counts number of nodes failing speakable text check
	# each test in node_aggregator_test_order must have entry here!
	def __run_aggregate_tests(self):
		#!!!!!! ## DO COUNTS HERE!! COUNT TRUE AND FALSE FOR ALL TO GET DENOMINATOR

		for n in self.view.nodes:
			# REMEBER, results can be na if not applicable
			# so making checks explicit (== True) to reduce errors
			# count num of nodes in this view with missing speakable text

			## count True and False to get accurate demoninator of tested elements
			if n.checker.get_result("Speakable_Text_Present") == False:
				self.node_aggregate_checks["Num_Missing_Speakable_Text"]["count"] += 1
				self.node_aggregate_checks["Num_Missing_Speakable_Text"]["denom"] += 1
			else:
				self.node_aggregate_checks["Num_Missing_Speakable_Text"]["denom"] += 1

			if n.checker.get_result("Element_Wide_Enough") == False:
				self.node_aggregate_checks["Num_Not_Wide_Enough"]["count"] += 1
				self.node_aggregate_checks["Num_Not_Wide_Enough"]["denom"] += 1
			else:
				self.node_aggregate_checks["Num_Not_Wide_Enough"]["denom"] += 1

			if n.checker.get_result("Element_Tall_Enough") == False:
				self.node_aggregate_checks["Num_Not_Tall_Enough"]["count"] += 1
				self.node_aggregate_checks["Num_Not_Tall_Enough"]["denom"] += 1
			else:
				self.node_aggregate_checks["Num_Not_Tall_Enough"]["denom"] += 1

			# this one's node check counts the undesired trait, the ones above count the positives
			if n.checker.get_result("Editable_Textview_With_Cont_Desc") == True:
				self.node_aggregate_checks["Num_Editable_Textview_Cont_Desc"]["count"] += 1
				self.node_aggregate_checks["Num_Editable_Textview_Cont_Desc"]["denom"] += 1
			else:
				self.node_aggregate_checks["Num_Editable_Textview_Cont_Desc"]["denom"] += 1

			if n.checker.get_result("Has_Redundant_Description") == True:
				self.node_aggregate_checks["Num_Redundant_Description"]["count"] += 1
				self.node_aggregate_checks["Num_Redundant_Description"]["denom"] += 1
			else:
				self.node_aggregate_checks["Num_Redundant_Description"]["denom"] += 1