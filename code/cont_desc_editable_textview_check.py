from node_check_base import Node_Check_Base 
import talkback_accessible

class Cont_Desc_Editable_Textview_Check(Node_Check_Base):

	def __init__(self, id_arg, node_arg):
		Node_Check_Base.__init__(self,id_arg, node_arg)

	# this check only checks if it has a label, that is, if it's label (
	# be it personal label or from children, is not None

	def perform(self):
		### Label check
		# if talkback accessible, should have appropriate label
		self.result = self.__cont_desc_editable_textview()
	

	#####
	## Check content desc in TextView
	## editable image label
	#####

	# TODO, check if this is right class to check!
	# check if inherits from android.widget.EditText
	# should use get_role but don't know if just check class or inheritance
	def __cont_desc_editable_textview(self):
		if self.__is_editable_textview() and (self.node.get_cont_desc()!= None):
			return True
		return False

	def __is_editable_textview(self):
		ancestors = self.node.raw_properties['ancestors']
		if "android.widget.EditText" in ancestors:
			return True
		return False


