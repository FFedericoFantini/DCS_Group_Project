# save_scene.py
import os

def save_scene(sim, filename):
    # Path of the folder containing the current Python script
    current_folder = os.path.dirname(os.path.abspath(__file__))

    # Parent folder ("..")
    parent_folder = os.path.abspath(os.path.join(current_folder, ".."))

    # Full path of the file to be saved
    fullpath = os.path.join(parent_folder, filename)

    try:
        sim.saveScene(fullpath)
        print(f"📁 Scene saved to:   {filename}")
    except Exception as e:
        print("❌ Error while saving the scene:", e)
