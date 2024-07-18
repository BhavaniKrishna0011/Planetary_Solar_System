from Planet3D import Planet, generate_solar_system

if __name__ == "__main__":
    sun = Planet(name="Sun", radius=5.0, orbit_radius=0.0, rotation_speed=0.0, color=(1.0, 0.8, 0.0))
    mercury = Planet(name="Mercury", radius=0.2, orbit_radius=5.0, rotation_speed=5.0, color=(0.7, 0.7, 0.7))
    venus = Planet(name="Venus", radius=0.5, orbit_radius=8.0, rotation_speed=3.0, color=(0.9, 0.7, 0.0))
    earth = Planet(name="Earth", radius=0.6, orbit_radius=12.0, rotation_speed=0.9, color=(0.0, 0.5, 1.0))
    mars = Planet(name="Mars", radius=0.4, orbit_radius=18.0, rotation_speed=0.8, color=(1.0, 0.0, 0.0))
    jupiter = Planet(name="Jupiter", radius=2.0, orbit_radius=50.0, rotation_speed=0.4, color=(0.8, 0.6, 0.4))
    saturn = Planet(name="Saturn", radius=1.8, orbit_radius=75.0, rotation_speed=0.3, color=(0.9, 0.6, 0.4))
    uranus = Planet(name="Uranus", radius=1.0, orbit_radius=110.0, rotation_speed=0.2, color=(0.5, 0.7, 0.8))
    neptune = Planet(name="Neptune", radius=1.0, orbit_radius=150.0, rotation_speed=0.15, color=(0.0, 0.0, 0.7))

    saturn_rings_color = (0.8, 0.8, 0.8)
    saturn.add_ring(radius=5.0, width=0.2, color=saturn_rings_color, transparency=0.3)

    earth.add_moon(name="Moon", radius=0.3, orbit_radius=3.0, rotation_speed=1.0, color=(0.8, 0.8, 0.8))

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    # To run in fullscreen mode, set fullscreen=True
    generate_solar_system(planets, display=(1200, 800), fullscreen=True)
