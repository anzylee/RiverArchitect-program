# !/usr/bin/python
try:
    import sys, os
except:
    print("ExceptionERROR: Missing fundamental packages (required: os, sys).")

try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\..')) + "\\LifespanDesign\\")
    from cThresholdDirector import *
except:
    print("ExceptionERROR: cGravel cannot find cFeatureLifespan (need ThresholdDirector).")


class GravelInStream:
    # This is the Gravel augmentation instream class
    # __call__()

    def __init__(self, feat_id):
        self.parameter_list = ["mobile_grains", "mu", "ds_stable_grains"]  # governs analysis HIERARCHY!
        self.id = feat_id

        thresh = ThresholdDirector(feat_id)
        try:
            self.mu_bad = thresh.get_thresh_value("mu_bad")
        except:
            self.mu_bad = []
        try:
            self.mu_good = thresh.get_thresh_value("mu_good")
        except:
            self.mu_good = []
        try:
            self.mu_method = int(thresh.get_thresh_value("mu_method"))
        except:
            self.mu_method = -1
        try:
            if (self.mu_bad.__len__() == 0) and (self.mu_good.__len__() == 0):
                self.mu_method = -1
        except:
            pass
        self.threshold_freq = thresh.get_thresh_value("freq")
        self.threshold_taux = thresh.get_thresh_value("taux")
        thresh.close_wb()

    def __call__(self):
        print("Class Info: <type> = Feature: Gravel augmentation (Instream)")


class GravelOutStream:
    # This is the Gravel augmentation outstream class
    # __call__()

    def __init__(self, feat_id):
        self.parameter_list = ["mobile_grains", "scour", "mu", "ds_stable_grains"]  # governs analysis HIERARCHY!
        self.id = feat_id

        thresh = ThresholdDirector(feat_id)
        try:
            self.mu_bad = thresh.get_thresh_value("mu_bad")
        except:
            self.mu_bad = []
        try:
            self.mu_good = thresh.get_thresh_value("mu_good")
        except:
            self.mu_good = []
        try:
            self.mu_method = int(thresh.get_thresh_value("mu_method"))
        except:
            self.mu_method = -1
        try:
            if (self.mu_bad.__len__() == 0) and (self.mu_good.__len__() == 0):
                self.mu_method = -1
        except:
            pass
        self.threshold_freq = thresh.get_thresh_value("freq")
        self.threshold_taux = thresh.get_thresh_value("taux")
        self.threshold_scour = thresh.get_thresh_value("scour")
        thresh.close_wb()

    def __call__(self):
        print("Class Info: <type> = Feature: Gravel augmentation (Bank stockpile)")