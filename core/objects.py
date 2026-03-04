"""
Gravitaional time dilation multipliers for various celestial objects.
Multiplier = sqrt(1 - 2GM/(rc^2)) approximatley.
All values are 0 < multipliers <= 1.
"""

GRAVITATIONAL_OBJECTS = {
    "earth": {
        "name": "Earth",
        "multiplier": 0.9999999993,
        "discription": "Surface gravity",
    },
    "sun": {
        "name": "Sun",
        "multiplier": 0.9999989,
        "discription": "Surface gravity",
    },
    "white-dwarf": {
        "name": "White Dwarf",
        "multiplier": 0.9997,
        "discription": "Typical white dwarf surface gravity",
    },
    "neutron_star": {
        "name": "Neutron Star",
        "multiplier": 0.77,
        "discription": "Typical neutron star surface gravity",
    },
    "black_hole": {
        "name": "Black Hole (near horizon)",
        "multiplier": 0.1,
        "discription": "Just outside the event horizon",
    },
}

# List of keys for iteration
OBJECTS_KEYS = list(GRAVITATIONAL_OBJECTS.keys())
