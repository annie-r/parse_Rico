from checker_base import Checker_Base
# MUST ADD AGGREGATE CHECK HERE AND PERFORM CHECK IN __run_aggregate_tests()
# if needs to be initialized to something other than 0, must set in initialize checks
view_aggregate_check_order = ["Num_Missing_Speakable_Text", "Num_Not_Wide_Enough", "Num_Not_Tall_Enough",\
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
			self.view_aggregate_checks[ag_check] = {"count":0,"denom":0}


	### PRINTING

	def print_table(self, table_type,fd):
		if table_type == "BY_APP":
			# print by percentage
			ag_group_type = None
			for c in view_aggregate_check_order:
				fd.write(str(self.view_aggregate_checks[c]["count"])+",")
				denominator = self.view_aggregate_checks[c]["denom"]

				## SINCE ONLY FIXED THE NON-AGGREGATE TESTS IN VIEW, HAVE TO TREAT DIFF
				# these checks apply to all elements
				# if c == "Num_Missing_Speakable_Text":
				# 	ag_group_type = "WEBVIEW"
				# elif c == "Num_Not_Wide_Enough" or c== "Num_Not_Tall_Enough":
				# 	ag_group_type = "TALKBACK"
				# elif c == "Num_Editable_Textview_Cont_Desc":
				# 	ag_group_type = "EDITABLE_TEXTVIEW"
				#if c == "Num_Fully_Overlapping_Clickable" or c == "Num_Clickable_Duplicate_Text":
				#	ag_group_type = "CLICKABLE"
				#elif c == "Num_Non_Clickable_Duplicate_Text":
				#	ag_group_type = "NON_CLICKABLE"
				#else:
				#	ag_group_type = None
				# elif c == "Num_Redundant_Description":
				# 	ag_group_type = "HAVE_CONT_DESC"
				# else:
				# 	raise NameError("Aggregate Test: "+str(c)+" does not have aggregate to get percentage defined")
				#if (ag_group_type == None):
				#	denominator = self.view_aggregate_checks[c]["denom"]
				#else:
				#	denominator = self.app.get_num_nodes_by_type(ag_group_type)
				# if ag_group_type == "WEBVIEW":
				# 	# for speakable text exclude webview nodes
				# 	denominator = self.app.get_num_nodes_by_type("TALKBACK") - self.app.get_num_nodes_by_type("WEBVIEW")
				# else:
				# 	denominator = self.app.get_num_nodes_by_type(ag_group_type)

				fd.write(str(denominator)+",")

				if denominator == 0:
						fd.write("na,")
				else:
					per_node = self.view_aggregate_checks[c]["count"] / denominator
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
			fd.write("total_checks_"+str(c)+",")
			fd.write(str(c)+"_Per_Node,")
		# then by app checks
		for c in by_app_check_order:
			fd.write(str(c)+",")

	## View-Based Aggregated Per App Checks
	def __run_aggregate_tests(self):
		for t in self.app.traces.values():
			for v in t.views.values():
				#for check in view_aggregate_check_order:
				#	print(check)
				#	self.view_aggregate_checks[check]["count"] += v.checker.get_result(check)["count"]
				# may need to go back to this way if it goes weird (like the checks are named diff things in the view checker
				# counts number of nodes failing speakable text check

				self.view_aggregate_checks["Num_Missing_Speakable_Text"]["count"] += v.checker.get_result("Num_Missing_Speakable_Text")["count"]
				self.view_aggregate_checks["Num_Missing_Speakable_Text"]["denom"] += v.checker.get_result("Num_Missing_Speakable_Text")["denom"]

				self.view_aggregate_checks["Num_Not_Wide_Enough"]["count"] += v.checker.get_result("Num_Not_Wide_Enough")["count"]
				self.view_aggregate_checks["Num_Not_Wide_Enough"]["denom"] += v.checker.get_result("Num_Not_Wide_Enough")["denom"]

				self.view_aggregate_checks["Num_Not_Tall_Enough"]["count"] += v.checker.get_result("Num_Not_Tall_Enough")["count"]
				self.view_aggregate_checks["Num_Not_Tall_Enough"]["denom"] += v.checker.get_result("Num_Not_Tall_Enough")["denom"]

				self.view_aggregate_checks["Num_Editable_Textview_Cont_Desc"]["count"] += v.checker.get_result("Num_Editable_Textview_Cont_Desc")["count"]
				self.view_aggregate_checks["Num_Editable_Textview_Cont_Desc"]["denom"] += v.checker.get_result("Num_Editable_Textview_Cont_Desc")["denom"]

				self.view_aggregate_checks["Num_Redundant_Description"]["count"] += v.checker.get_result("Num_Redundant_Description")["count"]
				self.view_aggregate_checks["Num_Redundant_Description"]["denom"] += v.checker.get_result("Num_Redundant_Description")["denom"]

				## DIDn'T FIX ALL TESTS IN VIEW
				self.view_aggregate_checks["Num_Fully_Overlapping_Clickable"]["count"] += v.checker.get_result("Num_Fully_Overlapping_Clickable")
				# just = not += because already agg number
				self.view_aggregate_checks["Num_Fully_Overlapping_Clickable"]["denom"] = self.app.get_num_nodes_by_type("CLICKABLE")

				self.view_aggregate_checks["Num_Clickable_Duplicate_Text"]["count"] += v.checker.get_result("Num_Clickable_Duplicate_Text")
				self.view_aggregate_checks["Num_Clickable_Duplicate_Text"]["denom"] = self.app.get_num_nodes_by_type("CLICKABLE")

				self.view_aggregate_checks["Num_Non_Clickable_Duplicate_Text"]["count"] += v.checker.get_result("Num_Non_Clickable_Duplicate_Text")
				self.view_aggregate_checks["Num_Non_Clickable_Duplicate_Text"]["denom"] = self.app.get_num_nodes_by_type("NON_CLICKABLE")
