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


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Autofill class from file Autofill.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .autofill import AutoFill
    return AutoFill(iface)
