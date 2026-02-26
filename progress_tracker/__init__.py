# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Viewport Tracker
                                 A QGIS plugin
 Track areas of the map you have already viewed
 ***************************************************************************/
"""


def classFactory(iface):
    """Load ViewportTrackerPlugin class from file progress_tracker.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .progress_tracker import ViewportTrackerPlugin
    return ViewportTrackerPlugin(iface)

