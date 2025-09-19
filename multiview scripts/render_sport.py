import bpy
import math
import os
import sys
import random

# Convert feet to meters (assuming 1 Blender unit = 1 meter)
def feet_to_meters(feet):
    return feet * 0.3048

# Get the Blender file path from the command line arguments
if len(sys.argv) < 2:
    raise ValueError("Please provide the Blender file path as an argument.")

# Blender command line arguments start after '--'
blend_file_path = sys.argv[sys.argv.index("--") + 1]

# Load the Blender file
bpy.ops.wm.open_mainfile(filepath=blend_file_path)

# Set the output directory based on the Blender file name
blend_file_name = os.path.splitext(os.path.basename(blend_file_path))[0]
output_dir = os.path.join(os.path.dirname(blend_file_path), f"{blend_file_name}_renders")
os.makedirs(output_dir, exist_ok=True)
# Set the render background to transparent
bpy.context.scene.render.film_transparent = True  # Enable transparency

# Get the camera
camera = bpy.data.objects.get('Camera')
if camera is None:
    raise ValueError("No camera named 'Camera' found in the scene.")

# Check if the camera has a tracking constraint
if camera.constraints:
    tracked_object = camera.constraints[0].target
else:
    # If no constraint is found, manually specify the object to be tracked
    tracked_object = bpy.data.objects.get('McLaren 570s')  # Replace 'YourObjectName' with your object’s name
    if tracked_object is None:
        raise ValueError("No object specified for tracking. Please set 'YourObjectName' to the correct object name.")
    # Optionally, add a Track To constraint to the camera
    track_to = camera.constraints.new(type='TRACK_TO')
    track_to.target = tracked_object
    track_to.track_axis = 'TRACK_NEGATIVE_Z'
    track_to.up_axis = 'UP_Y'

# Center of the object
object_center = tracked_object.location

# Calculate the original distance between the camera and the tracked object
original_distance = (camera.location - object_center).length

# Set radius based on the original distance, ensuring it's within 20-30 feet (6.1-9.1 meters)
min_radius = feet_to_meters(20)
max_radius = feet_to_meters(30)
radius = min(max(original_distance, min_radius), max_radius)

# Parameters for randomness (converted to meters)
num_views = 30  # Number of images to render (e.g., 12 images for a full circle)
height_variation = feet_to_meters(3.0)  # Maximum variation in height (Z-axis)
horizontal_variation = feet_to_meters(2.0)  # Maximum variation in horizontal plane (X and Y)

# Render images from different camera positions
for i in range(num_views):
    # Calculate the base angle in radians
    angle = (i / num_views) * 2 * math.pi
    
    # Introduce randomness to the camera position
    random_angle_offset = random.uniform(-0.1, 0.1) * math.pi  # Small random angular offset
    random_radius_offset = random.uniform(-horizontal_variation, horizontal_variation)  # Small random radius offset
    random_height_offset = random.uniform(-height_variation, height_variation)  # Small random height offset
    
    # Calculate the new camera position with randomness
    x = object_center.x + (radius + random_radius_offset) * math.cos(angle + random_angle_offset)
    y = object_center.y + (radius + random_radius_offset) * math.sin(angle + random_angle_offset)
    z = camera.location.z + random_height_offset  # Add random height variation
    
    # Move the camera to the new position
    camera.location = (x, y, z)
    
    # Update the scene
    bpy.context.view_layer.update()

    # Set render settings
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    render_filepath = os.path.join(output_dir, f"render_view_{i:04d}.png")
    bpy.context.scene.render.filepath = render_filepath

    # Render the image
    bpy.ops.render.render(write_still=True)

    # Check if the image was saved
    if os.path.exists(render_filepath):
        print(f"Saved image: {render_filepath}")
    else:
        print(f"Failed to save image: {render_filepath}")

print(f"Rendering complete! Images saved in: {output_dir}")
