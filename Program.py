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
window = glfw.create_window(1600, 1080, "Realistic Planetary Model of Solar System", None, None)
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
    "sun" : load_texture("textures/sun.jpeg"),
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
    ("Mercury", 0.2, 2, textures["mercury"], 0.06, 0.205, math.radians(7)),
    ("Venus", 0.3, 3, textures["venus"], 0.045, 0.007, math.radians(3.4)),
    ("Earth", 0.4, 4, textures["earth"], 0.03, 0.017, math.radians(0)),
    ("Mars", 0.3, 5, textures["mars"], 0.015, 0.093, math.radians(1.85)),
    ("Jupiter", 0.7, 6.5, textures["jupiter"], 0.012, 0.048, math.radians(1.3)),
    ("Saturn", 0.6, 8, textures["saturn"], 0.0105, 0.056, math.radians(2.49)),
    ("Uranus", 0.5, 9.5, textures["uranus"], 0.009, 0.046, math.radians(0.77)),
    ("Neptune", 0.5, 11, textures["neptune"], 0.0075, 0.010, math.radians(1.77)),
    ("Pluto", 0.1, 13, textures["pluto"], 0.006, 0.248, math.radians(17.16))
]

sun_texture = textures["sun"]

# Initialize OpenGL settings
glEnable(GL_TEXTURE_2D)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1])
glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])

# Generate positions for asteroids in a ring with a given range, eccentricity, and inclination
def generate_asteroid_positions(inner_radius, outer_radius, num_asteroids, eccentricity, inclination):
    asteroid_positions = []
    for _ in range(num_asteroids):
        orbital_radius = np.random.uniform(inner_radius, outer_radius)
        angle = np.random.uniform(0, 2 * math.pi)
        x, y, z = get_orbit_position(orbital_radius, angle, eccentricity, inclination)
        asteroid_positions.append((x, y, z))
    return asteroid_positions

# Asteroid belt properties
inner_radius = 7.0
outer_radius = 8.0
num_asteroids = 500
asteroid_eccentricity = 0.05
asteroid_inclination = math.radians(10)
asteroid_base_speed = 0.003  # Adjust speed as needed

asteroid_positions = generate_asteroid_positions(inner_radius, outer_radius, num_asteroids, asteroid_eccentricity, asteroid_inclination)
asteroid_angles = [np.random.uniform(0, 2 * math.pi) for _ in range(num_asteroids)]


# Main loop
angles = {planet[0]: 0 for planet in planets}
while not glfw.window_should_close(window):
    # Clear the screen
    glClearColor(0.0,0.0,0.0,1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Set up the camera
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1600 / 1200, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 10, 30, 0, 0, 0, 0, 1, 0)
    
    # Draw distant stars as points or textured spheres
    glColor3f(1.0, 1.0, 1.0)  # White color for stars
    glPointSize(2.0)  # Adjust point size as needed
    glBegin(GL_POINTS)
    for _ in range(1000):  # Draw 1000 stars
        x = np.random.uniform(-100, 100)
        y = np.random.uniform(-100, 100)
        z = np.random.uniform(-150, -50)  # Place stars far behind the planets
        glVertex3f(x, y, z)
    glEnd()
    
    # Draw the Sun and planets
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, sun_texture)
    glColor3f(1.0, 1.0, 1.0)  # White color for the Sun
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
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
    
    # Draw and update the asteroid belt (if desired)
    # Code for asteroid belt
    
    # Swap front and back buffers
    glfw.swap_buffers(window)
    
    # Poll for and process events
    glfw.poll_events()

# Terminate GLFW
glfw.terminate()
