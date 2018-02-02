''' Based on Android Talkback 1/30/2018
	
	runs test to emulate the checks of Android's talkback if it focuses and attempts to read
	an element 


'''

def has_text_or_cont_desc(node):
	pass_label = False
	k = node.properties.keys()
	# set to if the field exists
	has_text = 'text' in k
	has_content_desc = 'content-desc' in k
	# check if existing fields have content
	if has_content_desc:
		if(node.properties["content-desc"] == [None]):
			has_content_desc = False
		#print("content desc: ")
		#print(node["content-desc"])
	#if has_text:
		#print ("Text:" + str(node["text"]))
		# not checking if good, checking if has?
		#if node.properties["text"] == "" :
			#print("empty text")
		#	has_text = False
	#print("RESULT: ")
	# must have non-empty/null text or cont_desc to pass
	if not has_text and not has_content_desc:
		pass_label = False
		#print ("inaccessible")
	else:
		pass_label = True
		#print("accessible")
	# return if has label 
	return pass_label


# return if node is clickable or long-clickable
def is_clickable(node):
	k = node.properties.keys()
	has_clickable ='clickable' in k
	has_long_clickable = 'content-desc' in k

	# is clickable
	if('clickable' in k):
		if(node.properties["clickable"]):
			print("node is clickable")
			return True
	# long clickable
	if('long-clickable' in k):
		if(node.properties["long-clickable"]):
			print ("node is long clickable")
			return True
	return False

'''
	- Has non-actionable speaking children
		○ Ignore focusable children
		○ Ignore invisible childresn
		○ Recursively check children for isSpeakable
			If any child or grandchild is speakable, has nonactionablespeaking children
		○ TODO: Is top level scroll and is speaking

'''

def has_nonactionable_speaking_children(node):
	for child in node.children:
		# ignore focusable children
		if is_focusable(child):
			continue
		# ignore invisible children
		if not is_visible(child):
			continue
		# check if this is a speaking child
		if is_speakable(child):
			return True
		# recursively check
		if len(child.children) > 0:
			return has_nonactionable_speaking_children(child)
		# if leaf node and hasn't passed yet, false
		return False




'''
A node is speakable if:
	1. has text or content description
	2. is checkable (checkbox)
	3. has web content
	4. has non-actionable speaking children
'''

def is_speakable(node):
	if (has_text_or_cont_desc(node)):
		node.is_speakable = True
	if(is_clickable(node)):
		node.is_speakable = True
	#TODO web content
	if(has_nonactionable_speaking_children(node)):
		node.is_speakable = True
	return node.is_speakable


def is_focusable(node):
	return node.properties["focusable"]

# returns if a node is visible
def is_visible(node):
	k = node.properties.keys()
	print (k)

	if ('visibility' in k):
		# TODO: figure out all the meaning of the different
		# possible values of 'visibility' 
		if (node.properties['visibility'] == "visible"):
			return True
	# if the node doesn't have a visibility property
	# or if that property is not set to "visible"
	# it is not a visible node
	return False

''' returns if is accessed by Talkback based on Xiaoyi's list:
		An element can be accessed by Talkback only if:
		TODO: 1. It supports WebActions
		2. It is focusable(detected by Accessibility API) and has no visible children
		3. It is focusable and has something to speak
		4. It has text and no focusable ancestors (every getParent)
		
		An element cannot be accessed by Talkback if
		1. It is not visible
		TODO: 2. Its bounds are same as root window bounds
		3. It is focusable but has nothing to speak
		4. It doesn’t satisfy any of "should be focusable by Talkback” criteria.

	Based on read of Talkback Sourcecode
	Annie's inclusion :
		Focus "actionable" nodes:
		1. nodes that are clickable or long clickable
		2. if it's focusable
		3. is speakable

	Exclusion:
		1. never focus invisible
		2.


'''
def talkback_accessible(node, ancestor_focusable, children_visible):
	talkback_accessible = False
	k = node.properties.keys()


	if not is_visible(node):
		node.talkback_accessible = False
	elif is_clickable(node):
		node.talkback_accessible = True
	elif is_focusable(node):
		node.talkback_accessible = True
	elif is_speakable(node):
		node.talkback_accessible = True

	# inclusion criteria 2
	'''
	if is_focusable and not children_visible:
		print("focus and no vis children")
		talkback_accessible= True
	'''
	# # inclusion criteria 3
	# # exclusion criteria 3
	# if is_focusable and has_label(element):
	# 	print("focus and labeled")
	# 	talkback_accessible = True
	# else:
	# 	talkback_accessible = False 

	# inclusion criteria 4
	if has_text_or_cont_desc(node) and (not ancestor_focusable):
		print ("labeled with no focusable ancestor")
		talkback_accessible = True

	# exclusion criteria 1
	#print("visibility: "+str(element['visibility'])+ " "+ str(element['visibility'] == "visible"))
	if not 'visibility' in k or not (node.properties['visibility'] == "visible"):
		print("not visible")
		talkback_accessible = False

	print ("tb_access: "+str(talkback_accessible))
	return talkback_accessible
