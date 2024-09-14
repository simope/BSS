import numpy as np
import matplotlib.pyplot as plt


# Earth coordinates (sphere)
R_earth = 1
phi, theta = np.mgrid[0:2*np.pi:100j, 0:np.pi:50j]
x_sphere = R_earth * np.sin(theta) * np.cos(phi)
y_sphere = R_earth * np.sin(theta) * np.sin(phi)
z_sphere = R_earth * np.cos(theta)

# Earth's axis, pointing NCP
tilt = np.radians(23.5) # Its inclination
x_arrow, y_arrow, z_arrow = (0, -np.sin(tilt), -np.cos(tilt)) # Origin
u_arrow, v_arrow, w_arrow = (0, np.sin(tilt), np.cos(tilt)) # Direction

# Angle and radius for plotting circles
theta = np.linspace(0, 2*np.pi, 100)
R_circle = 5

# Celestial equator (tilted 23.5 degrees wrt ecliptic plane)
x_eq = R_circle * np.cos(theta)
y_eq = R_circle * np.sin(theta)
z_eq = R_circle * np.sin(-tilt) * np.sin(theta)

# Ecliptic (on the xy plane)
x_ecl = R_circle * np.cos(theta)
y_ecl = R_circle * np.sin(theta)
z_ecl = np.zeros_like(theta)

# Create plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
# The following are important to maintain the axes ratio
# You don't want a squeezed Earth!
ax.axes.set_xlim3d(left=-R_circle, right=R_circle) 
ax.axes.set_ylim3d(bottom=-R_circle, top=R_circle) 
ax.axes.set_zlim3d(bottom=-R_circle, top=R_circle) 

# Earth
ax.plot_surface(x_sphere, y_sphere, z_sphere, color='b', alpha=0.3, rstride=5, cstride=5)

# Earth's axis
ax.quiver(x_arrow, y_arrow, z_arrow, u_arrow, v_arrow, w_arrow, color='k', linestyle='--', length=2.5, arrow_length_ratio=0.1, label='Earth\'s axis')

# Celestial equator
ax.plot(x_eq, y_eq, z_eq, color='g', label='Celestial Equator')

# Ecliptic
ax.plot(x_ecl, y_ecl, z_ecl, color='b', label='Ecliptic')

## Important points
# Vernal Equinox
ax.scatter(R_circle, 0, 0, color='yellow', s=100, label='Vernal Equinox')

# Autumnal Equinox
ax.scatter(-R_circle, 0, 0, color='orange', s=100, label='Autumnal Equinox')

# Summer Solstice
ax.scatter(0, R_circle, 0, color='pink', s=100, label='Summer Solstice')

# Winter Solstice
ax.scatter(0, -R_circle, 0, color='purple', s=100, label='Winter Solstice')

##  Define GCRS coordinate system axes
# Define x-axis, which is aligned with
# VernalEquinox point
x_axis_x, x_axis_y, x_axis_z = (0, 0, 0)
x_axis_u, x_axis_v, x_axis_w = (1, 0, 0)

# Define z-axis, which is aligned with
# Earth's axis
z_axis_x, z_axis_y, z_axis_z = (0, 0, 0)
z_axis_u, z_axis_v, z_axis_w = (0, np.sin(tilt), np.cos(tilt))

# Define y-axis, which complete the 
# right-hand triad (correct name in English?)
y_axis_x, y_axis_y, y_axis_z = (0, 0, 0)
y_axis_u, y_axis_v, y_axis_w = -np.cross([x_axis_u, x_axis_v, x_axis_w], [z_axis_u, z_axis_v, z_axis_w])

# Plot GCRS axes
ax.quiver(x_axis_x, x_axis_y, x_axis_z, x_axis_u, x_axis_v, x_axis_w, color='cyan', length = 2.5, arrow_length_ratio=0.1, label='GCRS x-axis')
ax.quiver(y_axis_x, y_axis_y, y_axis_z, y_axis_u, y_axis_v, y_axis_w, color='magenta', length = 2.5, arrow_length_ratio=0.1, label='GCRS y-axis')
ax.quiver(z_axis_x, z_axis_y, z_axis_z, z_axis_u, z_axis_v, z_axis_w, color='purple', length = 2.5, arrow_length_ratio=0.1, label='GCRS z-axis')

# Labels and legend
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Earth, Ecliptic, CE and GCRS system')
ax.legend()
plt.show()
