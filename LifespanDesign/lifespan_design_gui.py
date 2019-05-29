try:
    import os, sys
    import tkinter as tk
    from tkinter.messagebox import askokcancel, showinfo
    from tkinter.filedialog import *
    import webbrowser
    from functools import partial
except:
    print("ExceptionERROR: Missing fundamental packages (required: os, sys, tkinter, webbrowser).")

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\\.site_packages\\riverpy\\")
    import cDefinitions as cdef
    import fGlobal as fg
    import cReachManager as cmio
except:
    print("ExceptionERROR: Cannot find package files (RP/fGlobal.py, RP/cDefinitions.py, RP/cReachManager).")


class PopUpWindow(object):
    def __init__(self, master):
        self.dir2ra = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\\"
        top = self.top = tk.Toplevel(master)
        msg0 = "Manning\'s n is used in the calculation of grain mobility for shear velocity.\n"
        msg1 = "Please refer to the manual (Lifespan mapping section about angular boulders and grain mobility) for more details.\n"
        msg3 = "If you are using US costumary units, River Architect will use an internal conversion factor for the here entered metric value.\n"
        self.l_0 = tk.Label(top, text=msg0)
        self.l_0.pack(padx=5, pady=5)
        self.l_1 = tk.Label(top, text=msg1)
        self.l_1.pack(padx=5, pady=5)
        self.l_2 = tk.Label(top, text="Enter new SI-metric value for Manning\'s n in [s/m^(1/3)]:")
        self.l_2.pack(padx=5, pady=5)
        self.e = tk.Entry(top, width=10)
        self.e.pack(padx=5, pady=5)
        self.b = tk.Button(top, text='OK', command=self.cleanup)
        self.b.pack(padx=5, pady=5)
        self.l_3 = tk.Label(top, text=msg3)
        self.l_3.pack(padx=5, pady=5)
        self.top.iconbitmap(self.dir2ra + ".site_packages\\templates\\code_icon.ico")

    def cleanup(self):
        self.value = self.e.get()
        self.top.destroy()


class RunGui:
    def __init__(self, master):
        # Construct the Frame object
        self.dir2ra = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\\"
        self.master = tk.Toplevel(master)
        self.master.wm_title("CHECK CONSOLE MESSAGES")
        self.master.bell()
        self.msg = ""

        # ARRANGE GEOMETRY
        self.ww = 400
        self.wh = 100
        self.wx = (self.master.winfo_screenwidth() - self.ww) / 2
        self.wy = (self.master.winfo_screenheight() - self.wh) / 2
        self.master.geometry("%dx%d+%d+%d" % (self.ww, self.wh, self.wx, self.wy))

    def gui_raster_maker(self, condition, reach_ids_applied, feature_list, mapping, habitat, units, wild, n, ext_type):
        import feature_analysis as fa
        out_dir = fa.raster_maker(condition, reach_ids_applied, feature_list, mapping, habitat, units, wild, n, ext_type)
        self.master.iconbitmap(self.dir2ra + ".site_packages\\templates\\code_icon.ico")
        return out_dir

    def gui_map_maker(self, raster_directories, reach_ids_applied):
        import feature_analysis as fa
        self.master.iconbitmap(self.dir2ra + ".site_packages\\templates\\code_icon.ico")
        if not reach_ids_applied:
            return fa.map_maker(raster_directories)
        else:
            return fa.map_maker(raster_directories, reach_ids=reach_ids_applied)

    def gui_quit(self):
        self.master.destroy()

    def open_log_file(self):
        logfilenames = ["error.log", "rasterlogfile.log", "logfile.log", "map_logfile.log", "mxd_logfile.log"]
        for filename in logfilenames:
            _f = r'' + os.path.dirname(os.path.abspath(__file__)) + "\\" + filename
            if os.path.isfile(_f):
                try:
                    webbrowser.open(_f)
                except:
                    pass


