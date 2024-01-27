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

import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialogButtonBox, QDialog
from qgis.core import QgsFeatureRequest, QgsExpression
from qgis.core import QgsExpressionContext, QgsExpressionContextUtils
from qgis.core import QgsFieldProxyModel
from qgis.core import QgsMessageLog

from .progressbar import Progressbar


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'autofill_dialog.ui'))


class AutoFillDialog(QDialog, FORM_CLASS):
    def __init__(self, layer, field='', parent=None):
        """Constructor."""
        super(AutoFillDialog, self).__init__(parent)
        
        self.layer = layer
        self.field = field

        self.setupUi(self)
        
        self.setWindowTitle("AutoFill Attributes")

        self.mFieldComboBox.setFilters(QgsFieldProxyModel.String)       
        self.mFieldComboBox.setLayer(self.layer)
        self.mFieldComboBox.setField(self.field)
        self.mFieldComboBox.fieldChanged.connect(lambda fieldName: setattr(self,'field',fieldName))

        #Loop through fields and set a dictionary of field names and empty values
        self.fields_value = {}
        for field in self.layer.fields():
            self.fields_value[field.name()] = ''

        # Call the function to display the keys and the values of the dictionary
        self.display()

        # Set up the button box to apply the changes                
        self.ApplyButton.clicked.connect(self.fill_attributes)

        # Set up the button box to save the values in the dictionary
        self.SaveButton.clicked.connect(self.save)

        # Set up the button box to close the dialog
        self.CancelButton.clicked.connect(self.close)
        
        self.context = QgsExpressionContext()
        self.context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(self.layer))
    
    
    # Called when "Fill" button is pressed
    # Perform the fill on all features
    def fill_attributes(self):

        if not self.layer.isEditable():
            self.layer.startEditing()


        # Loop through the features and fill the attributes according to the dictionary
        with Progressbar(num_items=self.layer.featureCount()) as progb:
            for f in self.layer.getFeatures():
                progb.advance()
                for key, value in self.fields_value.items():
                    f[key] = value
                self.layer.updateFeature(f)        

    # Called when "Save" button is pressed
    # Save the value written in the inputLine box in the dictionary
    def save(self):
        self.fields_value[self.field] = self.inputLine.value()
        self.display()

    # Called when "Apply" button is pressed
    #Create a function to display the keys and the values of the dictionary
    def display(self):
        self.FieldLabel.setText('\n'.join(self.fields_value.keys()))
        self.ValueLabel.setText('\n'.join(self.fields_value.values()))
        