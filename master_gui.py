try:
    import os, sys
    import tkinter as tk
    from tkinter import ttk
    from tkinter.messagebox import askokcancel, showinfo
    from tkinter.filedialog import *
    import webbrowser
except:
    print("ERROR: Missing fundamental packages (required: os, sys, tkinter, webbrowser).")
try:
    sys.path.append(os.path.dirname(__file__) + "\\.site_packages\\riverpy\\")
    from cLogger import Logger
except:
    print("ERROR: Could not import Logger (riverpy).")
try:
    import GetStarted
except:
    print("ERROR: Could not import Welcome Screen (Get Started).")
try:
    import ProjectMaker
except:
    print("ERROR: Could not import ProjectMaker.")
try:
    import LifespanDesign
except:
    print("ERROR: Could not import LifespanDesign.")
try:
    import MaxLifespan
except:
    print("ERROR: Could not import MaxLifespan.")
try:
    import ModifyTerrain
except:
    print("ERROR: Could not import ModifyTerrain.")
try:
    import SHArC
except:
    print("ERROR: Could not import SHArC.")
try:
    import EcoMorphology
except:
    print("ERROR: Could not import EcoMorphology.")


class RaGui(tk.Frame):
    # master GUI for all RiverArchitect modules
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.logger = Logger("logfile")
        self.pack()

        self.master.title("River Architect")
        self.master.iconbitmap(os.path.dirname(os.path.abspath(__file__)) + "\\.site_packages\\templates\\code_icon.ico")

        self.tab_container = ttk.Notebook(master)

        self.tab_names = ['Get Started',
                          'Lifespan',
                          'Morphology',
                          'Ecohydraulics',
                          'Project Maker']

        self.sub_tab_parents = ['Lifespan',
                                'Morphology',
                                'Ecohydraulics']

        self.sub_tab_names = [['Lifespan Design', 'Max Lifespan'],
                              ['Terrain Creation', 'Volume Assessment'],
                              ['SHArC', 'Connectivity']]

        # working directory suffixes for each module
        self.tab_dir_names = ['\\GetStarted\\',
                              ['\\LifespanDesign\\', '\\MaxLifespan\\'],
                              ['\\ModifyTerrain\\', '\\ModifyTerrain\\'],
                              ['\\SHArC\\', '\\SHArC\\'],
                              '\\ProjectMaker\\']

        # Frames initialized by module, with parent being tab container
        self.tab_list = [GetStarted.welcome_gui.MainGui(self.tab_container),
                         ttk.Notebook(self.tab_container),
                         ttk.Notebook(self.tab_container),
                         ttk.Notebook(self.tab_container),
                         ProjectMaker.project_maker_gui.MainGui(self.tab_container)]

        self.tab_dirs = dict(zip(self.tab_names, self.tab_dir_names))
        self.tabs = dict(zip(self.tab_names, self.tab_list))

        # sub tabs initialized, with parents being associated top-level tabs
        self.sub_tab_list = [[LifespanDesign.lifespan_design_gui.FaGui(self.tabs['Lifespan']),
                              MaxLifespan.action_gui.ActionGui(self.tabs['Lifespan'])],
                             [ModifyTerrain.modify_terrain_gui.MainGui(self.tabs['Morphology']),
                              ModifyTerrain.modify_terrain_gui.MainGui(self.tabs['Morphology'])],
                             [SHArC.sharc_gui.MainGui(self.tabs['Ecohydraulics']),
                              SHArC.sharc_gui.MainGui(self.tabs['Ecohydraulics'])]]

        self.sub_tab_names = dict(zip(self.sub_tab_parents, self.sub_tab_names))
        self.sub_tabs = dict(zip(self.sub_tab_parents, self.sub_tab_list))

        for tab_name in self.tab_names:
            tab = self.tabs[tab_name]
            tab.bind('<Visibility>', self.tab_select)
            self.tab_container.add(tab, text=tab_name)
            self.tab_container.pack(expand=1, fill="both")
            # set sub-tabs
            if tab_name in self.sub_tab_parents:
                for i, sub_tab_name in enumerate(self.sub_tab_names[tab_name]):
                    sub_tab = self.sub_tabs[tab_name][i]
                    sub_tab.bind('<Visibility>', self.tab_select)
                    tab.add(sub_tab, text=sub_tab_name)

    def tab_select(self, event):
        selected_tab_name = self.tab_container.tab(self.tab_container.select(), 'text')
        if selected_tab_name in self.sub_tab_parents:
            parent = self.tabs[selected_tab_name]
            # names of sub-tabs for this parent
            sub_tab_names = self.sub_tab_names[selected_tab_name]
            # name of selected sub-tab
            selected_subtab_name = parent.tab(parent.select(), 'text')
            # index of sub-tab under parent tab
            i = sub_tab_names.index(selected_subtab_name)
            selected_tab = self.sub_tabs[selected_tab_name][i]
            os.chdir(os.path.dirname(os.path.abspath(__file__)) + self.tab_dirs[selected_tab_name][i])
        else:
            selected_tab = self.tabs[selected_tab_name]
            os.chdir(os.path.dirname(os.path.abspath(__file__)) + self.tab_dirs[selected_tab_name])
        selected_tab.set_geometry()
        selected_tab.make_menu()


if __name__ == '__main__':
    RaGui().mainloop()
