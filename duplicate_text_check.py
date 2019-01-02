from check_base import Check_Base 
import talkback_accessible

class Duplicate_Text_Check(Check_Base):

	def __init__(self, id_arg, node_arg):
		Check_Base.__init__(self,id_arg, node_arg)

	# this check only checks if it has a label, that is, if it's label (
	# be it personal label or from children, is not None

	def perform(self):
		### Label check
		# if talkback accessible, should have appropriate label
		self.result = self.__has_label()


	#####
	## Check identical speakable text
	## item descriptions
	# /** Accessitility-Test-framework-for-android DuplicateSpeakableTextViewHierarchyCheck
 	# If two Views in a hierarchy have the same speakable text, that could be confusing for users. Two
 	# Views with the same text, and at least one of them is clickable we warn in that situation. If we
 	# find two non-clickable Views with the same speakable text, we report that fact as info. If no
 	# Views in the hierarchy have any speakable text, we report that the test was not run.
	#####

	def __duplicate_text_check(self):
		# find all text and views that have text
		speakable_text_to_node_map = {}
		for node in self.nodes:
			text = talkbackAccessible.get_speaking_text(node)
			if text != None:
				if not text in speakable_text_to_node_map:
					speakable_text_to_node_map[text] = []
				speakable_text_to_node_map[text].append(node)
		# deal with duplicates
		for speakable_text in speakable_text_to_node_map.keys():
			# not duplicate
			if(len(speakable_text_to_node_map[speakable_text]) < 2):
				continue
			# sort into clickable and non clickable
			clickable = []
			non_clickable = []
			for n in speakable_text_to_node_map[speakable_text]:
				if (talkbackAccessible.is_clickable(n)):
					clickable.append(n)
				else:
					non_clickable.append(n)
			# if it's clickable, it's a warning
			# if it's not, then it's just info
			# so for now count as separate checks
			# line 69, accessibility test framework, proto, duplicatespeakabletextviewhierarchycheck
			# shares with clickable
			if len(clickable) > 0:
				self.overall_checks['num_shares_label_clickable'] = len(clickable) 
				self.log.append("duplicate clickable label: "+ str(speakable_text))
			# duplication is on non-clickable
			# don't know why -1, in framework code
			else:
				self.overall_checks['num_shares_label_non_clickable'] = len(non_clickable) - 1 
				self.log.append("duplicate non clickable label: "+ str(speakable_text))
