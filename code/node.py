
from talkback_accessible import talkback_focus
from node_checker import Node_Checker
class Node:
	# raw_properties are the dictionary of properties associated with the node 9(e.g. "focusable" "cont_desc")
	# characteristics are determined with heuristic tests (e.g. "is speakble" "is visible")
	# parent, pointer to parent node
	# children, empty list of children
	#test
	def __init__(self, properties, parent, level_arg):
		self.raw_properties = properties
		# depth from root
		self.level = level_arg
		self.characteristics = {}
		self.parent = parent
		self.children = []

		# log to track decisions about talkback accessibility and checks
		self.log = {'talkback_accessible':[], 'checks':[]}
		# logged by step
		#self.log = {'talkback_accessible':[], 'checks':[]}

		# collects results of check results for individual nodes
		self.checker = Node_Checker(self)

	# checks if coords are within this node's boundries
	def contains_coords(self,coords):
		bounds = self.get_bounds()
		if coords['x'] >= bounds['left'] and coords['x'] <= bounds['right'] and \
						coords['y'] >= bounds['top'] and coords['y'] <= bounds['bottom']:
			return True
		else:
			return False

	def print_table(self,table_type):
		if table_type == "BY_NODE":
			k = self.raw_properties.keys()
			#ID column
			if 'resource-id' in k:
				print(str(self.raw_properties['resource-id']),end="")
			else:
				print("None",end="")
			#,class_name,android_widget?,ad_widget?,checks
			print(","+str(self.raw_properties['class'])+"," + str(self.is_android_default_widget())+","+str(self.is_ads_widget())+",",end="")
			self.checker.print_table(table_type)

	def print(self):
		k = self.raw_properties.keys()
		self.__print_level()
		print("##########")
		# resource id
		self.__print_level()
		if 'resource-id' in k:
			print("id: " + str(self.raw_properties['resource-id']))
		else:
			print("no resource id")
		# class
		self.__print_level()
		if 'class' in k:
			print("class: "+str(self.raw_properties['class']))
		else:
			print('no class')
		self.__print_level()
		print("ad: "+str(self.is_ads_widget()))
		self.__print_level()
		print("widget: "+str(self.is_android_default_widget()))

		# bounds
		self.__print_level()
		print("bounds: "+str(self.get_bounds()))
		# text, if applicable, to help identify

		if 'text' in self.raw_properties.keys():
			self.__print_level()
			try:
				print("text: " + str(self.raw_properties['text']))
			except UnicodeEncodeError:
				print("text: undefined unicode")

		self.__print_level()
		try:
			print("label: " + str(self.get_speakable_text()))
		except UnicodeEncodeError:
			print("label: undefined unicode")


		# talkback accessible criteria
		self.__print_level()
		print("talkback_accessible: " + str(self.is_talkback_accessible()))

		# print talkback accessible log
		for entry in set(self.log['talkback_accessible']):
			self.__print_level()
			try:
				print("- "+str(entry))
			except UnicodeEncodeError:
				print("-: undefined unicode")

		# print results of checks
		# self.__print_level()
		# print("checks results")
		# for check, result in self.checks.items():
		# 	self.__print_level()
		# 	print(check + ": "+str(result))

		# print checks log
		for entry in set(self.log['checks']):
			self.__print_level()
			print("- "+str(entry))

		#self.__print_level()
		self.checker.print_table("BY_NODE")

		#self.__print_children()

		print ('\n')

	def __print_children(self):
		for c in self.children:
			if len(c.children) > 0:
				c.__print_children()
			self.__print_level()
			try:
				print("- child: "+str(c.get_resource_id()) +" "+str(c.get_speakable_text()))
			except UnicodeEncodeError:
				print("- child: "+str(c.get_resource_id()) + " undefined unicode")


	def __print_level(self):
		for i in range(0,self.level):
			print("\t ",end="")
		print("++ ",end="")


	##############
	#### Getters and Setters
	##############
	def get_resource_id(self):
		k=self.raw_properties.keys()
		if 'resource-id' in k:
			return self.raw_properties['resource-id']
		else:
			return None

	def set_characteristics(self):
		# will it be focused and attempted read by Talkback
		#self.characteristics['talkback_accessible'] = talkback_focus(self)
		return 0

	def add_child(self,child):
		self.children.append(child)

	# so don't have to remember what order they are in in the json
	def get_bounds(self):
		bounds = self.raw_properties['bounds']
		# the coordinates start in upper left of screen so 0,0 is left, upper-most point
		return {"left":bounds[0], "top":bounds[1], "right":bounds[2], "bottom":bounds[3]}

	def is_talkback_accessible(self):
		if not 'talkback_accessible' in self.characteristics.keys():
			self.characteristics['talkback_accessible'] = talkback_focus(self)
		return self.characteristics['talkback_accessible']

	def is_android_default_widget(self):
		if not 'android_default_widget' in self.characteristics.keys():
			self.characteristics['android_default_widget'] = self.__is_android_default_widget()
		return self.characteristics['android_default_widget']

	# defined as having a class from the "android.widget" library
	def __is_android_default_widget(self):
		node_class = self.raw_properties['class']
		# classes appear to be android.widget.<widget>.<name>....
		class_name_list = node_class.split(".")
		if (class_name_list[0] == "android" and class_name_list[1]=="widget"):
			return True
		return False


	def is_ads_widget(self):
		if not 'ads_widget' in self.characteristics.keys():
			self.characteristics['ads_widget'] = self.__is_ads_widget()
		return self.characteristics['ads_widget']

	def __is_ads_widget(self):
		# appears the ads interface comes from library com.google.android.gms.ads
		ads_library = "com.google.android.gms.ads"
		node_class = self.raw_properties['class']
		# multiple types of views/widgets for ads? so just check for library at beginning
		# e.g. a class of com.google.android.gms.com.AdView should return true
		if node_class[:len(ads_library)] == ads_library:
			return True
		return False


	#################
	##### TODO
	###############
	#TODO
	def has_webAction(self):
		return False

	#TODO
	# don't know what fields to look for
	def is_checkable(self):
		return False




	###############
	##### CHARACTERISTICS
	###############

	def is_clickable(self):
		#print("is clickable test")
		k = self.raw_properties.keys()
		has_clickable ='clickable' in k
		has_long_clickable = 'content-desc' in k
		# is clickable
		if('clickable' in k):
			if(self.raw_properties["clickable"]):
				self.log['talkback_accessible'].append("node is clickable")
				return True
		# long clickable
		if('long-clickable' in k):
			if(self.raw_properties["long-clickable"]):
				self.log['talkback_accessible'].append("node is long clickable")
				return True
		return False

	# return if node is visible
	# currently defined as the "visibile to user" property is "True"
	def is_visible(self):
		#print("is visible test")
		k = self.raw_properties.keys()
		if ('visible-to-user' in k):
			# TODO: figure out all the meaning of the different
			# possible values of 'visibility'
			self.log['talkback_accessible'].append('visible-to-user: ' + str(self.raw_properties['visible-to-user']))
			if (self.raw_properties['visible-to-user']):
				return True
		# if the node doesn't have a visibility property
		# or if that property is not set to "visible"
		# it is not a visible node
		else:
			self.log['talkback_accessible'].append('no visible-to-user tag')
		return False

	def has_non_zero_dimensions(self):
		bounds = self.get_bounds()
		# not sure of case where it's only zero in one dimension
		if bounds['left'] == bounds['right'] and bounds['top'] == bounds['bottom']:
			self.log['talkback_accessible'].append("zero dimensions")
			return False
		return True

	def is_actionable(self):
		#print("is actionable test")
		if self.is_clickable():
			self.log['talkback_accessible'].append("is clickable")
			return True
		elif self.is_focusable():
			self.log['talkback_accessible'].append("is focusable")
			return True
		# TODO
		# elif web thing
		self.log['talkback_accessible'].append("not actionable")
		return False

	def is_focusable(self):
		#print("is focusable test")
		result = self.raw_properties["focusable"]
		if result:
			self.log['talkback_accessible'].append("focusable")
		else:
			self.log['talkback_accessible'].append("not focusable")
		return result

	def is_top_level_scrollable(self):
		if self == None:
			return False

		if self.parent == None:
			# not a child of anything
			return False

		if self.is_scrollable():
			return True

		# top-level items in a scrolling pager are actually two levels down since the first
		# level items in pagers are the pages themselves
		grandparent = self.parent.parent
		if (grandparent != None):
			if grandparent.get_role() == "ROLE_PAGER":
				return True

		parent_role = self.parent.get_role()
		# Note that ROLE_DROP_DOWN_LIST(Spinner) is not accepted.
		# TODO: haven't RecyclerView is classified as a list or grid based on its CollectionInfo.
		result = (parent_role == "ROLE_LIST" or parent_role == "ROLE_GRID" or parent_role =="ROLE_SCROLL_VIEW" \
				  or parent_role == "ROLE_HORIZONTAL_SCROLL_VIEW")
		self.log['talkback_accessible'].append("role: "+str(parent_role))
		return result

	# don't know if right definition since in talkback specifies as "scroll forward" and "scroll backward"
	# but in data only have "horizontal" and "vertical" scroll
	def is_scrollable(self):
		k = self.raw_properties.keys()
		if "scrollable-vertical" in k:
			if self.raw_properties["scrollable-vertical"]:
				self.log['talkback_accessible'].append("scrollable-vertical")
				return True

		if "scrollable-horizontal" in k:
			if self.raw_properties["scrollable-horizontal"]:
				self.log['talkback_accessible'].append("scrollable-horizontal")
				return True
		return False

	#
	def has_visible_children(self):
		#print("has visible children test")
		for child in self.children:
			if child.is_visible():
				return True
		return False

	# returns if the node is talkback speaking
	# based on if it's speakable text is null
	# this includes speakable text from children

	def is_speaking(self):
		return (not self.get_speakable_text() == None)

	def has_focusable_ancestors(self):
		#print("has focusable ancestor test")
		ancestor = self.parent
		while ancestor:
			if talkback_focus(ancestor, check_children=False):
				return True
			ancestor = ancestor.parent
		return False

	###########
	## Getters
	##########
	'''
	A node is speakable if:
		1. has text or content description
		2. is checkable (checkbox)
		3. has web content
		4. has non-actionable speaking children

		# will return text either from self or children, or None if no text
		# was is _speaking
	'''
	def get_speakable_text(self):
		#print("getting speakable")
		#print("is speaking test")
		text = self.get_self_text()
		# try:
		#     print("text: " + str(text))
		# except UnicodeEncodeError:
		#     print("text: undefined unicode")
		if text != None:
			#print("self text")
			return text
		#TODO
		#elif is_checkable(node):
		#	return True
		# TODO
		# if web thing
		text = self.get_non_actionable_speaking_children_text()
		# if text != None:
		# 	return text
		#print(" text: "+str(text))
		return text

	# defined as having none Null or zero length Text or Content Description
	# TODO:
	#      * For the purposes of this check, any node with a CollectionInfo is considered to not have
	#     * text since its text and content description are used only for collection transitions.
	# returns a node's text, or cont-descr, if available, else, returns None
	def get_self_text(self):
		#print ("hast text")
		#pass_label = False
		text = None
		text = self.__get_textfield()
		if text == None:
			text = self.get_cont_desc()
		self.log['talkback_accessible'].append("has own label: "+str(not text == None))
		return text

	# need for other check so make public
	def get_cont_desc(self):
		cont_desc = None
		k = self.raw_properties.keys()
		has_content_desc = 'content-desc' in k
		if has_content_desc:
			self.log['talkback_accessible'].append("has cont desc: "+str(self.raw_properties['content-desc'][0]))
			has_content_desc = not self.__is_empty(self.raw_properties["content-desc"][0])
			if has_content_desc:
				cont_desc = self.raw_properties["content-desc"][0]
		return cont_desc

	def get_non_actionable_speaking_children_text(self):
		#print ("num children: "+str(len(self.children)))
		#print("non actionable children test")
		for child in self.children:
			#print("child id: "+str(child.get_resource_id()))
			# ignore focusable children
			if child.is_focusable():
				#print ("child: "+child.get_resource_id()+" focusable")
				continue
			# ignore invisible children
			if not child.is_visible():
				#print("visible child")
				continue
			# check if this is a speaking child
			child_text = child.get_speakable_text()
			#print ("child: "+str(child.get_resource_id()) + " "+str(child_text))
			if child_text != None:
				self.log['talkback_accessible'].append("has nonactionable speaking children")
				#node.characteristics['has_non_actionable_speaking_children'] = True
				return child_text
			# recursively check children
			#if len(child.children) > 0:
			# child.get_speakable_text()
			# if leaf node and hasn't passed yet, false
		#print("ran out of children")
		return None



	#Role.java l213 2.14.2018 Talkback
	## SHOULD BE LOOKING AT JUST CLASS OR INHERITANCE!?
	def get_role(self):
		#print ("Getting role")

		if self == None:
			return "ROLE_NONE"
		k = self.raw_properties.keys()
		if not "class" in k:
			return "ROLE_NONE"

		node_class = self.raw_properties['class']
		#node_classes = node.raw_properties['ancestors']

		# When comparing node.getClassName() to class name of standard widgets, we should take care of
		# the order of the "if" statements: check subclasses before checking superclasses.
		# e.g. RadioButton is a subclass of Button, we should check Role RadioButton first and fall
		# down to check Role Button.

		# Inheritance: View->ImageView
		if (node_class == "android.widget.ImageView"):
			if (self.is_clickable()):
				return "ROLE_IMAGE_BUTTON"
			else:
				return "ROLE_IMAGE"

		##############################
		## Subclasses of TextView.

		## Inheritance: View->TextView->Button->CompoundButton->Switch
		if node_class == "android.widget.Switch":
			return "ROLE_SWITCH"

		if node_class == "android.widget.ToggleButton":
			return "ROLE_TOGGLE_BUTTON"

		if node_class == "android.widget.RadioButton":
			return "ROLE_RADIO_BUTTON"

		if node_class == "android.widget.CompoundButton":
			return "ROLE_CHECKBOX"

		if node_class == "android.widget.Button":
			return "ROLE_BUTTON"

		if node_class == "android.widget.CheckedTextView":
			return "ROLE_CHECKED_TEXT_VIEW"

		if node_class == "android.widget.EditText":
			return "ROLE_EDIT_TEXT"

		##################################
		## Subclasses of Progressbar

		if node_class == "android.widget.SeekBar":
			return "ROLE_SEEK_CONTROL"
		if node_class == "android.widget.ProgressBar":
			return "ROLE_PROGRESS_BAR"
		if node_class == "android.inputmethodservice.Keyboard.Key":
			return "ROLE_KEYBOARD_KEY"

		##############################
		## Subclasses of ViewGroup

		if node_class == "android.webkit.WebView":
			return "ROLE_WEB_VIEW"
		if node_class == "android.widget.TabWidget":
			return "ROLE_TAB_BAR"

		if node_class == "android.widget.HorizontalScrollView":
			return "ROLE_HORIZONTAL_SCROLL_VIEW"

		if node_class == "android.widget.ScrollView":
			return "ROLE_SCROLL_VIEW"
		# Inheritance: View->ViewGroup->ViewPager
		if node_class == "android.support.v4.view.ViewPager":
			return "ROLE_PAGER"

		if node_class == "android.widget.Spinner":
			return "ROLE_DROP_DOWN_LIST"
		if node_class == "android.widget.GridView":
			return "ROLE_GRID"
		if node_class == "android.widget.AbsListView":
			return "ROLE_LIST"

		# TODO!!! ln 339
		# CollectionInfoCompat collection = node.getCollectionInfo();
		# if (collection != null) {
		# # RecyclerView will be classified as a list or grid.
		# 	if (collection.getRowCount() > 1 && collection.getColumnCount() > 1) {
		# 		return ROLE_GRID;
		# 	} else {
		# 		return ROLE_LIST;
		# 	}
		# }

		if node_class == "android.view.ViewGroup":
			return "ROLE_VIEW_GROUP"

		return "ROLE_NONE"


	#### Private Getters
	def __get_textfield(self):
		text = None
		k = self.raw_properties.keys()
		# set to if the field exists
		has_text = 'text' in k
		if has_text:
			self.log['talkback_accessible'].append("has text: "+self.raw_properties['text'])
			has_text = not self.__is_empty(self.raw_properties['text'])
			if has_text:
				text = self.raw_properties['text']
		else:
			self.log['talkback_accessible'].append("no text")
		return text




	######################
	##### HELPER
	######################


	def __is_empty(self,str):
		if (str == None or len(str) == 0):
			return True
		else:
			return False



