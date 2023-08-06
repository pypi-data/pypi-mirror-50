import nanome
from nanome.util import Logs

import os

class RMSDMenu():
    def __init__(self, rmsd_plugin):
        self._menu = rmsd_plugin.menu
        self._plugin = rmsd_plugin
        self._selected_mobile = [] # button
        self._selected_target = None # button
        self._run_button = None
        self._current_tab = "receptor" #receptor = 0, target = 1
        self._drop_down_dict={"rotation":["None", "Kabsch","Quaternion"],"reorder_method":["None","Hungarian","Brute", "Distance"],\
        "select":["None","Global"]} # select["Local"] in the future
        self._current_reorder = "None"
        self._current_rotation = "None"
        self._current_select = "None"

    def _request_refresh(self):
        self._plugin.request_refresh()

    # run the rmsd algorithm
    def _run_rmsd(self):
        if self.check_resolve_error():
            self._plugin.run_rmsd([a.complex for a in self._selected_mobile], self._selected_target.complex)
        else:
            self.make_plugin_usable()

    # check the "unselect" and "select_same" error and call change_error
    def check_resolve_error(self,clear_only=False):
        if(not clear_only):
            if self._selected_mobile == None or self._selected_target == None:
                self.change_error("unselected")
                return False
            #elif self._selected_mobile.complex.index == self._selected_target.complex.index:
            elif self._selected_target.complex.index in list(map(lambda a:a.complex.index,self._selected_mobile)):
                self.change_error("select_same")
                return False
            else:
                self.change_error("clear")
                return True
        else:
            self.change_error("clear")
            return True

    # show the error message texts, fromRun means if the it is called after Run is pressed
    def change_error(self,error_type):
        if(error_type == "unselected"):
            self.error_message.text_auto_size=False
            self.error_message.text_size = 0.198
            self.error_message.text_value = "Error: Select both target and receptor"
            self.update_score(None)
            self._plugin.update_content(self.error_message)
            return True
        if(error_type == "select_same"):
            self.error_message.text_auto_size=False
            self.error_message.text_size = 0.22
            self.error_message.text_value = "Error: Select different complexes"
            self.update_score()
            self._plugin.update_content(self.error_message)
            return True
        if(error_type == "different_size"):
            self.error_message.text_auto_size=False
            self.error_message.text_size = 0.159
            self.error_message.text_value = "Error: Receptor and target have different sizes"
            self.update_score()
            self._plugin.update_content(self.error_message)
            return True
        if(error_type == "different_order"):
            self.error_message.text_auto_size=False
            self.error_message.text_size = 0.159
            self.error_message.text_value = "Error: Receptor and target have different order"
            self.update_score()
            self._plugin.update_content(self.error_message)
            return True
        if(error_type == "zero_size"):
            self.error_message.text_auto_size=False
            self.error_message.text_size = 0.15
            self.error_message.text_value = "Error: At least one complex has no atom selected"
            self.update_score()
            self._plugin.update_content(self.error_message)
            return True
        if(error_type == "selected_changed"):
            self.error_message.text_auto_size=False
            self.error_message.text_size = 0.176
            self.error_message.text_value = "Selected complexes have changed"
            self.update_score()
            self._plugin.update_content(self.error_message)
            return True
        if(error_type == "loading"):
            self.error_message.text_auto_size=False
            self.error_message.text_size = 0.2
            self.error_message.text_value = "Loading..."
            self.update_score()
            self._plugin.update_content(self.error_message)
            return True
        if(error_type == "clear"):
            self.error_message.text_value = ""
            self.error_message.text_auto_size = True
            self._plugin.update_content(self.error_message)



    # change the args in the plugin
    def update_args(self,arg,option):
        self._plugin.update_args(arg,option)

    def update_score(self,value=None):
        Logs.debug("update score called: ",value)
        if value == None:
            self.rmsd_score_label.text_value = "--"
        else:
            self.rmsd_score_label.text_value = str("%.3g"%value)
        self._plugin.update_content(self.rmsd_score_label)

    def make_plugin_usable(self, state = True):
        self._run_button.unusable = not state
        self._plugin.update_button(self._run_button)

    # change the complex list
    def change_complex_list(self, complex_list):
        
        # a button in the receptor list is pressed
        def mobile_pressed(button):

            # selecting button
            if button.complex.index not in [ a.complex.index for a in self._selected_mobile]:
                button.selected = True
                self._selected_mobile.append(button)
                if len(self._selected_mobile) == 1:
                    self.receptor_text.text_value = "Receptor: "+button.complex.name
                else:
                    self.receptor_text.text_value = "Receptor: multiple receptors"
            # deselecting button
            else:
                button.selected = False
                # self._selected_mobile = [i for i in self._selected_mobile if i.copmplex.index != button.complex.index]
                for x in self._selected_mobile:
                    if x.complex.index == button.complex.index:
                        self._selected_mobile.remove(x)
                if len(self._selected_mobile) == 1:
                    self.receptor_text.text_value = "Receptor: "+self._selected_mobile[0].complex.name
                elif len(self._selected_mobile) == 0:
                    self.receptor_text.text_value = "Receptor: Unselected"
                else:
                    self.receptor_text.text_value = "Receptor: multiple receptors"
                

            self.select_button.selected = False
            self.select_button.set_all_text("Select")            
            # tell the plugin and update the menu
            self._current_select = "None"
            self.update_args("select", "None")
            self._plugin.update_content(self._show_list)
            self._plugin.update_content(self.receptor_text)
            self._plugin.update_content(self.target_text)
            self._plugin.update_content(self.select_button)

        # a button in the target list is pressed
        def target_pressed(button):
            if self._selected_target != None:
                self._selected_target.selected = False 
                if self._selected_target.complex != button.complex: 
                    button.selected = True
                    self._selected_target = button
                    self.target_text.text_value ="Target: "+ button.complex.name
                else: 
                    self._selected_target = None
                    self.target_text.text_value = "Target: Unselected"
            else: 
                button.selected = True
                self._selected_target = button
                self.target_text.text_value ="Target: "+ button.complex.name
            self.check_resolve_error(clear_only=True)
            self.select_button.selected = False
            self.select_button.set_all_text("Select")
            # tell the plugin and update the menu
            self._current_select = "None"
            self.update_args("select", "None")
            self._plugin.update_content(self._show_list)
            self._plugin.update_content(self.receptor_text)
            self._plugin.update_content(self.target_text)
            self._plugin.update_content(self.select_button)

        self._mobile_list = []
        self._target_list = []

        if self._selected_mobile == None:
            self._selected_mobile = []

        if len(self._selected_mobile) != 0:
            for x in self._selected_mobile:
                if x.complex.index not in [i.index for i in complex_list]:
                    self._selected_mobile.remove()
            self._selected_mobile =None
        if self._selected_target != None and \
           self._selected_target.complex.index not in [i.index for i in complex_list]:
            self._selected_target = None
        
        for complex in complex_list:
            clone = self._complex_item_prefab.clone()
            ln_btn = clone.get_children()[0]
            btn = ln_btn.get_content()
            btn.set_all_text(complex.name)
            btn.complex = complex
            btn.register_pressed_callback(mobile_pressed)
            self._mobile_list.append(clone)
            if self._selected_mobile != None and btn.complex.index in [a.complex.index for a in self._selected_mobile]:
                btn.selected = True

            #clone1 = clone.clone()
            clone1 = self._complex_item_prefab.clone()
            ln_btn = clone1.get_children()[0]
            btn = ln_btn.get_content()
            btn.set_all_text(complex.name)
            btn.complex = complex
            btn.register_pressed_callback(target_pressed)
            self._target_list.append(clone1)
            if self._selected_target != None and btn.complex.index == self._selected_target.complex.index:
                btn.selected = True

        if len(self._selected_mobile) == 0:
            self.receptor_text.text_value ="Receptor: Unselected"
        if self._selected_target == None:
            self.target_text.text_value ="Target: Unselected "
        if self._current_tab == "receptor":
            self._show_list.items=self._mobile_list
        else:
            self._show_list.items=self._target_list
            
        self._plugin.update_menu(self._menu)

    # build the menu
    def build_menu(self):
        # refresh the lists
        def refresh_button_pressed_callback(button):
            self._request_refresh()
            

        # press the run button and run the algorithm
        def run_button_pressed_callback(button):
            self.make_plugin_usable(False)
            self._run_rmsd()


        # show the target list when the receptor tab is pressed
        def receptor_tab_pressed_callback(button):
            self._current_tab="receptor"
            receptor_tab.selected = True
            target_tab.selected = False
            self._show_list.items = self._mobile_list
            self._plugin.update_content(receptor_tab)
            self._plugin.update_content(target_tab)
            self._plugin.update_content(self._show_list)

        # show the target list when the target tab is pressed
        def target_tab_pressed_callback(button):
            self._current_tab="target"
            target_tab.selected = True
            receptor_tab.selected = False
            self._show_list.items = self._target_list
            self._plugin.update_content(receptor_tab)
            self._plugin.update_content(target_tab)
            self._plugin.update_content(self._show_list)
        
        # no hydrogen = ! no hydrogen
        def no_hydrogen_button_pressed_callback(button):
            no_hydrogen_button.selected = not no_hydrogen_button.selected
            self.update_args("no_hydrogen", no_hydrogen_button.selected)
            self._plugin.update_content(no_hydrogen_button)

        # backbone only = ! backbone only
        def backbone_only_button_pressed_callback(button):
            backbone_only_button.selected = not backbone_only_button.selected
            self.update_args("backbone_only", backbone_only_button.selected)
            self._plugin.update_content(backbone_only_button)
        
        # selected only = ! selected only
        def selected_only_button_pressed_callback(button):
            selected_only_button.selected = not selected_only_button.selected            
            self.update_args("selected_only", selected_only_button.selected)
            self._plugin.update_content(selected_only_button)

        # change Reorder to the next option
        def reorder_button_pressed_callback(button):
            drop_down  = self._drop_down_dict["reorder_method"]
            temp_length=len(drop_down)
            
            pre_index = drop_down.index(self._current_reorder)
            post_index = (pre_index + 1) % temp_length

            post_option = drop_down[post_index]

            reorder_button.selected = post_option != "None"
            reorder_button.set_all_text(post_option)
            
            # tell the plugin and update the menu
            self._current_reorder = post_option
            self.update_args("reorder_method", post_option)
            self.update_args("reorder", post_option != "None")
            self._plugin.update_content(reorder_button)

        # change Rotation to the next option
        def rotation_button_pressed_callback(button):
            drop_down  = self._drop_down_dict["rotation"]
            temp_length=len(drop_down)
            
            pre_index = drop_down.index(self._current_rotation)
            post_index = (pre_index + 1) % temp_length

            post_option = drop_down[post_index]

            rotation_button.selected = post_option != "None"
            rotation_button.set_all_text(post_option)
            
            # tell the plugin and update the menu
            self._current_rotation = post_option
            self.update_args("rotation_method", post_option)
            self._plugin.update_content(rotation_button)

        def select_button_pressed_callback(button): 
            if self._selected_mobile != None and self._selected_target != None:
                
                self._plugin.select([x.complex for x in self._selected_mobile],self._selected_target.complex)
                drop_down  = self._drop_down_dict["select"]
                temp_length=len(drop_down)
                
                pre_index = drop_down.index(self._current_select)
                post_index = (pre_index + 1) % temp_length
                
                post_option = drop_down[post_index]
                self.select_button.selected = post_option != "None"
                
                if post_option == "None":
                    self.select_button.set_all_text("Select")
                else:
                    self.select_button.set_all_text(post_option)
                
                # tell the plugin and update the menu
                self._current_select = post_option
                self.update_args("select", post_option)
            else:
                self.check_resolve_error()
            self._plugin.update_content(self.select_button)

        # Create a prefab that will be used to populate the lists
        self._complex_item_prefab = nanome.ui.LayoutNode()
        self._complex_item_prefab.layout_orientation = nanome.ui.LayoutNode.LayoutTypes.horizontal
        child = self._complex_item_prefab.create_child_node()
        child.name = "complex_button"
        prefabButton = child.add_new_button()
        prefabButton.text.active = True

        # import the json file of the new UI
        menu = nanome.ui.Menu.io.from_json(os.path.join(os.path.dirname(__file__), 'rmsd_pluginator.json'))
        self._plugin.menu = menu

        # add the refresh icon
        refresh_img = menu.root.find_node("Refresh Image", True)
        refresh_img.add_new_image(file_path = "./nanome_rmsd/Refresh.png")

        # create the Run button
        self._run_button = menu.root.find_node("Run", True).get_content()
        self._run_button.register_pressed_callback(run_button_pressed_callback)

        # create the Refresh button
        refresh_button = menu.root.find_node("Refresh Button", True).get_content()
        refresh_button.register_pressed_callback(refresh_button_pressed_callback)

        # create the List 
        self._show_list = menu.root.find_node("List", True).get_content()
        self._mobile_list = []
        self._target_list = []

        # create the Receptor tab
        receptor_tab = menu.root.find_node("Receptor_tab",True).get_content()
        receptor_tab.register_pressed_callback(receptor_tab_pressed_callback)

        # create the Target tab
        target_tab = menu.root.find_node("Target_tab",True).get_content()
        target_tab.register_pressed_callback(target_tab_pressed_callback)

        # create the no hydrogen button
        no_hydrogen_button = menu.root.find_node("No Hydrogen btn",True).get_content()
        no_hydrogen_button.register_pressed_callback(no_hydrogen_button_pressed_callback)

        # create the use reflection button
        # use_reflections_button = menu.root.find_node("Use Reflection btn",True).get_content()
        # use_reflections_button.register_pressed_callback(use_reflections_button_pressed_callback)

        # create the backbone only button
        backbone_only_button = menu.root.find_node("Backbone only btn",True).get_content()
        backbone_only_button.register_pressed_callback(backbone_only_button_pressed_callback)

        # create the selected only button
        selected_only_button =  menu.root.find_node("Selected Only btn",True).get_content()
        selected_only_button.register_pressed_callback(selected_only_button_pressed_callback)

        # create the reorder button
        reorder_button = menu.root.find_node("Reorder menu",True).get_content()
        reorder_button.register_pressed_callback(reorder_button_pressed_callback)

        # create the roation "drop down"
        rotation_button = menu.root.find_node("Rotation menu",True).get_content()
        rotation_button.register_pressed_callback(rotation_button_pressed_callback)

        # create the select cycle button
        self.select_button = menu.root.find_node("Auto Select",True).get_content()
        self.select_button.register_pressed_callback(select_button_pressed_callback)

        # create the rmsd score
        self.rmsd_score_label = menu.root.find_node("RMSD number",True).get_content()

        # create the receptor text
        self.receptor_text = menu.root.find_node("Receptor").get_content()
        
        # create the target text
        self.target_text = menu.root.find_node("Target").get_content()
        
        # create the error message text
        error_node = menu.root.find_node("Error Message")
        self.error_message = error_node.get_content()

        self._menu = menu
        

        # self._request_refresh()