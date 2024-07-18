import turtle

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Solar System Visualization")
screen.setup(width=1300, height=700)

def draw_planet(name, color, radius, orbit_radius, speed):
    turtle.penup()
    turtle.color(color)
    turtle.goto(orbit_radius, -radius - 10)
    turtle.pendown()
    turtle.begin_fill()
    turtle.circle(radius)
    turtle.end_fill()
    turtle.penup()
    turtle.goto(orbit_radius, -radius - 30)
    turtle.pendown()
    turtle.write(name, align="center", font=("Arial", 10, "normal"))
    turtle.penup()
    turtle.goto(0, -orbit_radius)
    turtle.pendown()
    turtle.circle(orbit_radius, 360)
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(orbit_radius, 0)
    turtle.pendown()
    
draw_planet("Sun", "yellow", 30, 0, 0)
planets_data = [
    ("Mercury", "gray", 5, 60, 10),
    ("Venus", "orange", 10, 80, 8),
    ("Earth", "blue", 10, 120, 5),
    ("Mars", "red", 8, 150, 3),
    ("Jupiter", "tan", 30, 190, 1),
    ("Saturn", "gold", 25, 250, 0.5),
    ("Uranus", "lightblue", 20, 310, 0.3),
    ("Neptune", "darkblue", 18, 380, 0.2)
]
for planet_data in planets_data:
    draw_planet(*planet_data)
    
screen.exitonclick()