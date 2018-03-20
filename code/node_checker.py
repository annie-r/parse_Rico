from checker_base import Checker_Base
from speakable_text_present_check import Speakable_Text_Present_Check
from element_height_check import Element_Height_Check
from element_width_check import Element_Width_Check
from cont_desc_editable_textview_check import Cont_Desc_Editable_Textview_Check

check_order = ["Speakable_Text_Present","Element_Wide_Enough","Element_Tall_Enough","Editable_Textview_With_Cont_Desc"]

# some per node checks can only be set by the view because need know about other nodes
# so initilize here but will be set by view
view_set_checks_order = ["Num_Nodes_Overlap_With", "Num_Nodes_Share_Label"]
class Node_Checker(Checker_Base):
	def __init__(self, node_arg):
		# the node this checker is checking
		self.node = node_arg
		Checker_Base.__init__(self)

		self.view_set_checks = {}

		self.__initialize_checks()
	## MUST BE RUN IN INIT!!
	def __initialize_checks(self):
		# some tests only to be performed on talkback accessible nodes
		# test objects know if they are talkback accessible applicable
		# must do on all nodes so that if we print all nodes, the columns are meaningful
		# if not applicable, result will be na
		# TODO: this is not memory effective, may have to restructure the is accessible check before creating

		## MUST ADD TO ABOVE check_order
		self.checks["Speakable_Text_Present"] = (Speakable_Text_Present_Check("Speakable_Text_Present",self.node))
		self.checks["Element_Wide_Enough"]=(Element_Width_Check("Element_Wide_Enough",self.node))
		self.checks["Element_Tall_Enough"]=(Element_Height_Check("Element_Tall_Enough",self.node))
		self.checks["Editable_Textview_With_Cont_Desc"]=(Cont_Desc_Editable_Textview_Check("Editable_Textview_With_Cont_Desc",self.node))

		for c in view_set_checks_order:
			self.view_set_checks[c] = None

	def print_table(self, table_type,fd):
		# print order:
		# has_speakable_text_present,
		if table_type == "BY_NODE":
			# result will be "na" if test isn't applicable
			for c in check_order:
				fd.write(str(self.checks[c].result)+",")
			for c in view_set_checks_order:
				fd.write(str(self.view_set_checks[c])+",")


	## MUST BE IN SAME ORDER AS PUT IN __INITIALIZE_CHECKS
	@staticmethod
	def print_header(fd):
		for c in check_order:
			fd.write(str(c)+",")
		for c in view_set_checks_order:
			fd.write(str(c)+",")
		# print("Speakable_Text_Present,", end="")
		# print("Element_Wide_Enough,",end="")
		# print("Element_Tall_Enough,",end="")
		# print("Editable_Textview_With_Cont_Desc",end="")
