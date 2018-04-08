from checker_base import Checker_Base
from num_nodes_accessible_in_trace_check import Num_Nodes_Accessible_In_Trace_Check

check_order = ["NUM_TALKBACK_INACCESSIBLE_NODES"]

# some per node checks can only be set by the view because need know about other nodes
# so initilize here but will be set by view
view_set_checks_order = []
class Trace_Checker(Checker_Base):
	def __init__(self, trace_arg):
		# the node this checker is checking
		self.trace = trace_arg
		Checker_Base.__init__(self)

		#self.view_set_checks = {}

		self.__initialize_checks()
	## MUST BE RUN IN INIT!!
	def __initialize_checks(self):
		# some tests only to be performed on talkback accessible nodes
		# test objects know if they are talkback accessible applicable
		# must do on all nodes so that if we print all nodes, the columns are meaningful
		# if not applicable, result will be na
		# TODO: this is not memory effective, may have to restructure the is accessible check before creating

		## MUST ADD TO ABOVE check_order
		self.checks["NUM_TALKBACK_INACCESSIBLE_NODES"] = Num_Nodes_Accessible_In_Trace_Check("NUM_TALKBACK_INACCESSIBLE_NODES",self.trace)

	def print_table(self, table_type,fd):
		# print order:
		if table_type == "BY_TRACE":
			# result will be "na" if test isn't applicable
			for c in check_order:
				fd.write(str(self.checks[c].get_result())+",")
				if len(self.trace.gestures) == 0:
					percent = "na"
				else:
					percent = self.checks[c].get_result() / len(self.trace.gestures)
				fd.write(str(percent)+",")
			#for c in view_set_checks_order:
			#	fd.write(str(self.view_set_checks[c])+",")


	## MUST BE IN SAME ORDER AS PUT IN __INITIALIZE_CHECKS
	@staticmethod
	def print_header(fd):
		for c in check_order:
			fd.write(str(c)+",")
			## LEFT HERE
			fd.write(str(c)+"_percent_clicks,")
		#for c in view_set_checks_order:
		#	fd.write(str(c)+",")
		# print("Speakable_Text_Present,", end="")
		# print("Element_Wide_Enough,",end="")
		# print("Element_Tall_Enough,",end="")
		# print("Editable_Textview_With_Cont_Desc",end="")