class FaGui(tk.Frame):
    def __init__(self, master=None):

        self.path = r"" + os.path.dirname(os.path.abspath(__file__))
        self.path_lvl_up = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        self.condition = ""
        self.condition_list = fg.get_subdir_names(self.path_lvl_up + "\\01_Conditions\\")
        self.condition_selected = False
        self.errors = False
        self.feature_list = []
        self.features = cdef.Features(False)
        self.habitat = False
        self.manning_n = 0.0473934
        self.mapping = False
        self.mt_template_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..')) + "\\ModifyTerrain\\.templates\\"
        self.out_lyt_dir = []
        self.out_ras_dir = []
        self.reaches = cdef.Reaches()
        self.reach_ids_applied = []  # self.reaches.id_xlsx ## initial: all reaches (IDs)
        self.reach_names_applied = []  # self.reaches.names_xlsx ## initial: all reaches (full names)
        self.reach_lookup_needed = False
        self.reach_reader = cmio.Read()
        self.unit = "us"
        self.verified = False
        self.wild = False

        # Construct the Frame object.
        tk.Frame.__init__(self, master)
        # if imported from master GUI, redefine master as highest level (ttk.Notebook tab container)
        if __name__ != '__main__':
            self.master = self.master.master
        self.pack(expand=True, fill=tk.BOTH)

        self.set_geometry()

        # GUI OBJECT VARIABLES
        self.gui_condition = tk.StringVar()
        self.gui_interpreter = tk.StringVar()
        self.extent_type = tk.StringVar()

        # LABELS
        self.l_s_feat = tk.Label(self, text="Selected features: ")
        self.l_s_feat.grid(sticky=tk.W, row=0, column=0, padx=self.xd, pady=self.yd)
        self.l_features = tk.Label(self, fg="red",
                                   text="Choose from \'Add Features\' Menu (required for Raster Maker only)")
        self.l_features.grid(sticky=tk.W, row=0, column=1, columnspan=6, padx=self.xd, pady=self.yd)
        self.l_reach_label = tk.Label(self, text="Reaches:")
        self.l_reach_label.grid(sticky=tk.W, row=1, column=0, columnspan=1, padx=self.xd, pady=self.yd * 2)
        self.l_reaches = tk.Label(self, fg="red", text="Select from Reaches menu (required for Raster Maker only)")
        self.l_reaches.grid(sticky=tk.W, row=1, column=1, columnspan=6, padx=self.xd, pady=self.yd * 2)
        self.l_condition = tk.Label(self, text="Condition: \n")
        self.l_condition.grid(sticky=tk.W, row=3, column=0, columnspan=3, padx=self.xd, pady=self.yd)
        self.b_v_condition = tk.Button(self, fg="red", text="Select \n Raster Maker only",
                                       command=lambda: self.select_condition)
        self.b_v_condition.grid(sticky=tk.W, row=3, column=3, padx=self.xd, pady=self.yd)
        self.l_n = tk.Label(self, text="Roughness (Manning\'s n): %.3f " % self.manning_n)
        self.l_n.grid(sticky=tk.W, row=10, column=0, columnspan=3, padx=self.xd, pady=self.yd)

        # DROP DOWN ENTRIES (SCROLL BARS)
        self.sb_condition = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.sb_condition.grid(sticky=tk.W, row=3, column=2, padx=0, pady=self.yd)
        self.lb_condition = tk.Listbox(self, height=3, width=14, yscrollcommand=self.sb_condition.set)
        for e in self.condition_list:
            self.lb_condition.insert(tk.END, e)
        self.lb_condition.grid(sticky=tk.W, row=3, column=1, padx=self.xd, pady=self.yd)
        self.sb_condition.config(command=self.lb_condition.yview)

        # BUTTONS
        self.b_mod_r = tk.Button(self, width=25, bg="white", text="Modify raster input", command=lambda:
                                 self.open_inp_file("input_definitions.inp"))
        self.b_mod_r.grid(sticky=tk.EW, row=5, column=0, columnspan=2, padx=self.xd, pady=self.yd)
        self.b_mod_r["state"] = "disabled"
        self.b_mod_m = tk.Button(self, width=25, bg="white", text="Modify global map parameters", command=lambda:
                                 self.open_inp_file("mapping.inp"))
        self.b_mod_m.grid(sticky=tk.EW,row=5, column=2, columnspan=2, padx=self.xd, pady=self.yd)
        self.b_mod_th = tk.Button(self, width=25, bg="white", text="Modify survival threshold values", command=lambda:
                                  self.open_inp_file("threshold_values.xlsx"))
        self.b_mod_th.grid(sticky=tk.EW, row=6, column=0, columnspan=2, padx=self.xd, pady=self.yd)
        self.b_mod_rea = tk.Button(self, width=25, bg="white", text="Modify river/reach extents", command=lambda:
                                   self.open_inp_file("computation_extents.xlsx", "MT"))
        self.b_mod_rea.grid(sticky=tk.EW, row=6, column=2, columnspan=2, padx=self.xd, pady=self.yd)
        self.b_n = tk.Button(self, width=25, bg="white", text="Change / Info", command=lambda: self.set_n())
        self.b_n.grid(sticky=tk.W, row=10, column=2, columnspan=5, padx=self.xd, pady=self.yd)

        self.make_menu()

        # CHECK BOXES(CHECKBUTTONS)
        self.cb_lyt = tk.Checkbutton(self, text="Include mapping after raster preparation", command=lambda:
                                     self.mod_mapping())
        self.cb_lyt.grid(sticky=tk.W, row=7, column=0, columnspan=4, padx=self.xd, pady=self.yd)
        self.cb_wild = tk.Checkbutton(self, text="Apply wildcard raster to spatially confine analysis", command=lambda:
                                      self.mod_wild())
        self.cb_wild.grid(sticky=tk.W, row=8, column=0, columnspan=5, padx=self.xd, pady=self.yd)

        self.cb_habitat = tk.Checkbutton(self, text="Apply habitat matching",
                                         command=lambda: self.mod_habitat())
        self.cb_habitat.grid(sticky=tk.W, row=9, column=0, columnspan=5, padx=self.xd, pady=self.yd)
        self.cb_extent = tk.Checkbutton(self, text="Limit computation extent to background (back.tif) raster",
                                        variable=self.extent_type, onvalue="raster", offvalue="standard")
        self.cb_extent.grid(sticky=tk.W, row=11, column=0, columnspan=5, padx=self.xd, pady=self.yd)
        self.cb_extent.select()


    def set_geometry(self):
        # ARRANGE GEOMETRY
        # width and height of the window.
        self.ww = 700
        self.wh = 490
        self.xd = 5  # distance holder in x-direction (pixel)
        self.yd = 5  # distance holder in y-direction (pixel)
        # height and location
        self.wx = (self.master.winfo_screenwidth() - self.ww) / 2
        self.wy = (self.master.winfo_screenheight() - self.wh) / 2
        self.master.geometry("%dx%d+%d+%d" % (self.ww, self.wh, self.wx, self.wy))
        if __name__ == '__main__':
            self.master.title("Lifespan Design")  # window title
            self.master.iconbitmap(self.path_lvl_up + "\\.site_packages\\templates\\code_icon.ico")

    def make_menu(self):
        # DROP DOWN MENU
        # menu does not need packing - see tkinter manual page 44ff
        self.mbar = tk.Menu(self.master)  # create new menubar
        self.master.config(menu=self.mbar)  # attach it to the root window

        # FEATURE DROP DOWN
        self.featmenu = tk.Menu(self.mbar, tearoff=0)  # create new menu
        self.mbar.add_cascade(label="Add Features", menu=self.featmenu)  # attach it to the menubar
        # add menu entries
        self.build_feat_menu()

        # REACH  DROP DOWN
        self.reach_lookup_needed = False
        self.reachmenu = tk.Menu(self.mbar, tearoff=0)  # create new menu
        self.mbar.add_cascade(label="Reaches", menu=self.reachmenu)  # attach it to the menubar
        self.build_reach_menu()

        # RUN DROP DOWN
        self.runmenu = tk.Menu(self.mbar, tearoff=0)  # create new menu
        self.mbar.add_cascade(label="Run", menu=self.runmenu)  # attach it to the menubar
        self.runmenu.add_command(label="Verify settings", command=lambda: self.verify())
        self.runmenu.add_command(label="Run: Raster Maker", command=lambda: self.run_raster_maker())
        self.runmenu.add_command(label="Run: Map Maker", command=lambda: self.run_map_maker())

        # UNIT SYSTEM DROP DOWN
        self.unitmenu = tk.Menu(self.mbar, tearoff=0)  # create new menu
        self.mbar.add_cascade(label="Units", menu=self.unitmenu)  # attach it to the menubar
        self.unitmenu.add_command(label="[current]  U.S. customary", background="pale green")
        self.unitmenu.add_command(label="[             ]  SI (metric)", command=lambda: self.unit_change())

        # CLOSE DROP DOWN
        self.closemenu = tk.Menu(self.mbar, tearoff=0)  # create new menu
        self.mbar.add_cascade(label="Close", menu=self.closemenu)  # attach it to the menubar
        self.closemenu.add_command(label="Credits", command=lambda: self.show_credits())
        self.closemenu.add_command(label="Quit program", command=lambda: self.myquit())

    def add_reach(self, reach):
        if str(reach).__len__() < 1:
            # appends all available reaches
            self.reach_names_applied = fg.dict_values2list(self.reaches.name_dict.values())
            self.reach_ids_applied = fg.dict_values2list(self.reaches.id_dict.values())
            label_text = "All"
            self.l_reaches.config(fg="dark slate gray", text=label_text)
        else:
            if not(reach == "clear"):
                if not(reach in self.reach_names_applied):
                    self.reach_names_applied.append(self.reaches.name_dict[reach])
                    self.reach_ids_applied.append(self.reaches.id_dict[reach])
                if self.reach_names_applied.__len__() > 6:
                    if self.reach_names_applied.__len__() == 8:
                        label_text = "All"
                    else:
                        label_text = "Multiple (> 6)"
                else:
                    label_text = ", ".join(self.reach_names_applied)
                self.l_reaches.config(fg="dark slate gray", text=label_text)
            else:
                self.reach_names_applied = []
                self.reach_ids_applied = []
                self.l_reaches.config(fg="red", text="Select from \'Reaches\' Menu")

    def build_feat_menu(self):
        self.featmenu.add_command(label="Add: ALL", command=lambda: self.define_feature(""))

        for feat in self.features.name_list:
            menu_name = "Add: " + str(feat)
            self.featmenu.add_command(label=menu_name, command=partial(self.define_feature, feat))
        self.featmenu.add_command(label="_____________________________")
        self.featmenu.add_command(label="Group layer: Terraforming", command=lambda: self.define_feature("framework"))
        self.featmenu.add_command(label="Group layer: Plantings", command=lambda: self.define_feature("plants"))
        self.featmenu.add_command(label="Group layer: Bioengineering", command=lambda: self.define_feature("toolbox"))
        self.featmenu.add_command(label="Group layer: Maintenance", command=lambda: self.define_feature("complementary"))
        self.featmenu.add_command(label="CLEAR ALL", command=lambda: self.define_feature("clear"))

    def build_reach_menu(self):
        if not self.reach_lookup_needed:
            self.reachmenu.add_command(label="DEFINE REACHES", command=lambda: self.define_reaches())
            self.reachmenu.add_command(label="RE-BUILD MENU", command=lambda: self.build_reach_menu())
            self.reachmenu.add_command(label="_____________________________")
            self.reachmenu.add_command(label="ALL", command=lambda: self.add_reach(""))
            self.reachmenu.add_command(label="CLEAR ALL", command=lambda: self.add_reach("clear"))
            self.reachmenu.add_command(label="_____________________________")
            self.reachmenu.add_command(label=self.reaches.name_dict["reach_00"], command=lambda: self.add_reach("reach_00"))
            self.reachmenu.add_command(label=self.reaches.name_dict["reach_01"], command=lambda: self.add_reach("reach_01"))
            self.reachmenu.add_command(label=self.reaches.name_dict["reach_02"], command=lambda: self.add_reach("reach_02"))
            self.reachmenu.add_command(label=self.reaches.name_dict["reach_03"], command=lambda: self.add_reach("reach_03"))
            self.reachmenu.add_command(label=self.reaches.name_dict["reach_04"], command=lambda: self.add_reach("reach_04"))
            self.reachmenu.add_command(label=self.reaches.name_dict["reach_05"], command=lambda: self.add_reach("reach_05"))
            self.reachmenu.add_command(label=self.reaches.name_dict["reach_06"], command=lambda: self.add_reach("reach_06"))
            self.reachmenu.add_command(label=self.reaches.name_dict["reach_07"], command=lambda: self.add_reach("reach_07"))
            self.reach_lookup_needed = True
        else:
            # re-build reach names if spreadsheet was modified
            self.reaches.names_xlsx = self.reach_reader.get_reach_info("full_name")
            self.reaches.name_dict = dict(zip(self.reaches.internal_id, self.reaches.names_xlsx))
            self.reachmenu.entryconfig(6, label=self.reaches.name_dict["reach_00"])
            self.reachmenu.entryconfig(7, label=self.reaches.name_dict["reach_01"])
            self.reachmenu.entryconfig(8, label=self.reaches.name_dict["reach_02"])
            self.reachmenu.entryconfig(9, label=self.reaches.name_dict["reach_03"])
            self.reachmenu.entryconfig(10, label=self.reaches.name_dict["reach_04"])
            self.reachmenu.entryconfig(11, label=self.reaches.name_dict["reach_05"])
            self.reachmenu.entryconfig(12, label=self.reaches.name_dict["reach_06"])
            self.reachmenu.entryconfig(13, label=self.reaches.name_dict["reach_07"])

    def define_feature(self, feature_name):
        if feature_name.__len__() < 1:
            # append all available
            self.feature_list = self.features.name_list
            self.l_features.config(fg="SteelBlue", text="All")
        else:
            if not(feature_name == "clear"):
                if not(feature_name == "framework"):
                    if not(feature_name == "toolbox"):
                        if not(feature_name == "complementary"):
                            if not (feature_name == "plants"):
                                if not(feature_name in self.feature_list):
                                    # append single feature to analysis list
                                    self.feature_list.append(str(feature_name))
                            else:
                                # append plant features
                                self.feature_list = self.features.name_list_plants
                        else:
                            # append complementary features
                            self.feature_list = self.features.name_list_complement
                    else:
                        # append toolbox features
                        self.feature_list = self.features.name_list_toolbox
                else:
                    # append framework features
                    self.feature_list = self.features.name_list_framework
                self.l_features.config(fg="SteelBlue", text=", ".join(self.feature_list))
            else:
                # clear
                self.feature_list = []
                self.l_features.config(fg="red",
                                       text="Choose from \'Add Features\' Menu (required for Raster Maker only)")

    def define_reaches(self):
        try:
            webbrowser.open(self.mt_template_dir + "computation_extents.xlsx")
            self.reach_lookup_needed = True  # tells build_reachmenu that lookup of modified spreasheet info is needed
        except:
            showinfo("ERROR", "Cannot open the file\n" + self.mt_template_dir + "computation_extents.xlsx")

    def mod_habitat(self):
        if not self.habitat:
            self.habitat = True
        else:
            self.habitat = False

    def mod_mapping(self):
        if not self.mapping:
            self.mapping = True
        else:
            self.mapping = False

    def mod_wild(self):
        if not self.wild:
            self.wild = True
        else:
            self.wild = False

    def myquit(self):
        if askokcancel("Close", "Do you really wish to quit?"):
            tk.Frame.quit(self)

    def open_inp_file(self, filename, *args):
        # args[0] = STR indicating other modules
        try:
            if str(args[0]) == "MT":
                _f = r'' + os.path.abspath(
                    os.path.join(os.path.dirname(__file__), '..')) + "\\ModifyTerrain\\.templates\\" + filename
            else:
                _f = self.path_lvl_up + "\\01_Conditions\\" + self.condition + "\\" + filename
        except:
            try:
                _f = self.path_lvl_up + "\\01_Conditions\\" + self.condition + "\\" + filename
            except:
                _f = None

        if os.path.isfile(_f):
            try:
                webbrowser.open(_f)
            except:
                showinfo("ERROR ", "Cannot open " + str(_f) +
                         ".\nMake sure that the file was created (Get Started tab) and that your operating system has a standard application defined for *.inp-files.")
        else:
            showinfo("ERROR ",
                     "The file " + str(_f) + " does not exist.\nUse the Get Started tab to create and input file.")

    def open_log_file(self):
        logfilenames = ["error.log", "rasterlogfile.log", "logfile.log", "map_logfile.log", "mxd_logfile.log"]
        for filename in logfilenames:
            _f = r'' + os.path.dirname(os.path.abspath(__file__)) + "\\" + filename
            if os.path.isfile(_f):
                try:
                    webbrowser.open(_f)
                except:
                    pass

    def run_raster_maker(self):
        showinfo("INFORMATION",
                 " Analysis takes a while. \n Python windows seem unresponsive in the meanwhile. \n Check console messages.\n \n PRESS OK TO START")
        if not self.verified:
            self.verify()
        if self.verified:
            run = RunGui(self)
            out_dir = run.gui_raster_maker(self.condition, self.reach_ids_applied, self.feature_list,
                                           self.mapping, self.habitat, self.unit, self.wild, self.manning_n,
                                           str(self.extent_type.get()))
            if self.mapping:
                self.out_lyt_dir = out_dir
            else:
                self.out_ras_dir = out_dir
            run.gui_quit()
            self.cb_lyt.destroy()
            self.cb_habitat.destroy()
            self.cb_wild.destroy()
            self.master.bell()
            tk.Button(self, width=25, bg="pale green", text="QUIT\n", command=lambda:
                      tk.Frame.quit(self)).grid(sticky=tk.EW, row=9, column=0, columnspan=2, padx=self.xd,
                                                pady=self.yd)
            if not self.mapping:
                tk.Button(self, bg="salmon", width=25, text="IMPORTANT\n Read logfile(s)", command=lambda:
                          self.open_log_file()).grid(sticky=tk.EW, row=9, column=2, columnspan=2, padx=self.xd,
                                                     pady=self.yd)
            else:
                tk.Button(self, bg="gold", width=25, text="IMPORTANT\n Read logfile(s) from Map Maker",
                          command=lambda:
                          self.open_log_file()).grid(sticky=tk.EW, row=9, column=2, columnspan=2, padx=self.xd,
                                                     pady=self.yd)
            if self.habitat:
                tk.Label(self, fg="forest green", text=
                            "Applied habitat matching").grid(
                            sticky=tk.W, row=8, column=0, columnspan=6, padx=self.xd, pady=self.yd)

    def run_map_maker(self):
        run = RunGui(self)
        if self.out_ras_dir.__len__() < 1:
            showinfo("INFORMATION", "Choose folder that contains lifespan and design rasters.")
            self.out_ras_dir = [askdirectory(initialdir=".") + "/"]
        if not self.reach_ids_applied.__len__() < 1:
            self.out_lyt_dir = run.gui_map_maker(self.out_ras_dir, self.reach_ids_applied)
        else:
            self.out_lyt_dir = run.gui_map_maker(self.out_ras_dir, None)
        run.gui_quit()
        self.cb_lyt.destroy()
        self.cb_habitat.destroy()
        self.cb_wild.destroy()
        self.master.bell()
        tk.Button(self, width=25, bg="pale green", text="QUIT\n",
                  command=lambda:
                  tk.Frame.quit(self)).grid(sticky=tk.EW, row=9, column=0, columnspan=2, padx=self.xd,
                                            pady=self.yd)
        tk.Button(self, bg="pale green", width=25, text="IMPORTANT\n Read logfile(s) from Map Maker", command=lambda:
                  self.open_log_file()).grid(sticky=tk.EW, row=9, column=2, columnspan=2, padx=self.xd, pady=self.yd)

    def set_n(self):
        sub_frame = PopUpWindow(self.master)
        self.b_n["state"] = "disabled"
        self.master.wait_window(sub_frame.top)
        self.b_n["state"] = "normal"
        self.manning_n = float(sub_frame.value)
        self.l_n.config(text="Roughness (Manning\'s n): %.3f " % self.manning_n)
        if float(self.manning_n) > 0.2:
            showinfo("WARNING", "That seems to be an incredibly rough channel. Consider revising the new value for Manning\'s n")

    def select_condition(self):
        try:
            items = self.lb_condition.curselection()
            self.condition = [self.condition_list[int(item)] for item in items][0]
            input_dir = self.path_lvl_up + "\\01_Conditions\\" + str(self.condition)
            if os.path.exists(input_dir) or self.mapping:
                self.b_v_condition.config(fg="forest green", text="Selected:\n" + self.condition)
                self.b_mod_r["state"] = "normal"
                self.condition_selected = True
                return ""
            else:
                self.b_v_condition.config(fg="red", text="ERROR")
                self.errors = True
                self.verified = False
                return "Invalid file structure (non-existent directory /01_Conditions/CONDITION/)."
        except:
            self.errors = True
            self.verified = False
            return "Invalid entry for \'Condition\'."

    def show_credits(self):
        showinfo("Credits", fg.get_credits())

    def unit_change(self):
        if self.unit == "si":
            new_unit = "us"
            self.unitmenu.delete(0, 1)
            self.unitmenu.add_command(label="[current]  U.S. customary", background="pale green")
            self.unitmenu.add_command(label="[             ]  SI (metric)", command=lambda: self.unit_change())
            self.master.bell()
            showinfo("UNIT CHANGE", "Unit system changed to U.S. customary.")
        else:
            new_unit = "si"
            self.unitmenu.delete(0, 1)
            self.unitmenu.add_command(label="[             ]  U.S. customary", command=lambda: self.unit_change())
            self.unitmenu.add_command(label="[current]  SI (metric)", background="pale green")
            self.master.bell()
            showinfo("UNIT CHANGE", "Unit system changed to SI (metric).\n\nThreshold values need separate definition in threshold_values.xlsx (click button \'Modify survival threshold values\').")
        self.unit = new_unit

    def verify(self, *args):
        # args[0] = True limits verification to condition only
        try:
            full_check = args[0]
        except:
            full_check = True

        error_msg = []
        self.verified = True
        if full_check:
            try:
                import feature_analysis
            except:
                error_msg.append("Check installation of feature_analysis package.")
                self.verified = False
                self.errors = True
            if not (self.feature_list.__len__() > 0):
                error_msg.append("For RasterMaker: Choose at least one feature.")
                self.verified = False
                self.errors = True
            else:
                if self.feature_list.__len__() < 6:
                    self.l_features.config(fg="forest green", text=", ".join(self.feature_list))
                else:
                    self.l_features.config(fg="forest green", text="Many / All")
            try:
                if not (sys.version_info.major == 3):
                    error_msg.append("Wrong Python interpreter (Required: Python3).")
                    self.errors = True
                    self.verified = False
            except:
                pass
            try:
                import arcpy
            except:
                error_msg.append("Wrong Python interpreter (arcpy not available).")
                self.errors = True
                self.verified = False

        if not self.condition_selected:
            condition_selection = self.select_condition()
            error_msg.append(condition_selection)
        if self.errors:
            self.master.bell()
            showinfo("VERIFICATION ERROR(S)", "\n ".join(error_msg))
            self.errors = False

    def __call__(self):
        self.mainloop()


# enable script to run stand-alone
if __name__ == "__main__":
    FaGui().mainloop()
