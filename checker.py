## checks for accessibility barriers on RICO dataset 

import talkbackAccessible 
import re

# class for keeping track of overall checking results
# and for performing individual tests on all nodes
# TODO: make file checker and app checker
class Checker:
	# initialize all overall checks
	# git test
	def __init__(self, file):
		self.file = file

		self.overall_checks = {}
		self.log = []

		# must add overall check here and initialize in order
		# to track later
		self.overall_checks['num_unlabeled']=0
		self.overall_checks['num_talkback_accessible']=0
		self.overall_checks['num_elements']=0
		self.overall_checks['num_not_wide_enough']=0
		self.overall_checks['num_not_tall_enough']=0
		self.overall_checks['num_not_wide_tall_enough']=0
		self.overall_checks['num_full_overlapping']=0
		self.overall_checks['num_cont_desc_editable_textview'] =0

		#all nodes associated with TODO: screen? app? trace?
		self.nodes = []

	# TODO
	def print_overall_checks(self):
		print("OVERALL CHECKS")
		for k,v in self.overall_checks.items():
			print(str(k) + ": "+ str(v))


	def print_log(self):
		print ("CHECKER LOG")
		for v in set(self.log):
			print(str(v))
	# Modifiers
	def add_overall_check(self, key, value):
		self.overall_checks[key] = value

	def add_node(self, node):
		self.nodes.append(node)
		self.overall_checks['num_elements'] += 1


	###########
	## CHECKS
	###########

	# takes care of all tests over all nodes
	def perform_checks(self):
		# data needed for checks involving multiple nodes
		self.set_clickable_nodes()

		#perform checks on each node
		for node in self.nodes:
			# tests to run on talkback accessible nodes
			if node.characteristics['talkback_accessible']:
				self.overall_checks['num_talkback_accessible'] += 1 
				self.run_talkback_accessible_checks(node)


	def set_clickable_nodes(self):
		self.clickable_nodes = []
		for n in self.nodes:
			if talkbackAccessible.is_clickable(n):
				self.clickable_nodes.append(n)


	def run_talkback_accessible_checks(self,node):

		### Size check
		# only clickable or touchable nodes need to be checked for size
		if talkbackAccessible.is_clickable(node):
			node.checks['wide_enough'] = self.wide_enough(node)
			node.checks['tall_enough'] = self.tall_enough(node)
			if (not node.checks['wide_enough'] and not node.checks['tall_enough']):
				self.overall_checks['num_not_wide_tall_enough'] += 1
			elif (not node.checks['wide_enough']):
				self.overall_checks['num_not_wide_enough'] += 1
			elif (not node.checks['tall_enough']):
				self.overall_checks['num_not_tall_enough'] += 1

		### Label check
		# if talkback accessible, should have appropriate label
		node.checks['has_label'] = self.has_label(node)
		if (not node.checks['has_label']):
			self.overall_checks['num_unlabeled'] += 1

		### Full Overlap check
		# only clickable items need to check for full overlap
		if node in self.clickable_nodes:
			node.checks['num_full_overlap'] = self.full_overlap_clickable(node)
			if node.checks['num_full_overlap'] > 0:
				self.overall_checks['num_full_overlapping'] += 1

		### Editable TextView check
		node.checks['cont_desc_editable_textview'] = self.cont_desc_editable_textview(node)
		if node.checks['cont_desc_editable_textview']:
			self.overall_checks['num_cont_desc_editable_textview'] += 1

		### Duplicate Label
		self.duplicate_text_check()



	#####
	## Check content desc in TextView
	## editable image label
	#####

	# TODO, check if this is right class to check!
	# check if inherits from android.widget.EditText
	# should use get_role but don't know if just check class or inheritance
	def cont_desc_editable_textview(self, node):
		if self.is_editable_textview(node) and (talkbackAccessible.get_cont_desc(node)!= None):
			return True
		return False

	def is_editable_textview(self,node):
		ancestors = node.raw_properties['ancestors']
		if "android.widget.EditText" in ancestors:
			return True
		return False

	#####
	## Check identical speakable text
	## item descriptions
	# /** Accessitility-Test-framework-for-android DuplicateSpeakableTextViewHierarchyCheck
 	# If two Views in a hierarchy have the same speakable text, that could be confusing for users. Two
 	# Views with the same text, and at least one of them is clickable we warn in that situation. If we
 	# find two non-clickable Views with the same speakable text, we report that fact as info. If no
 	# Views in the hierarchy have any speakable text, we report that the test was not run.
	#####

	def duplicate_text_check(self):
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


	# return map from speakable text to all views/nodes of self with that speakable text
	#def get_speakable_text_to_node_map(self):


	#####
	### Check exact overlap
	### checks if two clickable nodes occupy the exact same place on the screen
	#####

	def full_overlap_clickable(self,node):
		num_full_overlap = 0
		for n in self.clickable_nodes:
			if n==node:
				continue
			else:
				if self.full_overlap_compare(node, n):
					num_full_overlap += 1
		return num_full_overlap

	# check if two elements n1 and n2 occupy the exact same space 
	def full_overlap_compare(self, node1,node2):
		b1 = node1.get_bounds()
		b2 = node2.get_bounds()
		if(b1['upper'] == b2['upper'] and b1['lower'] == b2['lower'] and \
			b1['left'] == b2['left'] and b1['right'] == b2['right']):
			return True
		return False

	#####
	### NOT IN USE
	### Check overlap
	### Not actually a check on Google Scanner
	#####
	def overlap_clickable(self, node):
		num_overlap = 0
		for n in self.clickable_nodes:
			if n == node:
				continue
			else:
				# only need to return 
				if self.overlap_clickable_compare(node, n):
					num_overlap += 1
		return num_overlap

	# check if two rectangular elements n1 and n2 overlap
	def overlap_clickable_compare(self, node1,node2):
		b1 = node1.get_bounds()
		b2 = node2.get_bounds()

		# if don't overlap one rect has to be above the other
		# or to the left of the other

		#above or below
		if (b1['lower'] < b2['upper'] or b2['lower'] < b1['upper']):
			return False
		# to the right or left
		if b1['left'] > b2['right'] or b2['left'] > b2['right']:
			return False
		return True

	#####
	### Check Label
	#####

	def has_label(self,node):
		return talkbackAccessible.get_speaking_text(node) != None

		# # if has own label, done
		# if talkbackAccessible.has_text(node):
		# 	return True
		# # if doesn't have own label, but is using children's label, ok
		# elif talkbackAccessible.has_non_actionable_speaking_children(node):
		# 	return True
		# else:
		# 	return False

	#####
	### Check Size
	#####
	def px_to_dp(self,px):
		# TODO: figure out dpi/phyical device of RICO
		# conversion of dp units to screen pixels is simple: px = dp * (dpi / 160).
		# https://developer.android.com/guide/practices/screens_support.html
		# calculated from what Google Scanner gave as DP of an element on 
		# the current version of app on Nexus 6P physical device and the 
		# pixel width based on that element's representation in RICO data
		# use dpi = 560
		dpi = 560
		return (px * 160)/dpi

	def wide_enough(self,node):
		k = node.raw_properties.keys()
		# bounds is 4 node array
		# 0 = left, 1 = top, 2 = right, 3 = bottom
		# google dev guidelines, needs to be 48 dp
		bounds = node.get_bounds()
		px_width = bounds['right'] - bounds['left']
		# must convert pixel to dp

		dp_width = self.px_to_dp(px_width)
		node.log['checks'].append("dp width: "+str(dp_width))
		dp_width_threshold = 48
		wide_enough = None
		if (dp_width < dp_width_threshold ):
			wide_enough = False
		else:
			wide_enough = True
		return wide_enough

	def tall_enough(self,node):
		k = node.raw_properties.keys()
		# bounds is 4 node array
		# 0 = left, 1 = top, 2 = right, 3 = bottom
		# google dev guidelines, needs to be 48 dp
		bounds = node.get_bounds()
		px_height = bounds['lower'] - bounds['upper']
		# must convert pixel to dp
		dp_height = self.px_to_dp(px_height)
		node.log['checks'].append("dp height: "+str(dp_height))
		dp_height_threshold = 48
		tall_enough = None
		if (dp_height < dp_height_threshold ):
			tall_enough = False
		else:
			tall_enough = True
		return tall_enough

	## TODO!!
	# INTEGRATE URL, perhaps look at text for common starters of links?
	def isValidURL(self, url):
	    URL_REGEX = re.compile(
	        u"^"
	        # protocol identifier
	        u"(?:(?:https?|ftp)://)"
	        # user:pass authentication
	        u"(?:\S+(?::\S*)?@)?"
	        u"(?:"
	        # IP address exclusion
	        # private & local networks
	        u"(?!(?:10|127)(?:\.\d{1,3}){3})"
	        u"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
	        u"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
	        # IP address dotted notation octets
	        # excludes loopback network 0.0.0.0
	        # excludes reserved space >= 224.0.0.0
	        # excludes network & broadcast addresses
	        # (first & last IP address of each class)
	        u"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
	        u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
	        u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
	        u"|"
	        # host name
	        u"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
	        # domain name
	        u"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
	        # TLD identifier
	        u"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
	        u")"
	        # port number
	        u"(?::\d{2,5})?"
	        # resource path
	        u"(?:/\S*)?"
	        u"$"
	        , re.UNICODE)
	    if URL_REGEX.match(url) == None:
	        return False
	    else:
	        return True
	#def has_label(node):
		# if it's not speakable, we're not interested in a label ?
		# TODO: check that this is right
	#	if(isSpeakable(node)):
	#		if node.characterisitcs['']
