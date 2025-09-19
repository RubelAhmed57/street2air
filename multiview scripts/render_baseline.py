import bpy
import mathutils
import os
import math

# Define the paths
blend_file_path = "path_to/van_1.blend"
output_dir = "path_to/van"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load the Blender file
bpy.ops.wm.open_mainfile(filepath=blend_file_path)

# Assuming 'car' is the name of the collection used as the camera
car_collection = bpy.data.collections.get('car')

if car_collection is None:
    raise ValueError("No collection named 'car' found in the scene. Please check the collection name.")

# Assuming the first object in the collection is the "camera"
object_as_camera = car_collection.objects[0]

# Get and print the world coordinates and rotation
world_location = object_as_camera.matrix_world.translation
world_rotation = object_as_camera.matrix_world.to_euler()

print("World Location:", world_location)
print("World Rotation (Euler):", world_rotation)

# Function to modify the view by rotating and translating the object
def modify_view(rotation=(0, 0, 0), translation=(0, 0, 0), index=0):
    # Rotate the object
    object_as_camera.rotation_euler = mathutils.Euler(rotation, 'XYZ')
    
    # Translate the object
    object_as_camera.location += mathutils.Vector(translation)
    
    # Update the scene
    bpy.context.view_layer.update()
    
    # Render the image
    bpy.context.scene.render.filepath = os.path.join(output_dir, f"rendered_view_{index:03d}.png")
    bpy.ops.render.render(write_still=True)

# Define different views
views = [
    {'rotation': (0, 0, 0), 'translation': (0, 0, 0)},             # Default view
    {'rotation': (0, 0, math.radians(15)), 'translation': (0, 0, 0)},  # Rotate 15 degrees around Z-axis
    {'rotation': (0, math.radians(10), 0), 'translation': (0, 0, 0)},  # Rotate 10 degrees around Y-axis
    {'rotation': (0, 0, 0), 'translation': (5, 0, 0)},             # Translate 5 units along X-axis
    {'rotation': (math.radians(-10), 0, 0), 'translation': (0, 0, 0)}, # Rotate -10 degrees around X-axis
]

# Apply each view and render
for i, view in enumerate(views):
    modify_view(rotation=view['rotation'], translation=view['translation'], index=i)

print("Rendering complete!")
