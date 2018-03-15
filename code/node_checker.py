from checker_base import Checker_Base
from speakable_text_present_check import Speakable_Text_Present_Check
from element_height_check import Element_Height_Check
from element_width_check import Element_Width_Check
from cont_desc_editable_textview_check import Cont_Desc_Editable_Textview_Check


class Node_Checker(Checker_Base):
    def __init__(self, node_arg):
        # the node this checker is checking
        self.node = node_arg
        Checker_Base.__init__(self)
        self.__initialize_checks()

    ## MUST BE RUN IN INIT!!
    def __initialize_checks(self):
        # some tests only to be performed on talkback accessible nodes
        if self.node.is_talkback_accessible():
            self.checks.append(Speakable_Text_Present_Check("Speakable_Text_Present",self.node))
            self.checks.append(Element_Width_Check("Element_Wide_Enough",self.node))
            self.checks.append(Element_Height_Check("Element_Tall_Enough",self.node))
            self.checks.append(Cont_Desc_Editable_Textview_Check("Editable_Textview_With_Cont_Desc",self.node))

    
    def print_views_table(self):
        # print order:
        # has_speakable_text_present,
        if self.node.is_talkback_accessible():
            for c in self.checks:
                print(str(c.result)+",",end="")

    ## MUST BE IN SAME ORDER AS PUT IN __INITIALIZE_CHECKS
    @staticmethod
    def print_header():
        print("Speakable_Text_Present,", end="")
        print("Element_Wide_Enough,",end="")
        print("Element_Tall_Enough,",end="")
        print("Editable_Textview_With_Cont_Desc",end="")
