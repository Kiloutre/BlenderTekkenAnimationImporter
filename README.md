# Tekken 7 animation to Blender importer/exporter plugin

This is an import/export plugin for Blender that makes it compatible with some Tekken 7 animations.
Both importing and exporting work decently well however rare are the animations that are compatible with this tool

It is made to work specifically with the following model: https://mega.nz/folder/05pBGLAL#XPHcsgK2tBxT3RLMbZPaFw
 
## Installation instructions
 
- Download the project as a .zip.
- Rename the .zip precisely as `BlenderTekkenAnimationImporter.zip` 
- **Manual**: Extract the archive so that it creates a folder here: `AppData\Roaming\Blender Foundation\Blender\2.92\scripts\addons`. Make sure the folder is correctly named **BlenderTekkenAnimationImporter**
- **Automatic**: Open Blender,go to **Edit -> Preferences**, in the newly opened window go to the **Add-ons** tab, click **Install** and select the .zip you downloaded earlier.
- If the addon is still not appearing, make sure it is enabled in **Edit -> Preferences -> Add-ons**

An export button should now be visible in **File -> Export -> Export Tekken7 Animation**

### Credits

- Tekken 7 mannequin model exported by Koenji.
- KulaGGin for developing the first prototype of Tekken->Blender animation conversion along with this plugin
- kilo for providing information about the animation format and completing KulaGGin's work
