import os # for parsing directories

from trace import Trace
from app_checker import App_Checker

class App:
	# defaults the ID of an app to the package name used as the directory name
	# info only for not constructing whole thing, mostly to quickly get missing info of app only
	def __init__(self, app_dir_arg, app_info_dict, app_id_arg=None, info_only=False):
		self.app_dir = app_dir_arg

		#ID should be package name since used as key to info dict
		self.id = app_id_arg

		# assume app directory is of form <.....>\<app_package>
		if (self.id == None):
			self.id = self.app_dir.split("\\")[-1]

		# dict contains: 'name': '<>',
		# 				 'date_updated': '<Month Day, Year>',
		# 				 'num_downloads': '<range>', 'category': '<>',
		#				 'num_ratings': #, 'rating':#
		self.info = {'date_updated':None,'name':None,'num_downloads':None,'category':None,'num_ratings':None,'rating':None}
		if self.id in app_info_dict.keys():
			self.info = app_info_dict[self.id]

		if not info_only:
			# map trace ID to Trace object
			self.traces = {}
			self.__parse_trace_dirs()

			self.num_views = None
			self.num_nodes = None
			self.num_type_nodes = {'TALKBACK':None, 'CLICKABLE':None, 'NON_CLICKABLE':None, 'EDITABLE_TEXTVIEW':None,
								   'ANDROID_DEFAULT': None, 'HAVE_CONT_DESC':None, 'WEBVIEW':None}

			self.checker = App_Checker(self)

	def __parse_trace_dirs(self):
		## assume directory struct of <....>\<app_package>\trace_<ID> 
		# so each item should just be trace_<ID>
		for item in os.listdir(self.app_dir):
			# check just in case something else is in the directory that is not
			# a trace directory
			item_info = item.split("_")
			if ((item_info[0]) == "trace"):
				#print ("Trace: "+item_info[1])
				trace_dir = self.app_dir + "\\"+item
				# should be <ID>
				#print("app: "+str(self.id))
				self.traces[item_info[1]] = Trace(trace_dir, self.id)

	## aggregators
	def __get_num_views(self):
		if self.num_views == None:
			self.num_views = 0
			for t in self.traces.values():
				self.num_views += len(t.views)
		return self.num_views

	def __get_num_nodes(self):
		if self.num_nodes == None:
			self.num_nodes = 0
			for t in self.traces.values():
				for v in t.views.values():
					self.num_nodes += len(v.nodes)
		return self.num_nodes

	def get_num_nodes_by_type(self,type):
		if self.num_type_nodes[type] == None:
			self.__set_type_nodes_count()
		return self.num_type_nodes[type]

	def __set_type_nodes_count(self):
		for type in self.num_type_nodes.keys():
			self.num_type_nodes[type] = 0
		for t in self.traces.values():
			for v in t.views.values():
				for type in self.num_type_nodes.keys():
					self.num_type_nodes[type] += v.get_num_type_nodes(type)

	# def get_num_talkback_nodes(self):
	# 	if self.num_talkback_nodes == None:
	# 		self.num_talkback_nodes = 0
	# 		for t in self.traces.values():
	# 			for v in t.views.values():
	# 				self.num_talkback_nodes += v.get_num_talkback_nodes()
	# 	return self.num_talkback_nodes
	#
	# def get_num_clickable_nodes(self):
	# 	if self.num_clickable_nodes == None:
	# 		self.num_clickable_nodes = 0
	# 		for t in self.traces.values():
	# 			for v in t.views.values():
	# 				self.num_clickable_nodes += v.get_num_nodes("CLICKABLE")
	# 	return self.num_clickable_nodes


	@staticmethod
	def print_header(fd, table_type):
		if table_type == "BY_APP":
			fd.write("app_id,app_name,date_updated,num_downloads,category,num_ratings,rating,num_traces,num_views,num_nodes,num_talkback_nodes,num_talkback_android_default,"
					 "num_clickable_nodes,num_non_clickable_nodes,num_editable_textview,")
		elif table_type == "APP_INFO_ONLY":
			fd.write("app_id,app_name,date_updated,num_downloads,category,num_ratings,rating,")
		elif table_type == "IMAGE_APP":
			fd.write("app_id,app_name,date_updated,num_downloads,category,num_ratings,rating,num_traces,num_views,num_nodes,num_talkback_nodes,num_talkback_android_default,"
					 "num_clickable_nodes,num_non_clickable_nodes,num_editable_textview,")
			#need to have num of eligible nodes per  test. FIX IN VIEW!!

	def print_table(self, table_type, fd, talkback_focus_only = True):
		if table_type == "BY_NODE" or table_type == "BY_TRACE" or table_type=="IMAGE_NODE":
			for t in self.traces.values():
				# table format
				# app_name, <node info>, <node checks>
				t.print_table(table_type, fd, talkback_focus_only)
		elif table_type == "BY_APP":
			fd.write(str(self.id)+","+\
				"\""+str(self.info['name'])+"\","+\
				"\""+str(self.info['date_updated'])+"\","+\
				"\""+str(self.info['num_downloads'])+"\","+\
				"\""+str(self.info['category'])+"\","+\
				str(self.info['num_ratings'])+","+str(self.info['rating'])+"," +\
				str(len(self.traces))+","+\
				str(self.__get_num_views())+"," +\
				str(self.__get_num_nodes())+"," +\
				str(self.get_num_nodes_by_type("TALKBACK"))+"," +\
				str(self.get_num_nodes_by_type("ANDROID_DEFAULT"))+ ","  +\
				str(self.get_num_nodes_by_type("CLICKABLE"))+"," +\
				str(self.get_num_nodes_by_type("NON_CLICKABLE"))+"," +\
				str(self.get_num_nodes_by_type("EDITABLE_TEXTVIEW"))+",")

			self.checker.print_table(table_type, fd)
			fd.write("\n")
		elif table_type == "APP_INFO_ONLY":
			fd.write(str(self.id)+","+\
				"\""+str(self.info['name'])+"\","+\
				"\""+str(self.info['date_updated'])+"\","+\
				"\""+str(self.info['num_downloads'])+"\","+\
				"\""+str(self.info['category'])+"\","+\
				str(self.info['num_ratings'])+","+str(self.info['rating'])+"," )
			fd.write("\n")


	def print_debug(self):
		print("App ID: "+self.id)
		for t in self.traces.values():
			t.print_debug()