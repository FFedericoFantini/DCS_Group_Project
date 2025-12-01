# save_scene.py
import os

def save_scene(sim, filename):
    # Path della cartella dove si trova lo script Python attuale
    current_folder = os.path.dirname(os.path.abspath(__file__))

    # Cartella superiore ("..")
    parent_folder = os.path.abspath(os.path.join(current_folder, ".."))

    # Percorso completo del file da salvare
    fullpath = os.path.join(parent_folder, filename)

    try:
        sim.saveScene(fullpath)
        print(f"✔ Scena salvata in:\n   {fullpath}\n")
    except Exception as e:
        print("❌ Errore nel salvataggio scena:", e)
