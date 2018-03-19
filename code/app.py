import os # for parsing directories

from trace import Trace
from app_checker import App_Checker

class App:
	# defaults the ID of an app to the package name used as the directory name
	def __init__(self, app_dir_arg, app_id_arg=None):
		self.app_dir = app_dir_arg
		self.id = app_id_arg
		# assume app directory is of form <.....>\<app_package>
		if (self.id == None):
			self.id = self.app_dir.split("\\")[-1]
		#print("app id: "+str(self.id))
		# map trace ID to Trace object

		self.traces = {}
		self.__parse_trace_dirs()

		self.num_views = None
		self.num_nodes = None
		self.num_talkback_nodes = None

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

	def __get_num_talkback_nodes(self):
		if self.num_talkback_nodes == None:
			self.num_talkback_nodes = 0
			for t in self.traces.values():
				for v in t.views.values():
					self.num_talkback_nodes += v.get_num_talkback_nodes()
		return self.num_talkback_nodes


	@staticmethod
	def print_header():
		print("app_id,num_traces,num_views,num_nodes,num_talkback_nodes,",end="")

	def print_table(self, table_type, talkback_focus_only = True):
		if table_type == "BY_NODE":
			for t in self.traces.values():
				# table format
				# app_name, <node info>, <node checks>
				t.print_table(table_type, talkback_focus_only)
		if table_type == "BY_APP":
			print(str(self.id)+","+str(len(self.traces))+","+\
				str(self.__get_num_views())+"," +\
				str(self.__get_num_nodes())+"," +\
				str(self.__get_num_talkback_nodes())+",",end="")
			self.checker.print_table(table_type)
			print("")


	def print_debug(self):
		print("App ID: "+self.id)
		for t in self.traces.values():
			t.print_debug()