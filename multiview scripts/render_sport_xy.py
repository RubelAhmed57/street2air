import bpy
import math
import random
import os
import shutil
import sys

# Get the Blender file path from the command line arguments
if len(sys.argv) < 2:
    raise ValueError("Please provide the Blender file path as an argument.")

# Blender command line arguments start after '--'
blend_file_path = sys.argv[sys.argv.index("--") + 1]
print(f"Original Blender file path: {blend_file_path}")

# Create a copy of the Blender file for rendering
blend_file_dir = os.path.dirname(blend_file_path)
blend_file_name = os.path.splitext(os.path.basename(blend_file_path))[0]  # Get the file name without extension
temp_blend_file_path = os.path.join(blend_file_dir, f"temp_{blend_file_name}.blend")
shutil.copy(blend_file_path, temp_blend_file_path)
print(f"Temporary Blender file created: {temp_blend_file_path}")

# Load the copied Blender file
bpy.ops.wm.open_mainfile(filepath=temp_blend_file_path)
print("Copied Blender file loaded successfully.")

# Number of images to render (excluding the default view)
num_renders = 30

# Directory to save the rendered images
output_dir = os.path.join(blend_file_dir, f"{blend_file_name}_renders")
os.makedirs(output_dir, exist_ok=True)
print(f"Render output directory: {output_dir}")

# Get the camera object from the scene collection
camera = bpy.data.objects.get('Camera')
if camera is None:
    raise ValueError("No camera named 'Camera' found in the scene.")

# Render the default view first
print("Rendering default view...")
default_view_filepath = os.path.join(output_dir, "default_view.png")
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = default_view_filepath
bpy.ops.render.render(write_still=True)
print(f"Default view saved as: {default_view_filepath}")

# Initial Y and Z coordinates (keep Z constant)
initial_y = camera.location.y
initial_z = camera.location.z

# Ensure there are at least 4 renders
assert num_renders >= 4, "Number of renders must be at least 4."

# Set predefined positions along the axes
axes_positions = [
    (0, initial_y),   # (0, y)
    (initial_y, 0),   # (y, 0)
    (0, -initial_y),  # (0, -y)
    (-initial_y, 0)   # (-y, 0)
]

# Determine how many random positions to generate
num_random_positions = num_renders - 4

# Generate random positions between the predefined axes positions
random_positions = []
for i in range(num_random_positions):
    # Determine the section of the circle (between two axis-aligned points)
    section = i % 4
    
    # Apply random Y variation
    y_variation = random.uniform(-1, 2)
    
    # Calculate position along the circle, not directly on the axes
    if section == 0:  # Between (0, y) and (y, 0)
        a = random.uniform(0, initial_y)
        pos = (a, initial_y - a + y_variation)
    elif section == 1:  # Between (y, 0) and (0, -y)
        a = random.uniform(0, initial_y)
        pos = (initial_y - a, -a + y_variation)
    elif section == 2:  # Between (0, -y) and (-y, 0)
        a = random.uniform(0, initial_y)
        pos = (-a, -initial_y + a + y_variation)
    else:  # Between (-y, 0) and (0, y)
        a = random.uniform(0, initial_y)
        pos = (-initial_y + a, a + y_variation)
    
    random_positions.append(pos)

# Combine predefined positions and random positions
all_positions = random_positions + axes_positions
random.shuffle(all_positions)  # Shuffle to mix predefined and random positions

# Render images at these positions
for i, (x, y) in enumerate(all_positions):
    # Apply additional random Y variation to avoid exact duplication of positions
    y += random.uniform(-1, 1)
    
    # Set the camera position
    camera.location.x = x
    camera.location.y = y
    camera.location.z = initial_z  + random.uniform(-0.5, 0.5) # Keep Z constant

    print(f"Camera position for render {i+1}: ({camera.location.x}, {camera.location.y}, {camera.location.z})")

    # Update the scene to apply the new camera position
    bpy.context.view_layer.update()

    # Set the render settings
    render_filepath = os.path.join(output_dir, f"render_view_{i:04d}.png")
    bpy.context.scene.render.filepath = render_filepath

    # Render the image
    bpy.ops.render.render(write_still=True)
    print(f"Rendered image {i+1} saved to {render_filepath}")

print("Rendering complete!")

# Clean up: Delete the temporary Blender file
os.remove(temp_blend_file_path)
print(f"Temporary Blender file deleted: {temp_blend_file_path}")
