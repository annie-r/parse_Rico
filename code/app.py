import os # for parsing directories

from trace import Trace

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
				self.traces[item_info[1]] = Trace(trace_dir, self.id)

	def print_views_table(self):
		for t in self.traces.values():
			# table format
			# app_name, <node info>, <node checks>
			t.print_views_table()
	def print_check(self):
		print("App ID: "+self.id)
		for t in self.traces.values():
			t.print_check()