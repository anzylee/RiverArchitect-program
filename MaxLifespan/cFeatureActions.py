# !/usr/bin/python
try:
    import arcpy, sys, os, logging
except:
    print("ExceptionERROR: Missing fundamental packages (required: arcpy, os, sys, logging")

try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + "\\.site_packages\\riverpy\\")
    import config
    import cDefinitions as cDef
except:
    print("ExceptionERROR: Cannot find riverpy.")


class Director:
    def __init__(self, condition, *args):
        # args[0] is an optional input path
        self.condition = condition  # [str] state of planning situation, .e.g., "2008"
        self.logger = logging.getLogger("logfile")
        try:
            self.raster_input_path = args[0]
        except:
            self.raster_input_path = config.dir2lf + "Output\\Rasters\\" + str(self.condition) + "\\"

        arcpy.env.workspace = self.raster_input_path
        self.all_rasters = arcpy.ListRasters()
        if not self.all_rasters:
            self.all_rasters = []
        arcpy.env.workspace = config.dir2ml

    def append_ds_rasters(self, feature_list):
        raster_list = []
        if str(self.all_rasters).__len__() < 1:
            return []
        for feat in feature_list:
            for ras_name in self.all_rasters:
                if feat in ras_name:
                    if ras_name[0:2] == "ds":
                        ras_act = self.raster_input_path + ras_name
                        if os.path.isfile(ras_act + '.aux.xml') or os.path.isfile(ras_act) or os.path.isfile(ras_act + '.tif'):
                            raster_list.append(arcpy.Raster(ras_act))
                        else:
                            raster_list.append("")
        return raster_list

    def append_lf_rasters(self, feature_list):
        raster_list = []
        if str(self.all_rasters).__len__() < 1:
            return []
        for feat in feature_list:
            for ras_name in self.all_rasters:
                if feat in ras_name:
                    if ras_name[0:2] == "lf":
                        ras_act = self.raster_input_path + ras_name
                        if os.path.isfile(ras_act + '.aux.xml') or os.path.isfile(ras_act) or os.path.isfile(ras_act + '.tif'):
                            raster_list.append(arcpy.Raster(ras_act))
                        else:
                            raster_list.append("")
        return raster_list


class FeatureGroup(Director):
    # This class stores all information about Feature Groups (terraforming, plantings, bioengineering or connectivity)
    def __init__(self, condition, *args):
        try:
            # check if args[0] = alternative input path exists
            Director.__init__(self, condition, args[0])
        except:
            Director.__init__(self, condition)
        self.features = cDef.FeatureDefinitions()
        self.names = self.features.name_list_framework
        self.shortnames = self.features.id_list_framework
        self.ds_rasters = self.append_ds_rasters(self.shortnames)
        self.lf_rasters = self.append_lf_rasters(self.shortnames)


class Manager(FeatureGroup):
    # Manages feature layer assignments
    def __init__(self, condition, feature_type, *args):
        acceptable_types = ["terraforming", "plantings", "bioengineering", "connectivity"]
        if feature_type in acceptable_types:
            try:
                # check if args[0] = alternative input path exists
                FeatureGroup.__init__(self, condition, args[0])
            except:
                FeatureGroup.__init__(self, condition)
                self.logger.info("*** feature_type: " + str(feature_type))
        else:
            self.logger.info("ERROR: Invalid keyword for feature type.")
