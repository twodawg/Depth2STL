import cv2
import numpy as np
from stl import mesh

def depth_to_mesh(image_path, output_stl, depth_scale=200, xy_scale=0.1):
    # Step 1: Load the depth map image
    full_image = cv2.imread(image_path)
    
    if full_image is None:
        print("Failed to load the depth map.")
        return
    
    # Step 2: Get the image dimensions
    height, width, channels = full_image.shape
    depth_map = full_image[:, width//2:]  # Get the right half
    #depth_map  = full_image

    # Convert to grayscale to treat as depth
    depth_map = cv2.cvtColor(depth_map, cv2.COLOR_BGR2GRAY)

    # Get the new dimensions of the depth map
    depth_height, depth_width = depth_map.shape

    # Step 3: Create arrays to hold the vertices and faces for the mesh
    vertices = []
    faces = []

    # Step 4: Generate vertices from the depth map with scaling
    for y in range(depth_height):
        for x in range(depth_width):  # Correct the range to depth_width
            z = (depth_map[y, x] / 255.0) * depth_scale  # Scale depth value
            scaled_x = x * xy_scale
            scaled_y  = y * xy_scale
            #vertices.append([x, y, -z])  # Store the vertex (x, y, z)
            vertices.append([scaled_x, -z, -scaled_y])

    # Step 5: Generate faces (triangles) for the mesh
    for y in range(depth_height - 1):
        for x in range(depth_width - 1):
            # Define two triangles for each square in the grid
            v1 = y * depth_width + x
            v2 = y * depth_width + (x + 1)
            v3 = (y + 1) * depth_width + x
            v4 = (y + 1) * depth_width + (x + 1)

            # First triangle (v1, v2, v3)
            faces.append([v1, v2, v3])
            # Second triangle (v2, v4, v3)
            faces.append([v2, v4, v3])


    # Convert lists to numpy arrays
    vertices = np.array(vertices)
    faces = np.array(faces)

    # Step 6: Create the mesh
    stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    
    for i, f in enumerate(faces):
        for j in range(3):
            stl_mesh.vectors[i][j] = vertices[f[j], :]

    # Step 7: Save the mesh to an STL file
    stl_mesh.save(output_stl)

    print(f"STL file saved as {output_stl}")

# Path to the depth map image and output STL file
image_path = '/Users/mike/Downloads/Putters - plasma_r.png'
output_stl = '/Users/mike/Downloads/Putters - plasma_r.stl'

depth_to_mesh(image_path, output_stl)