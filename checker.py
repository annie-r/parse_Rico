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
		self.overall_checks['num_unlabeled']=0
		self.overall_checks['num_talkback_accessible']=0
		self.overall_checks['num_elements']=0
		self.overall_checks['num_not_wide_enough']=0
		self.overall_checks['num_not_tall_enough']=0
		self.overall_checks['num_not_wide_tall_enough']=0
		self.overall_checks['num_full_overlapping']=0

		#all nodes associated with TODO: screen? app? trace?
		self.nodes = []

	# TODO
	def print_overall_checks(self):
		print("OVERALL CHECKS")
		for k,v in self.overall_checks.items():
			print(str(k) + ": "+ str(v))


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
		# if has own label, done
		if talkbackAccessible.has_text(node):
			return True
		# if doesn't have own label, but is using children's label, ok
		elif talkbackAccessible.has_non_actionable_speaking_children(node):
			return True
		else:
			return False

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
