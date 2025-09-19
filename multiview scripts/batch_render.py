import os
import subprocess
import logging
import sys

# Setup logging to capture errors
logging.basicConfig(filename='render_errors.log', level=logging.ERROR)

# Define the list of vehicle types and their corresponding render scripts
vehicle_scripts = {
    'bus': 'render_bus_xy.py',
    'sedan': 'render_sedan_xy.py',
    'sport': 'render_sport_xy.py',
    'suv': 'render_suv_xy.py',
    'truck': 'render_truck_xy.py',
    'van': 'render_van_xy.py'
}

# Blender executable command
blender_executable = "blender"  # Adjust this if your Blender executable has a different name or path

# Function to clear Blender's cache/memory after each render
def clear_blender_cache():
    # Clear Blender cache/memory (if necessary)
    clear_script = """
import bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.outliner.orphans_purge()
    """
    subprocess.run([blender_executable, '--background', '--python-expr', clear_script], check=True)
    print("Cache and memory cleared.")

# Loop through each vehicle type and corresponding script
for vehicle, render_script in vehicle_scripts.items():
    vehicle_dir = os.path.join(vehicle)
    if os.path.isdir(vehicle_dir):
        # Find all .blend files with _xy in the name
        for file_name in os.listdir(vehicle_dir):
            if file_name.endswith("_xy.blend"):
                blend_file_path = os.path.join(vehicle_dir, file_name)
                try:
                    # Construct the command to run Blender with the specified Python script and Blender file
                    command = [
                        blender_executable,
                        "--background",
                        "--python", render_script,
                        "--", blend_file_path
                    ]
                    print(f"Rendering {blend_file_path} with {render_script}...")
                    
                    # Run the Blender rendering process
                    subprocess.run(command, check=True)
                    
                    # Clear Blender cache/memory after each render
                    clear_blender_cache()

                except subprocess.CalledProcessError as e:
                    # Log any errors that occur
                    logging.error(f"Error rendering {blend_file_path} with {render_script}: {e}")
                    print(f"Error rendering {blend_file_path} with {render_script}, logged to render_errors.log")
    else:
        print(f"Directory {vehicle_dir} does not exist.")

print("Rendering process completed.")