import Rhino
import rhinoscriptsyntax as rs

file = rs.OpenFileName("Select file to import layers from:", extension="3dm")
if file:
    selectedFile = Rhino.FileIO.File3dm.Read(file)

if selectedFile:
    layers = selectedFile.Layers

for layer in layers:
    rs.AddLayer(name=layer.FullPath, color=layer.Color, visible=layer.IsVisible, locked=layer.IsLocked)
