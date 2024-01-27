# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Autofill Attributes
                                 A QGIS plugin
 Simple screen to quickly perform find/replace on text in columns.
 Inspired by Sem Riemens' Find and Replace plugin : https://github.com/semriemens/qgis-plugin-findreplace
                             -------------------
        begin                : 2024-01-26
        copyright            : (C) 2024 by Steeve Beauvais
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

from qgis.gui import QgsGui, QgsMapLayerAction

# Import the code for the dialog
from .autofill_dialog import AutoFillDialog
import os.path


class AutoFill:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        self.plugin_dir = os.path.dirname(__file__)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        
        # Note: this is using a QgsMapLayerAction which will show in the right click menu on an attribute table.
        # It's not exactly what I wanted, as there is no way to get the selected field when using a QgsMapLayerAction
        # and also it will show up under the 'Actions' button in the main QGIS screen.
        # Another possibility would be to use a QgsAction with Field scope and the QgsActionManager, then add this action
        # to all layers. I decided against this as the action would then be saved and visible in people's project files.
        # I guess the ideal thing would be a QgsAttributeTableMapLayerAction, but I don't understand how to use that.
        # For now people will have to manually select the field to use.
        self.AutoFillAction = QgsMapLayerAction( "AutoFill",None, targets=QgsMapLayerAction.Target.SingleFeature )
        QgsGui.mapLayerActionRegistry().addMapLayerAction(self.AutoFillAction)
        
        self.AutoFillAction.triggeredForLayer.connect(self.run)
        self.AutoFillAction.triggeredForFeature.connect(self.run)
        
    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        QgsGui.mapLayerActionRegistry().removeMapLayerAction(self.AutoFillAction)
        del self.AutoFillAction

    def run(self, layer=None,feature=None):
        frd = AutoFillDialog(layer)
        
        frd.show()
        if frd.exec_():
            pass
        frd.deleteLater()
        del frd

