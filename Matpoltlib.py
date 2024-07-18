# simple_solar_system.py

from solar_system_3d import SolarSystem, Sun, Planet

# Constants for planets
planets_data = [
    {"name": "Mercury", "mass": 3.3011e23, "position": (57.9e9, 0, 0), "velocity": (0, 47.87e3, 0)},
    {"name": "Venus", "mass": 4.8675e24, "position": (108.2e9, 0, 0), "velocity": (0, 35.02e3, 0)},
    {"name": "Earth", "mass": 5.972e24, "position": (149.6e9, 0, 0), "velocity": (0, 29.78e3, 0)},
    {"name": "Mars", "mass": 6.4171e23, "position": (227.9e9, 0, 0), "velocity": (0, 24.07e3, 0)},
    {"name": "Jupiter", "mass": 1.8982e27, "position": (778.5e9, 0, 0), "velocity": (0, 13.07e3, 0)},
    {"name": "Saturn", "mass": 5.6834e26, "position": (1.434e12, 0, 0), "velocity": (0, 9.69e3, 0)},
    {"name": "Uranus", "mass": 8.6810e25, "position": (2.871e12, 0, 0), "velocity": (0, 6.81e3, 0)},
    {"name": "Neptune", "mass": 1.0241e26, "position": (4.495e12, 0, 0), "velocity": (0, 5.43e3, 0)},
    {"name": "Pluto", "mass": 1.303e22, "position": (5.906e12, 0, 0), "velocity": (0, 4.74e3, 0)}
]

# Normalize the size for visualization
scale_factor = 1e9

solar_system = SolarSystem(1e13 / scale_factor, projection_2d=True)

sun = Sun(solar_system)

planets = [
    Planet(
        solar_system,
        mass=planet["mass"],
        position=(planet["position"][0] / scale_factor, planet["position"][1] / scale_factor, planet["position"][2] / scale_factor),
        velocity=(planet["velocity"][0] / scale_factor, planet["velocity"][1] / scale_factor, planet["velocity"][2] / scale_factor)
    )
    for planet in planets_data
]

while True:
    solar_system.calculate_all_body_interactions()
    solar_system.update_all()
    solar_system.draw_all()
