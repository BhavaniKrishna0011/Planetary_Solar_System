import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
import math

# Initialize the GLFW library
if not glfw.init():
    raise Exception("GLFW can't be initialized")

# Create a windowed mode window and its OpenGL context
window = glfw.create_window(800, 600, "Realistic Planetary Model of Solar System", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window can't be created")

# Make the window's context current
glfw.make_context_current(window)

# Load texture function
def load_texture(path):
    img = Image.open(path)
    img_data = np.array(list(img.getdata()), np.uint8)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    return texture_id

# Load textures
textures = {
    "mercury": load_texture("textures/mercury.jpeg"),
    "venus": load_texture("textures/venus.jpeg"),
    "earth": load_texture("textures/earth.jpeg"),
    "mars": load_texture("textures/mars.jpeg"),
    "jupiter": load_texture("textures/jupiter.jpeg"),
    "saturn": load_texture("textures/saturn.png"),
    "uranus": load_texture("textures/uranus.jpeg"),
    "neptune": load_texture("textures/neptune.jpeg"),
    "pluto": load_texture("textures/pluto.jpeg")
}

# Function to draw a textured sphere
def draw_textured_sphere(texture_id, radius, slices, stacks):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, radius, slices, stacks)
    gluDeleteQuadric(quadric)

# Calculate the position of the planet based on its elliptical orbit with inclination
def get_orbit_position(orbital_radius, angle, eccentricity, inclination):
    a = orbital_radius  # semi-major axis
    b = a * math.sqrt(1 - eccentricity ** 2)  # semi-minor axis
    x = a * math.cos(angle)
    z = b * math.sin(angle)
    y = z * math.tan(inclination)
    return x, y, z



# Planet data: (name, scale, semi-major axis, texture, orbital speed, eccentricity, inclination)
planets = [
    ("Mercury", 0.2, 2, textures["mercury"], 0.04, 0.205, math.radians(7)),
    ("Venus", 0.3, 3, textures["venus"], 0.03, 0.007, math.radians(3.4)),
    ("Earth", 0.4, 4, textures["earth"], 0.02, 0.017, math.radians(0)),
    ("Mars", 0.3, 5, textures["mars"], 0.01, 0.093, math.radians(1.85)),
    ("Jupiter", 0.7, 6.5, textures["jupiter"], 0.008, 0.048, math.radians(1.3)),
    ("Saturn", 0.6, 8, textures["saturn"], 0.007, 0.056, math.radians(2.49)),
    ("Uranus", 0.5, 9.5, textures["uranus"], 0.006, 0.046, math.radians(0.77)),
    ("Neptune", 0.5, 11, textures["neptune"], 0.005, 0.010, math.radians(1.77)),
    ("Pluto", 0.1, 13, textures["pluto"], 0.004, 0.248, math.radians(17.16))
]

# Initialize OpenGL settings
glEnable(GL_TEXTURE_2D)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])

# Function to generate random positions within a ring
def generate_ring_positions(inner_radius, outer_radius, num_objects, eccentricity, inclination):
    positions = []
    for _ in range(num_objects):
        angle = np.random.uniform(0, 2 * np.pi)
        radius = np.random.uniform(inner_radius, outer_radius)
        x, y, z = get_orbit_position(radius, angle, eccentricity, inclination)
        positions.append((x, y, z))
    return positions

# Generate positions for the Asteroid Belt
asteroid_positions = generate_ring_positions(5.5, 6, 200, 0.05, math.radians(10))

# Generate positions for the Kuiper Belt
kuiper_positions = generate_ring_positions(14, 20, 300, 0.1, math.radians(20))

# Main loop
angles = {planet[0]: 0 for planet in planets}
while not glfw.window_should_close(window):
    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Set up the camera
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 800 / 600, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 20, 40, 0, 0, 0, 0, 1, 0)
    
    # Draw the Sun as a solid-colored sphere
    glPushMatrix()
    glColor3f(1.0, 1.0, 0.0)  # Yellow color for the Sun
    quadric = gluNewQuadric()
    gluSphere(quadric, 1.0, 32, 32)
    gluDeleteQuadric(quadric)
    glPopMatrix()
    
    # Draw each planet
    for planet in planets:
        name, scale, semi_major_axis, texture, base_speed, eccentricity, inclination = planet
        angle = angles[name]
        x, y, z = get_orbit_position(semi_major_axis, angle, eccentricity, inclination)
        
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(scale, scale, scale)
        draw_textured_sphere(texture, 1.0, 32, 32)
        glPopMatrix()
        
        # Update the angle for the next frame
        speed = base_speed * (1 + eccentricity * math.cos(angle))  # Vary speed with eccentricity
        angles[name] += speed
        if angles[name] >= 2 * math.pi:
            angles[name] = 0
    
    # Swap front and back buffers
    glfw.swap_buffers(window)
    
    # Poll for and process events
    glfw.poll_events()

# Terminate GLFW
glfw.terminate()
