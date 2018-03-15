from checker_base import Checker_Base

class View_Checker(Checker_Base):
    def __init__(self, node_arg):
        # the node this checker is checking
        self.node = node_arg
        Checker_Base.__init__(self)
        self.__initialize_checks()

    ## MUST BE RUN IN INIT!!
    def __initialize_checks(self):
    	return 0

    def print_table(self, table_type):
    	print("todo")

  	## MUST BE IN SAME ORDER AS PUT IN __INITIALIZE_CHECKS
    @staticmethod
    def print_header():
    	print("todo")