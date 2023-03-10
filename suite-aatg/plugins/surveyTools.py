import math
import os

from PyQt5.QtWidgets import QAction, QMessageBox
from qgis.PyQt.QtGui import QIcon

from aa_utils import file_utils, map_utils


class SurveyTools:
    def __init__(self, iface):
        self.iface = iface
        self.toolbar = self.iface.addToolBar('AATG Vermessung')
        self.toolbar.setObjectName('AATGVermessung')
        self.toolbar.setToolTip('AATG Vermessung')

    def initGui(self):
        iconLfp = QIcon(os.path.dirname(__file__) + '/images/csv-icon.svg')
        self.actionLfp = QAction(iconLfp, "LFP to csv", self.iface.mainWindow())
        self.actionLfp.triggered.connect(self.exportLfp)
        self.toolbar.addAction(self.actionLfp)
        self.iface.addPluginToMenu("AATG Vermessung", self.actionLfp)

        icon = QIcon(os.path.dirname(__file__) + '/images/csv-icon.svg')
        self.actionLfp = QAction(icon, "Geometry to csv", self.iface.mainWindow())
        self.actionLfp.triggered.connect(self.exportGeometry)
        self.toolbar.addAction(self.actionLfp)
        self.iface.addPluginToMenu("AATG Vermessung", self.actionLfp)

    def unload(self):
        self.iface.removeToolBarIcon(self.actionLfp)
        del self.actionLfp

    def exportLfp(self):
        output = r'{}\lfp_export.csv'.format(file_utils.get_temp_dir())
        selected_features = map_utils.get_selected_features()

        if len(selected_features) < 1:
            QMessageBox.information(None, 'LFP to csv', 'No features selected')
            return

        fp_list = []
        for f in selected_features:
            fp_list.append([f['objectid'], f['lkoordx'], f['lkoordy'], f['hoehegeom'], f['punktzeichen']])

        with open(output, 'w') as f:
            for fp in fp_list:
                f.write("{}\n".format(','.join([str(e) if e else '' for e in fp])))
            f.close()

        QMessageBox.information(None, 'LFP to csv', 'Exported {} LFP to {}'.format(len(fp_list), output))

    def exportGeometry(self):
        output = r'{}\geometry_export.csv'.format(file_utils.get_temp_dir())
        selected_features = map_utils.get_selected_features()

        if len(selected_features) < 1:
            QMessageBox.information(None, 'Geometry to csv', 'No features selected')
            return

        pt_list = []
        for f in selected_features:
            i = 0
            for v in f.geometry().vertices():
                i += 1
                pt_list.append([f.attribute('objectid'), round(v.x(), 3), round(v.y(), 3),
                                round(v.z(), 3) if not math.isnan(v.z()) else '',
                                '{}.{}'.format(f.attribute('objectid'), i)])

        with open(output, 'w') as f:
            for pt in pt_list:
                f.write("{}\n".format(','.join([str(e) if e else '' for e in pt])))
            f.close()

        QMessageBox.information(None, 'Geometry to csv',
                                'Exported {} geometries to {}'.format(len(selected_features), output))
