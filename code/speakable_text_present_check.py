from node_check_base import Node_Check_Base 
import talkback_accessible

class Speakable_Text_Present_Check(Node_Check_Base):

	def __init__(self, id_arg, node_arg):
		Node_Check_Base.__init__(self,id_arg, node_arg)

	# this check only checks if it has a label, that is, if it's label (
	# be it personal label or from children, is not None
	# this is only applicable to talkback_accessible nodes
	def perform(self):
		### Label check
		# if talkback accessible, should have appropriate label
		# don't check on webviews
		if self.node.is_talkback_accessible() and (not self.node.is_webview()) and (not self.node.is_editable_textview()):
			self.result = self.__has_label()
		else:
			self.result = "NA"

	#####
	### Check Label
	#####

	def __has_label(self):
		# Special case for web content.
		if self.node.has_webAction():
			return True
		# TODO special case for checkable
		if self.node.is_checkable():
			return True
		#print("\ntest: "+(self.node.get_resource_id()))
		return self.node.get_speakable_text() != None

