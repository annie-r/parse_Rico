from checker_base import Checker_Base

node_aggregate_check_order = ["Num_Missing_Speakable_Test", "Num_Not_Wide_Enough", "Num_Not_Tall_Enough",\
   "Num_Editable_Textview_Cont_Desc"]

by_view_check_order = []
class View_Checker(Checker_Base):
    def __init__(self, view_arg):
        # the node this checker is checking
        self.view = view_arg
        Checker_Base.__init__(self)

        # in different dict since map to result, not a check object
        # feels overkill to make object for the aggregator checks
        self.node_aggregate_checks = {}

        self.__initialize_checks()


    ## SETUP
    ## MUST BE RUN IN INIT!!
    def __initialize_checks(self):
    	self.node_aggregate_checks["Num_Missing_Speakable_Test"] = self.num_missing_speakable_test()


    ### PRINTING

    def print_table(self, table_type):
    	if table_type == "BY_APP":
            for c in node_aggregate_check_order:
                print(str(node_aggregate_checks[c])+",",end="")
            for c in by_view_check_order:
                print(str(self.checks[c].result)+",",end="")


    def print_debug(self):
        print("ID: "+self.id)
        
  	## MUST BE IN SAME ORDER AS PUT IN __INITIALIZE_CHECKS
    # print aggregate checks first, then by app checks
    @staticmethod
    def print_header():
    	# first comes aggregates, order matters
        for c in node_aggregate_check_order:
            print (str(c)+",", end="")
        # then by app checks
        for c in by_view_check_order:
            print (str(c)+",", end="")

    ## Compile Node-Based Checks

    # counts number of nodes failing speakable text check
    def num_missing_speakable_test(self):
        result = 0
        for n in self.view.nodes:
            if not node.checker.get_result("Speakable_Text_Present"):  
                result +=1
