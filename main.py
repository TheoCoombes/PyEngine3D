from PyEngine3D import Engine

# PyEngine3D Demo File ----------
# (C) Theo Coombes 2020


# Please note: this looks + runs way better running on your own pc.
# ^^^ EXPECT SOME LAG ON REPL.IT 

# CONTROLS ----
# WASD to move, mouse to look around
# Space + Shift to move up and down
# ESC to exit

# FILES ----
# Module files located in the "PyEngine3D" folder
# Level files located in the "levels" folder

initial_level = [
	{"type": "plane", "pos": [5, 15, 5], "size": [100, 100], "colour": "green"},
	{"type": "plane", "pos": [15, 15, 15], "axis": "yz", "size": [10, 10], "colour": "yellow"},
	{"type": "plane", "pos": [25, 15, 15], "axis": "yz", "size": [10, 10], "colour": "blue"}
]

game = Engine(initial_level = initial_level, sens=50, screen = [800, 600], fullscreen = True)

# USEFUL COMMANDS ----
game.sens = 10 # Changes mouse sensitivity
game.speed = 1 # Changes movement speed
game.player.position = [1, 0, 1] # Changes player position [X, Y, Z]

# COMING SOON ----

# plane = game.Instantiate(type="plane", pos=[X, Y, Z], length=[X, Y], axis="yx")
# ^ Instantiates/"spawns" a plane at X, Y, Z with a length of X, Y and on the axis yx
# ^ Returns a Plane object (see below)

# plane.position - returns the XYZ of the plane
# ^ plane.position = [X, Y, Z] - changes the position of the plane to [X, Y, Z]
# plane.length - returns the length [X, Y] of the plane
# ^ plane.length = [X, Y] - Resizes the plane spawned above to X, Y
# plane.Destroy() - Destroys/"deletes" the plane

# Basic Multiplayer (using flask)


# Possibly coming soon?
# Shadows
