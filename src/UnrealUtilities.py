from unreal import (
    AssetToolsHelpers,
    AssetTools,
    EditorAssetLibrary,
    Material,
    MaterialFactoryNew,
    MaterialProperty,
    MaterialEditingLibrary,
    MaterialExpressionTextureSampleParameter2D as TexSampler2D,
    AssetImportTask,
    FbxImportUI
) # imports libraries and tools from Unreal Engine and Python. libraries help in create and manage assets in Unreal Engine.

import os

class UnrealUtility: #define a class called UnrealUtility. Like setting up variables for directories and names that we'll reference later
    def __init__(self): # Initializes the class.
        self.substanceRootDir = "/game/Substance/" # Sets the root directory for Substance files.
        self.baseMaterialName = "M_SubstanceBase" # Sets the name for the base material.
        self.substanceTempDir = "/game/Substace/Temp/" # Sets the temporary directory for Substance files.
        self.baseMaterialPath = self.substanceRootDir + self.baseMaterialName # Creates the full path to the base material.
        self.baseColorName = "BaseColor" # Sets the parameter name for the base color.
        self.normalName = "Normal" # Sets the parameter name for the normal map.
        self.occRoughnessMetalicName = "OcclusionRoughnessMetalic" # Sets the parameter name for occlusion, roughness, and metallic properties.

    def FindOrCreateBaseMaterial(self): #This method checks if the base material already exists. If it does, it loads it. If not, it creates a new material with different properties like base color, normal map, and occlusion-roughness-metallic properties, and then saves it.
        if EditorAssetLibrary.does_asset_exist(self.baseMaterialPath): # Checks if the base material already exists.
            return EditorAssetLibrary.load_asset(self.baseMaterialPath) # Loads and returns the existing base material.
        
        baseMat = AssetToolsHelpers.get_asset_tools().create_asset(self.baseMaterialName, # Creates a new material asset with the specified name and directory.
                                                                   self.substanceRootDir,
                                                                   Material, 
                                                                   MaterialFactoryNew())
        
        baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TexSampler2D, -800, 0) # Adds a base color texture expression to the material.
        baseColor.set_editor_property("parameter_name", self.baseColorName) # Sets the parameter name for the base color.
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR) # Connects the base color to the material's base color property.

        normal = MaterialEditingLibrary.create_material_expression(baseMat, TexSampler2D, -800, 400) # Adds a normal map texture expression to the material.
        normal.set_editor_property("parameter_name", self.normalName) # Sets the parameter name for the normal map.
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal")) # Loads and assigns a default normal texture to the normal map.
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL) # Connects the normal map to the material's normal property.

        occRoughnessMetalic = MaterialEditingLibrary.create_material_expression(baseMat, TexSampler2D, -800, 800) # Adds an occlusion-roughness-metallic texture expression to the material.
        occRoughnessMetalic.set_editor_property("parameter_name", self.occRoughnessMetalicName)  # Sets the parameter name for the occlusion-roughness-metallic map.
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION) # Connects the red channel to the ambient occlusion property.
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "G", MaterialProperty.MP_ROUGHNESS) # Connects the green channel to the roughness property.
        MaterialEditingLibrary.connect_material_property(occRoughnessMetalic, "B", MaterialProperty.MP_METALLIC) # Connects the blue channel to the metallic property.

        EditorAssetLibrary.save_asset(baseMat.get_path_name()) # Saves the new material.
        return baseMat # Returns the new material.
    
    def LoadMeshFromPath(self, meshPath): #This method imports an FBX mesh file into Unreal. It sets up import options and performs the import task. The mesh is saved to the specified location.
        meshName = os.path.split(meshPath)[-1].replace(".fbx","") # Takes the mesh name from the file path and removes the ".fbx" extension.
        importTask = AssetImportTask() # Creates a new asset import task.
        importTask.replace_existing = True # Configures the task to replace existing assets.
        importTask.filename = meshPath # Sets the file path for the mesh to import.
        importTask.destination_path = "/game/" + meshName # Sets the destination path for the imported mesh.
        importTask.save = True # Ensures the imported mesh is saved.
        importTask.automated = True # Sets the task to run automatically.

        fbxImportOptions = FbxImportUI() # Creates new FBX import options.
        fbxImportOptions.import_mesh = True # Configures the options to import the mesh.
        fbxImportOptions.import_as_skeletal = False # Ensures the mesh is imported as a static mesh, not skeletal.
        fbxImportOptions.import_materials + False # Specifies not to import materials.
        fbxImportOptions. static_mesh_import_data.combine_meshes = True # Combines all meshes into a single static mesh.
        
        importTask.options = fbxImportOptions # Assigns the import options to the task.

        AssetToolsHelpers().get_asset_tools().import_asset_tasks([importTask]) # Executes the import task.
        return importTask.get_objects()[0]     # Returns the imported mesh.

    
    def LoadFromDir(self, fileDir): #This method loops through all files in the given directory, and if it finds an .fbx file, it calls LoadMeshFromPath to import it into Unreal
        for file in os.listdir(fileDir): # Loops through each file in the specified directory.
            if ".fbx" in file: # Checks if the file is an .fbx file.
                self.LoadMeshFromPath(os.path.join(fileDir, file)) # Calls LoadMeshFromPath to import the .fbx file.

