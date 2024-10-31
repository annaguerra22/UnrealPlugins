import tkinter.filedialog # Let's us open file dialogs.
from unreal import ToolMenuContext, ToolMenus, ToolMenuEntryScript, uclass, ufunction # Brings in tools from Unreal Engine for menus and scripting.
import sys # Helps us interact with the Python runtime.
import os # Lets us interact with the operating system.
import importlib # Allows us to import modules.
import tkinter # Used for creating a graphical user interface.

srcDir = os.path.dirname(os.path.abspath(__file__)) # Finds the directory of the current script.
if srcDir not in sys.path: # Adds the script's directory to the system path if it's not already there.
     sys.path.append(srcDir)

import UnrealUtilities # Imports the UnrealUtilities module.
importlib.reload(UnrealUtilities) # Reloads the UnrealUtilities module to ensure it's up-to-date.
 
@uclass() # Tells Unreal Engine this is a special class.
class LoadFromDirEntryScript(ToolMenuEntryScript): # Creates a new script class to load files from a directory.
     @ufunction(override=True) # Marks this function to replace the default one.
     def execute(self, context): # This function runs when the script is triggered.
          window = tkinter.Tk() # Makes a hidden window.
          window.withdraw() # Hides the window.
          fileDir = tkinter.filedialog.askdirectory() # Asks the user to pick a folder.
          window.destroy() # Closes the hidden window.
          UnrealUtilities.UnrealUtility().LoadFromDir(fileDir) # Loads the files from the chosen folder.

@uclass() # Tells Unreal Engine this is a special class.
class BuildBaseMaterialEntryScript(ToolMenuEntryScript): # Creates a new script class to build a base material.
    @ufunction(override=True) # Marks this function to replace the default one.
    def execute(self, context: ToolMenuContext) -> None: # This function runs when the script is triggered.
        UnrealUtilities.UnrealUtility().FindOrCreateBaseMaterial() # Builds or finds the base material.
    

class UnrealSubstancePlugin: # Creates a new plugin class for Unreal.
    def __init__(self): # Initializes the plugin.
        self.subMenuName="SubstancePlugin" # Sets up names and calls InitUI to set up the menu.
        self.subMenuLabel="Substance Plugin"
        self.InitUI()

    def InitUI(self): # Sets up the user interface.
        mainMenu = ToolMenus.get().find_menu("LevelEditor.MainMenu")  # Finds the main menu in the Level Editor.
        self.subMenu = mainMenu.add_sub_menu(mainMenu.menu_name, "", "SubstancePlugin", "Substance Plugin") # Adds a submenu called "Substance Plugin".
        self.AddEntryScript("BuildBaseMaterial", "Build Base Material", BuildBaseMaterialEntryScript()) # Adds a menu option to build a base material.
        self.AddEntryScript("LoadFromDir", "Load from Directory", LoadFromDirEntryScript()) # Adds a menu option to load from a directory.
        ToolMenus.get().refresh_all_widgets() # Refreshes the menu to show the new options.

    def AddEntryScript(self, name, label, script: ToolMenuEntryScript): # Adds entry scripts to the submenu.
            script.init_entry(self.subMenu.menu_name, self.subMenu.menu_name, "", name, label) # Initializes the menu entry.
            script.register_menu_entry() # Registers the entry with the menu system.

UnrealSubstancePlugin() # Creates and runs the plugin.


