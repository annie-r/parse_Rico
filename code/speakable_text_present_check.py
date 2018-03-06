from check_base import Check_Base 
import talkback_accessible

class Speakable_Text_Present_Check(Check_Base):

	def __init__(self, node_arg):
		Check_Base.__init__(self,node_arg,"Speakable_Text_Present")
		self.result = self.__has_label()

	def perform(self):
		### Label check
		# if talkback accessible, should have appropriate label
		return self.__has_label()

	#####
	### Check Label
	#####

	def __has_label(self):
		return self.node.get_speakable_text() != None

