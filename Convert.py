import numpy as np
from stl import mesh
from scipy.spatial import Delaunay

# Load the normals and depth data from the .npy files
#normals_data = np.load('C:/Users/mtwohey/Downloads/Mike Run Normals.npy')
depth_data = np.load('C:/Users/mtwohey/Downloads/Mike Run Depth.npy')

depth_data *= 100  # Adjust this factor based on the actual depth scale you want (e.g., 100 units max depth)

# Create a mesh grid for the image coordinates
height, width = depth_data.shape
x, y = np.meshgrid(np.arange(width), np.arange(height))

# Flatten the depth and normals arrays
x_flat = x.flatten() * 0.1
y_flat = y.flatten() * 0.1
z_flat = depth_data.flatten()

# Flip or adjust the z-axis if necessary (to ensure proper orientation)
#z_flat = np.max(z_flat) - z_flat  # Invert the depth values if they are upside down

# Construct 3D points from x, y, and depth (z) values
#points_3d = np.vstack((x_flat, y_flat, z_flat)).T

# Transform the coordinate system
# x stays the same, y becomes -z (to flip it), z becomes y (so Z is forward and Y is up)
points_3d = np.vstack((x_flat, z_flat, -y_flat)).T  # Z is now the depth, and -Y becomes the upward axis

# Apply translation: move by -70 in X and +70 in Z
points_3d[:, 0] -= 70  # Translate -70 units in X
points_3d[:, 2] += 70  # Translate +70 units in Z

# Generate the Delaunay triangulation for the mesh (2D triangulation of the x, y plane)
tri = Delaunay(np.vstack((x_flat, y_flat)).T)

# Define vertices and faces for the mesh
vertices = points_3d
faces = tri.simplices

# Create the mesh
mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, face in enumerate(faces):
    for j in range(3):
        mesh_data.vectors[i][j] = vertices[face[j], :]

# Save the mesh to an STL file
mesh_data.save('3d_reconstructed_mesh.stl')

print('STL file created successfully!')
