import bpy
import math
import os
import sys
import random

# Convert feet to meters (assuming 1 Blender unit = 1 meter)
def feet_to_meters(feet):
    return feet * 0.3048

# Convert meters to feet (assuming 1 Blender unit = 1 meter)
def meters_to_feet(meters):
    return meters / 0.3048

print("Starting script...")

# Get the Blender file path from the command line arguments
if len(sys.argv) < 2:
    raise ValueError("Please provide the Blender file path as an argument.")

# Blender command line arguments start after '--'
blend_file_path = sys.argv[sys.argv.index("--") + 1]
print(f"Blender file path: {blend_file_path}")

# Load the Blender file
bpy.ops.wm.open_mainfile(filepath=blend_file_path)
print("Blender file loaded successfully.")

# Set the output directory based on the Blender file name
blend_file_name = os.path.splitext(os.path.basename(blend_file_path))[0]
output_dir = os.path.join(os.path.dirname(blend_file_path), f"{blend_file_name}_renders")
os.makedirs(output_dir, exist_ok=True)
print(f"Output directory set to: {output_dir}")

# Set the render background to transparent
bpy.context.scene.render.film_transparent = True  # Enable transparency

# Determine if unit conversion is necessary
scene = bpy.context.scene
unit_system = scene.unit_settings.system
print(f"Unit system in Blender file: {unit_system}")

if unit_system == 'IMPERIAL':
    print("Units are set to feet, no conversion necessary.")
    def to_scene_units(value): return value  # No conversion needed
else:
    print("Units are set to meters, converting to feet.")
    def to_scene_units(value): return meters_to_feet(value)  # Convert to feet

# Get the camera
camera = bpy.data.objects.get('Camera')
if camera is None:
    raise ValueError("No camera named 'Camera' found in the scene.")
print(f"Camera found: {camera.name}")

# Check if the camera has a tracking constraint
if camera.constraints:
    tracked_object = camera.constraints[0].target
    print(f"Camera tracking an object: {tracked_object.name}")
else:
    # If no constraint is found, manually specify the object to be tracked
    tracked_object = bpy.data.objects.get('YourObjectName')  # Replace 'YourObjectName' with your object’s name
    if tracked_object is None:
        raise ValueError("No object specified for tracking. Please set 'YourObjectName' to the correct object name.")
    # Optionally, add a Track To constraint to the camera
    track_to = camera.constraints.new(type='TRACK_TO')
    track_to.target = tracked_object
    track_to.track_axis = 'TRACK_NEGATIVE_Z'
    track_to.up_axis = 'UP_Y'
    print(f"Tracking constraint added to object: {tracked_object.name}")

# Center of the object
object_center = tracked_object.location
print(f"Object center located at: {object_center}")

# Calculate the original distance between the camera and the tracked object
original_distance = (camera.location - object_center).length
print(f"Original distance from camera to object: {original_distance} units")

# Set radius based on the original distance, ensuring it's within 20-30 feet (6.1-9.1 meters)
min_radius = to_scene_units(10)
max_radius = to_scene_units(15)
radius = min(max(original_distance, min_radius), max_radius)
print(f"Orbit radius set to: {radius} units")

# Parameters for randomness (converted to feet)
num_views = 30  # Number of images to render
height_variation = to_scene_units(2.0)  # Maximum variation in height (Z-axis)
horizontal_variation = to_scene_units(1.0)  # Maximum variation in horizontal plane (X and Y)
print(f"Number of views: {num_views}, Height variation: {height_variation} feet, Horizontal variation: {horizontal_variation} feet")

# Render the default view first
print("Rendering default view...")
default_view_filepath = os.path.join(output_dir, f"{blend_file_name}_default.png")
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = default_view_filepath
bpy.ops.render.render(write_still=True)
print(f"Default view saved as: {default_view_filepath}")

# Render images from different camera positions
for i in range(num_views):
    print(f"Rendering view {i+1}/{num_views}...")
    
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
    print(f"Camera moved to: ({x}, {y}, {z})")
    
    # Update the scene
    bpy.context.view_layer.update()
    print("Scene updated.")

    # Set render settings
    render_filepath = os.path.join(output_dir, f"{blend_file_name}_view_{i:03d}.png")
    bpy.context.scene.render.filepath = render_filepath
    print(f"Render file path set to: {render_filepath}")

    # Render the image
    bpy.ops.render.render(write_still=True)
    print(f"Render {i+1} command executed.")

    # Check if the image was saved
    if os.path.exists(render_filepath):
        print(f"Saved image: {render_filepath}")
    else:
        print(f"Failed to save image: {render_filepath}")

print(f"Rendering complete! Images saved in: {output_dir}")
