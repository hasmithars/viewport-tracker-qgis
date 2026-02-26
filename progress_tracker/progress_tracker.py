# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Viewport Tracker
                                 A QGIS plugin
 Track areas of the map you have already viewed
 ***************************************************************************/
"""
import os
import tempfile
from pathlib import Path

from qgis.PyQt.QtCore import QSettings, Qt
from qgis.PyQt.QtGui import QIcon, QColor, QKeySequence
from qgis.PyQt.QtWidgets import QAction, QMessageBox, QShortcut
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsFeature,
    QgsGeometry,
    QgsField,
    QgsFields,
    QgsCoordinateReferenceSystem,
    QgsVectorFileWriter,
    QgsWkbTypes,
    QgsSymbol,
    QgsFillSymbol,
    QgsSimpleFillSymbolLayer,
    QgsEffectStack,
    QgsOuterGlowEffect,
    QgsRectangle,
    QgsMapLayerType
)
from qgis.gui import QgsMapCanvas


class ViewportTrackerPlugin:
    """QGIS Plugin to track viewed map areas."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.plugin_dir = os.path.dirname(__file__)
        self.action = None
        self.toolbar = None
        self.progress_layer = None
        self.gpkg_path = None
        self.is_active = False
        self.layer_was_removed = False
        self.capture_shortcut = None

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        
        # Create action that will trigger the plugin activation/deactivation
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        self.action = QAction(
            QIcon(icon_path),
            "Toggle Viewport Tracker",
            self.iface.mainWindow()
        )
        
        # Make it checkable (toggle button)
        self.action.setCheckable(True)
        self.action.setChecked(False)
        
        # Connect to toggle signal
        self.action.toggled.connect(self.toggle_activation)
        
        # Add toolbar button
        self.iface.addToolBarIcon(self.action)
        
        # Create a SEPARATE keyboard shortcut for capturing (not on the action)
        self.capture_shortcut = QShortcut(QKeySequence("P"), self.iface.mainWindow())
        self.capture_shortcut.activated.connect(self.capture_extent)
        
        # Connect to layer removed signal
        QgsProject.instance().layersRemoved.connect(self.on_layers_removed)
        
        # Connect to project closing signal to clean up temp file
        QgsProject.instance().writeProject.connect(self.on_project_saved)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        # Disconnect signals
        try:
            QgsProject.instance().layersRemoved.disconnect(self.on_layers_removed)
            QgsProject.instance().writeProject.disconnect(self.on_project_saved)
        except:
            pass
        
        # Remove shortcut
        if self.capture_shortcut:
            self.capture_shortcut.setEnabled(False)
            self.capture_shortcut.deleteLater()
            self.capture_shortcut = None
        
        if self.action:
            self.iface.removeToolBarIcon(self.action)
            self.action = None

    def get_gpkg_path(self):
        """Get the path for the GPKG file in the temp directory."""
        temp_dir = tempfile.gettempdir()
        gpkg_name = "qgis_viewport_tracker_temp.gpkg"
        return os.path.join(temp_dir, gpkg_name)

    def on_layers_removed(self, layer_ids):
        """Handle layer removal event."""
        try:
            # Check if we have a progress layer and if it was removed
            if self.progress_layer and self.progress_layer.id() in layer_ids:
                self.layer_was_removed = True
                self.progress_layer = None
                
                if self.is_active:
                    # Recreate the layer if plugin is still active
                    self.iface.messageBar().pushMessage(
                        "Viewport Tracker",
                        "Progress layer was removed. Creating a new one...",
                        level=1,  # Warning
                        duration=2
                    )
                    self.create_progress_layer()
        except RuntimeError:
            # Layer object was deleted - silently handle it
            self.progress_layer = None
            self.layer_was_removed = True

    def on_project_saved(self):
        """Handle project save event."""
        # Don't clean up on save, only on actual exit
        pass

    def toggle_activation(self, checked):
        """Toggle plugin activation state."""
        self.is_active = checked
        
        if checked:
            # Activating plugin
            self.activate_plugin()
        else:
            # Deactivating plugin
            self.deactivate_plugin()

    def activate_plugin(self):
        """Activate the viewport tracker."""
        # Check if we need to create a new GPKG file
        need_new_file = False
        self.gpkg_path = self.get_gpkg_path()
        
        # Check if layer exists in project
        layers = QgsProject.instance().mapLayersByName('progress')
        if layers:
            try:
                # Verify the layer is still valid
                layer = layers[0]
                if layer.isValid():
                    self.progress_layer = layer
                else:
                    need_new_file = True
            except RuntimeError:
                # Layer was deleted
                need_new_file = True
        else:
            need_new_file = True
        
        # Create new layer if needed
        if need_new_file:
            # Delete old file if it exists and create fresh one
            if os.path.exists(self.gpkg_path):
                try:
                    os.remove(self.gpkg_path)
                except:
                    pass  # Ignore if we can't delete
            
            if not self.create_progress_layer():
                self.action.setChecked(False)
                self.is_active = False
                return
        
        # Show activation message
        self.iface.messageBar().pushMessage(
            "Viewport Tracker",
            "Viewport Tracker ACTIVATED. Press 'P' to capture view extents.",
            level=3,  # Success (blue)
            duration=3
        )

    def deactivate_plugin(self):
        """Deactivate the viewport tracker."""
        # Show deactivation message
        self.iface.messageBar().pushMessage(
            "Viewport Tracker",
            "Viewport Tracker DEACTIVATED.",
            level=1,  # Info
            duration=2
        )
        
        # Keep the layer visible but stop capturing

    def layer_is_valid(self):
        """Check if progress layer is still valid."""
        if not self.progress_layer:
            return False
        
        try:
            # Try to access layer properties to check if it's still valid
            return self.progress_layer.isValid()
        except RuntimeError:
            # Layer object has been deleted
            self.progress_layer = None
            return False

    def create_progress_layer(self):
        """Create a new progress layer with GPKG backend."""
        self.gpkg_path = self.get_gpkg_path()
        
        # Define fields
        fields = QgsFields()
        fields.append(QgsField("id", 4))  # QVariant.Int
        
        # Get CRS from canvas
        crs = self.canvas.mapSettings().destinationCrs()
        
        # Create GPKG file
        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "GPKG"
        options.fileEncoding = "UTF-8"
        options.layerName = "progress"
        
        writer = QgsVectorFileWriter.create(
            self.gpkg_path,
            fields,
            QgsWkbTypes.Polygon,
            crs,
            QgsProject.instance().transformContext(),
            options
        )
        
        if writer.hasError() != QgsVectorFileWriter.NoError:
            error_msg = f"Error creating GPKG file: {writer.errorMessage()}"
            self.iface.messageBar().pushMessage(
                "Viewport Tracker",
                error_msg,
                level=2,  # Warning level
                duration=5
            )
            return False
        
        del writer  # Close the writer
        
        # Load the layer
        layer = QgsVectorLayer(self.gpkg_path + "|layername=progress", "progress", "ogr")
        if not layer.isValid():
            self.iface.messageBar().pushMessage(
                "Viewport Tracker",
                f"Failed to load progress layer from {self.gpkg_path}",
                level=2,  # Warning level
                duration=5
            )
            return False
        
        # Verify the layer can be edited
        if not layer.dataProvider().capabilities() & layer.dataProvider().AddFeatures:
            self.iface.messageBar().pushMessage(
                "Viewport Tracker",
                "Layer does not support adding features",
                level=2,  # Warning level
                duration=5
            )
            return False
        
        self.progress_layer = layer
        QgsProject.instance().addMapLayer(layer)
        self.apply_neon_symbology()
        
        # Show success message
        self.iface.messageBar().pushMessage(
            "Viewport Tracker",
            f"Progress layer created at: {self.gpkg_path}",
            level=0,  # Info level
            duration=3
        )
        
        return True

    def apply_neon_symbology(self):
        """Apply red neon effect symbology to the progress layer."""
        if not self.layer_is_valid():
            return
        
        # Create fill symbol
        symbol = QgsFillSymbol.createSimple({
            'color': '255,0,0,100',  # Red with transparency
            'outline_color': '255,0,0,255',  # Solid red outline
            'outline_width': '0.5',
            'outline_style': 'solid'
        })
        
        # Create outer glow effect for neon appearance
        glow_effect = QgsOuterGlowEffect()
        glow_effect.setColor(QColor(255, 0, 0, 200))
        glow_effect.setBlurLevel(10)
        glow_effect.setSpread(2.0)
        glow_effect.setOpacity(0.8)
        
        # Create effect stack and add glow
        effect_stack = QgsEffectStack()
        effect_stack.appendEffect(glow_effect)
        
        # Apply effect to symbol
        symbol.symbolLayers()[0].setPaintEffect(effect_stack)
        
        # Set the symbol to the layer
        self.progress_layer.renderer().setSymbol(symbol)
        self.progress_layer.triggerRepaint()

    def capture_extent(self):
        """Capture the current map canvas extent and add it as a box."""
        # Only capture if plugin is active
        if not self.is_active:
            self.iface.messageBar().pushMessage(
                "Viewport Tracker",
                "Plugin is not active. Click the toolbar button to activate it first.",
                level=1,  # Warning level
                duration=2
            )
            return
        
        # Check if layer is still valid, recreate if needed
        if not self.layer_is_valid():
            if not self.create_progress_layer():
                return
        
        # Get current extent
        extent = self.canvas.extent()
        
        # Validate extent
        if extent.isEmpty():
            self.iface.messageBar().pushMessage(
                "Viewport Tracker",
                "Canvas extent is empty. Please load a layer or zoom to an area.",
                level=1,  # Warning level
                duration=3
            )
            return
        
        # Create polygon geometry from extent
        rect_geom = QgsGeometry.fromRect(extent)
        
        # Validate geometry
        if rect_geom.isNull() or not rect_geom.isGeosValid():
            self.iface.messageBar().pushMessage(
                "Viewport Tracker",
                "Failed to create valid geometry from extent",
                level=2,  # Warning level
                duration=3
            )
            return
        
        # Create feature with proper fields
        feature = QgsFeature(self.progress_layer.fields())
        feature.setGeometry(rect_geom)
        
        # Set attributes
        feature.setAttribute('id', self.progress_layer.featureCount() + 1)
        
        # Add feature to layer
        self.progress_layer.startEditing()
        success = self.progress_layer.addFeature(feature)
        
        if not success:
            self.iface.messageBar().pushMessage(
                "Viewport Tracker",
                "Failed to add feature to layer",
                level=2,  # Warning level
                duration=3
            )
            self.progress_layer.rollBack()
            return
        
        # Commit changes to save to GPKG
        if not self.progress_layer.commitChanges():
            error_msg = self.progress_layer.commitErrors()
            self.iface.messageBar().pushMessage(
                "Viewport Tracker",
                f"Failed to commit changes: {', '.join(error_msg)}",
                level=2,  # Warning level
                duration=5
            )
            return
        
        # Refresh canvas to show the new box
        self.progress_layer.triggerRepaint()
        self.canvas.refresh()

