from checker_base import Checker_Base
# MUST ADD AGGREGATE CHECK HERE AND PERFORM CHECK IN __run_aggregate_tests()
# if needs to be initialized to something other than 0, must set in initialize checks
view_aggregate_check_order = ["Num_Missing_Speakable_Test", "Num_Not_Wide_Enough", "Num_Not_Tall_Enough",\
    "Num_Editable_Textview_Cont_Desc","Num_Fully_Overlapping_Clickable","Num_Clickable_Duplicate_Text", \
							  "Num_Non_Clickable_Duplicate_Text", "Num_Redundant_Description"]

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

	def print_table(self, table_type,fd):
		if table_type == "BY_APP":
			# print by percentage
			ag_group_type = None
			for c in view_aggregate_check_order:
				fd.write(str(self.view_aggregate_checks[c])+",")
				# these checks apply to all elements
				if c == "Num_Missing_Speakable_Test" or c == "Num_Not_Wide_Enough" or c== "Num_Not_Tall_Enough":
					ag_group_type = "TALKBACK"
				elif c == "Num_Editable_Textview_Cont_Desc":
					ag_group_type = "EDITABLE_TEXTVIEW"
				elif c == "Num_Fully_Overlapping_Clickable" or c == "Num_Clickable_Duplicate_Text":
					ag_group_type = "CLICKABLE"
				elif c == "Num_Non_Clickable_Duplicate_Text":
					ag_group_type = "NON_CLICKABLE"
				elif c == "Num_Redundant_Description":
					ag_group_type = "HAVE_CONT_DESC"
				else:
					raise NameError("Aggregate Test: "+str(c)+" does not have aggregate to get percentage defined")

				if self.app.get_num_nodes_by_type(ag_group_type) == 0:
						fd.write("na,")
				else:
					per_node = self.view_aggregate_checks[c] / self.app.get_num_nodes_by_type(ag_group_type)
					fd.write(str(per_node)+",")
			for c in by_app_check_order:
				fd.write(str(self.checks[c].result)+",")


	def print_debug(self):
		print("ID: "+self.id)

	## MUST BE IN SAME ORDER AS PUT IN __INITIALIZE_CHECKS
	# print aggregate checks first, then by app checks
	@staticmethod
	def print_header(fd):
		# first comes aggregates, order matters
		for c in view_aggregate_check_order:
			fd.write(str(c)+",")
			fd.write(str(c)+"_Per_Node,")
		# then by app checks
		for c in by_app_check_order:
			fd.write(str(c)+",")

	## View-Based Aggregated Per App Checks
	def __run_aggregate_tests(self):
		for t in self.app.traces.values():
			for v in t.views.values():
				# counts number of nodes failing speakable text check
				self.view_aggregate_checks["Num_Missing_Speakable_Test"] += v.checker.get_result("Num_Missing_Speakable_Test")
				self.view_aggregate_checks["Num_Not_Wide_Enough"] += v.checker.get_result("Num_Not_Wide_Enough")
				self.view_aggregate_checks["Num_Not_Tall_Enough"] += v.checker.get_result("Num_Not_Tall_Enough")
				self.view_aggregate_checks["Num_Editable_Textview_Cont_Desc"] += v.checker.get_result("Num_Editable_Textview_Cont_Desc")
				self.view_aggregate_checks["Num_Fully_Overlapping_Clickable"] += v.checker.get_result("Num_Fully_Overlapping_Clickable")
				self.view_aggregate_checks["Num_Clickable_Duplicate_Text"] += v.checker.get_result("Num_Clickable_Duplicate_Text")
				self.view_aggregate_checks["Num_Non_Clickable_Duplicate_Text"] += v.checker.get_result("Num_Non_Clickable_Duplicate_Text")
				self.view_aggregate_checks["Num_Redundant_Description"] += v.checker.get_result("Num_Redundant_Description")