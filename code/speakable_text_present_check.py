from check_base import Check_Base 
import talkback_accessible

class Speakable_Text_Present_Check(Check_Base):

	def __init__(self, node_arg):
		Check_Base.__init__(self,node_arg,"Speakable_Text_Present")

	# this check only checks if it has a label, that is, if it's label (
	# be it personal label or from children, is not None

	def perform(self):
		### Label check
		# if talkback accessible, should have appropriate label
		self.result = self.__has_label()

	#####
	### Check Label
	#####

	def __has_label(self):
		#print("\ntest: "+(self.node.get_resource_id()))
		return self.node.get_speakable_text() != None

