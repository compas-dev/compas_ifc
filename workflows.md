# WORKFLOWS

This document outlines some typical workflows of using COMPAS IFC.

# Stand-alone

Using COMPAS IFC directly in python scripts to build IFC hierarchies, assign geometry representations, define properties, and export to IFC files.

### TODO
- [ ] Define default behavior to store full COMPAS geometry metadata to IFC properties, such as Mesh Vertex attributes.

# From COMPAS Model

Craeting a `COMPAS Model` first. And use a built-in `to_ifc_model()` funtion to directly convert to an COMPAS IFC model, or use `to_ifc(path)` to directly export to an IFC file.

### TODO
- [ ] Extend the `COMPAS Model` class to `BimModel`. Perhaps in a new package `COMPAS BIM`?

# From CAD

Export to IFC directly in a CAD environment where COMPAS IFC can be installed.

## From Rhino

Export from a Rhino file, where the layer structure corresponds to the IFC spatial hiearchy. The geometry representations are tranlsated in a lossless manner. Object UserData can be used to define IFC properties.

### TODO
- [ ] Rhino template file with correct layer structure and object types.
- [ ] Complete mapping from compas(_rhino) geometry to IFC geometry, especially BRep and Extrusion.
- [ ] Mechanism to define how UserData is mapped to IFC properties.
- [ ] Validation mechanism to check if the Rhino file has the correct layer structure and object types.
- [ ] GUI, perhaps through a new `COMPAS BIM` package.

## From Blender
...

## From Revit
...

## From ArchiCAD
...