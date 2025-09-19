import bpy
import math
import os
import sys

# Function to convert feet to meters (assuming 1 Blender unit = 1 meter)
def feet_to_meters(feet):
    return feet * 0.3048

# Get command-line arguments
if len(sys.argv) < 3:
    raise ValueError("Please provide the Blender file path and rotation interval as arguments.")

# Blender command line arguments start after '--'
argv = sys.argv
if "--" in argv:
    argv = argv[argv.index("--") + 1:]

blend_file_path = argv[0]
rotation_interval = int(argv[1])  # Rotation interval in degrees

# Load the Blender file
bpy.ops.wm.open_mainfile(filepath=blend_file_path)

# Set the output directory based on the Blender file name
blend_file_name = os.path.splitext(os.path.basename(blend_file_path))[0]
output_dir = os.path.join(os.path.dirname(blend_file_path), f"{blend_file_name}_renders")
os.makedirs(output_dir, exist_ok=True)

# Get the object to rotate (assumes a collection named 'McLaren 570s')
tracked_object = bpy.data.objects.get('McLaren 570s')
if tracked_object is None:
    raise ValueError("No object named 'McLaren 570s' found in the scene.")

# Set render background to transparent
bpy.context.scene.render.film_transparent = True  # Enable transparency

# Define positions to move the car
positions = [
    (0, 0, 0),  # Add your desired coordinates here
    (-10, 0, 0),
    (5, 0, 0),
    (13, 0, 0),
    (0, -10, 0),
    (0, 8, 0)
]

# Iterate over the specified positions
for position_index, position in enumerate(positions):
    # Move the car to the new position
    tracked_object.location = position

    # Render the car at different rotations
    for angle in range(0, 360, rotation_interval):
        # Set the rotation (around Z-axis)
        tracked_object.rotation_euler[2] = math.radians(angle)

        # Update the scene
        bpy.context.view_layer.update()

        # Set render settings
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        render_filepath = os.path.join(output_dir, f"render_pos_{position_index}_angle_{angle:03d}_loc_{position[0]:.2f}_{position[1]:.2f}.png")
        bpy.context.scene.render.filepath = render_filepath

        # Render the image
        bpy.ops.render.render(write_still=True)

        # Check if the image was saved
        if os.path.exists(render_filepath):
            print(f"Saved image: {render_filepath}")
        else:
            print(f"Failed to save image: {render_filepath}")

print(f"Rendering complete! Images saved in: {output_dir}")
