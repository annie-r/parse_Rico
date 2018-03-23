from node_check_base import Node_Check_Base

class Redundant_Description_Check(Node_Check_Base):

###
## based on accessibility test framework 3.0 accessed 3_23_2018
###
 # Checks to ensure that speakable text does not contain redundant information about the view's
 # type. Accessibility services are aware of the view's type and can use that information as needed
 # (ex: Screen readers may append "button" to the speakable text of a {@link Button}).
 #
	def __init__(self, id_arg, node_arg):
		Node_Check_Base.__init__(self,id_arg, node_arg)
		# must be lowercase
		self.redundant_words = ["button"]

	def perform(self):
		if (not self.node.is_talkback_accessible()):
			self.result = "na"
		# TODO: can't check for language
		else:
			cont_desc = self.node.get_cont_desc()
			if cont_desc == None:
				self.result = "na"

			# check if cont description includes redundant words
			else:
				cont_desc = cont_desc.encode('ascii','ignore')
				cont_desc = cont_desc.lower()
				self.result = False
				for word in self.redundant_words:
					if word in str(cont_desc):
						self.result = True

