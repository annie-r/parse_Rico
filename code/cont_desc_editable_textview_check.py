from node_check_base import Node_Check_Base 
import talkback_accessible

class Cont_Desc_Editable_Textview_Check(Node_Check_Base):

	def __init__(self, id_arg, node_arg):
		Node_Check_Base.__init__(self,id_arg, node_arg)

	def perform(self):
		# not applicable to non-textviews or non-focusable textviews
		if self.node.is_talkback_accessible() and self.node.is_editable_textview():
			self.result = self.__cont_desc_editable_textview()
		else:
			self.result = "na"
		
	

	#####
	## Check content desc in TextView
	## editable image label
	#####

	# TODO, check if this is right class to check!
	# check if inherits from android.widget.EditText
	# should use get_role but don't know if just check class or inheritance
	def __cont_desc_editable_textview(self):
		if self.node.is_editable_textview() and (self.node.get_cont_desc()!= None):
			return True
		return False



