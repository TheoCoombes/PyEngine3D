import os
os.system("pip install pynput")
# ^ Repl.it only

import tkinter as tk
import statistics
from math import sqrt
from json import load
from pynput.keyboard import Listener, Key
from time import time


#   ___      ___           _          _______  
#  | _ \_  _| __|_ _  __ _(_)_ _  ___|__ /   \ 
#  |  _/ || | _|| ' \/ _` | | ' \/ -_)|_ \ |) |
#  |_|  \_, |___|_||_\__, |_|_||_\___|___/___/ 
#       |__/         |___/                     
#
# 			(C) Theo Coombes 2020


def warn(error):
	print("\033[93m" + "[PyEngine3D] (Warning) " + error + "\033[0m")

class Engine:
	def __init__(self,
                     initial_level=[],
                     screen=[1920, 1080], # The resolution
                     fullscreen=True, # Sets the engine to fullscreen
                     sens=10,
                     fov=2500,
                     speed=0.25,
                     start_pos=[0, 0, 0]):
		print("Hello, World.")
		self.sens = sens
		self.abort = False # Stops loop
		self.speed = speed
		self.screen = screen # Screen size
		self.fov = screen[0] * 2
		self.player = Player() # Player detais
		self.root = tk.Tk() # Init tkinter
		self.canvas = tk.Canvas(self.root,
                        width=self.screen[0], height=self.screen[1],
                        bg = "#99e6ff"
		)
		self.canvas.pack()
		if fullscreen:
			self.root.attributes("-fullscreen", True)
		
		# Bindings
		self.root.bind('<Motion>', self.onMouse)
		self.root.bind('<Escape>', self.exitGame)

		# Good movement this time
		self.wasd = [False, False, False, False, False, False]

		self.scene = []

		if type(initial_level) != list:
			initial_level = load(initial_level)

		self.loadLevel(initial_level)
		self.mainLoop()

	
	def onPress(self, key):
		try:
			if key.char == 'w':
				self.wasd[0] = True
			elif key.char == 'a':
				self.wasd[1] = True
			elif key.char == 's':
				self.wasd[2] = True
			elif key.char == 'd':
				self.wasd[3] = True
		except:
			if key == Key.space:
				self.wasd[4] = True
			elif key == Key.shift:
				self.wasd[5] = True
	
	def onRelease(self, key):
		try:
			if key.char == 'w':
				self.wasd[0] = False
			elif key.char == 'a':
				self.wasd[1] = False
			elif key.char == 's':
				self.wasd[2] = False
			elif key.char == 'd':
				self.wasd[3] = False
		except:
			if key == Key.space:
				self.wasd[4] = False
			elif key == Key.shift:
				self.wasd[5] = False


	def exitGame(self, content):
		print("Goodbye, World.")
		self.root.destroy()
		self.abort = True
		#exit()
	
	def Distance(self, pos1, pos2):
		""" Calculates the distance between 2 3D points """
		# https://www.math.usm.edu/lambers/mat169/fall09/lecture17.pdf
		return sqrt(((pos1[0] - pos2[0]) ** 2) + ((pos1[2] - pos2[2]) ** 2))
		#return sqrt(((pos1[0] - pos2[0]) ** 2) + ((pos1[1] - pos2[1]) ** 2) + ((pos1[2] - pos2[2]) ** 2))

	def loadLevel(self, level):
		for object in level:
			if object["type"].lower() == "plane":
				obj = Plane(
					pos=object.get("pos", [0, 0, 0]),
					size=object.get("size", [10, 10]),
					axis=object.get("axis", "x"),
					colour=object.get("colour", "white"),
					outline=object.get("outline", "black")
				)
				self.scene.append(obj)


	def toXY(self, pos):
		""" Converts XYZ to XY for 2D drawings """
		if not pos[2] + self.player.pos[2] <= 1:
			nx = self.fov * ((pos[0] + self.player.pos[0]) / (pos[2] + self.player.pos[2])) + ((self.player.rotation[0] * -1) * self.sens)
			ny = self.fov * ((pos[1] + self.player.pos[1]) / (pos[2] + self.player.pos[2])) + ((self.player.rotation[1] * -1) * self.sens)
		else:
			nx = self.fov * ((pos[0] + self.player.pos[0]) / 2) + ((self.player.rotation[0] * -1) * self.sens)
			ny = self.fov * ((pos[1] + self.player.pos[1]) / 2) + ((self.player.rotation[1] * -1) * self.sens)
		return [nx, ny]

	def renderPlane(self, pos, size=[10, 10], axis="x"):
		""" Renders a Plane into drawable, 2D lines """
		lines = []
		if axis == "x":
			lines += self.toXY(pos)
			lines += self.toXY([pos[0] + size[0], pos[1], pos[2]])
			lines += self.toXY([pos[0] + size[0], pos[1], pos[2] + size[1]])
			lines += self.toXY([pos[0], pos[1], pos[2] + size[1]])
		elif axis == "z":
			lines += self.toXY(pos)
			lines += self.toXY([pos[0] + size[1], pos[1], pos[2]])
			lines += self.toXY([pos[0] + size[1], pos[1], pos[2] + size[0]])
			lines += self.toXY([pos[0], pos[1], pos[2] + size[0]])
		elif axis == "yz":
			lines += self.toXY(pos)
			lines += self.toXY([pos[0], pos[1] + size[0], pos[2]])
			lines += self.toXY([pos[0], pos[1] + size[0], pos[2] + size[1]])
			lines += self.toXY([pos[0], pos[1], pos[2] + size[1]])
		elif axis == "yx":
			lines += self.toXY(pos)
			lines += self.toXY([pos[0], pos[1] + size[0], pos[2]])
			lines += self.toXY([pos[0] + size[1], pos[1] + size[0], pos[2]])
			lines += self.toXY([pos[0] + size[1], pos[1], pos[2]])
		return lines

	def renderCube(self, pos, size=5):
		""" Renders a Cube into drawable, 2D lines """
		# --- Obsolete, use planes instead -----
		lines = []
		# X, Y
		lines.append([
			self.toXY(pos),
			self.toXY([pos[0] + size, pos[1], pos[2]])
		])
		lines.append([
			self.toXY([pos[0] + size, pos[1], pos[2]]),
			self.toXY([pos[0] + size, pos[1] - size, pos[2]])
		])
		lines.append([
			self.toXY([pos[0] + size, pos[1] - size, pos[2]]),
			self.toXY([pos[0], pos[1] - size, pos[2]])
		])
		lines.append([
			self.toXY([pos[0], pos[1] - size, pos[2]]),
			self.toXY(pos)
		])
		# X, Z
		lines.append([
			self.toXY(pos),
			self.toXY([pos[0], pos[1], pos[2] - (size/2)])
		])
		lines.append([
			self.toXY([pos[0], pos[1], pos[2] - (size/2)]),
			self.toXY([pos[0] + size, pos[1], pos[2] - (size/2)])
		])
		lines.append([
			self.toXY([pos[0] + size, pos[1], pos[2] - (size/2)]),
			self.toXY([pos[0] + size, pos[1], pos[2]])
		])
		lines.append([
			self.toXY([pos[0] + size, pos[1], pos[2]]),
			self.toXY([pos[0] + size, pos[1], pos[2] - (size/2)])
		])
		# X, Y, Z
		lines.append([
			self.toXY([pos[0] + size, pos[1], pos[2] - (size/2)]),
			self.toXY([pos[0] + size, pos[1] - size, pos[2] - (size/2)])
		])
		lines.append([
			self.toXY([pos[0] + size, pos[1] - size, pos[2]]),
			self.toXY([pos[0] + size, pos[1] - size, pos[2] - (size/2)])
		])
		lines.append([
			self.toXY([pos[0] + size, pos[1] - size, pos[2] - (size/2)]),
			self.toXY([pos[0], pos[1] - size, pos[2] - (size/2)])
		])
		lines.append([
			self.toXY([pos[0], pos[1] - size, pos[2] - (size/2)]),
			self.toXY([pos[0], pos[1] - size, pos[2]])
		])
		lines.append([
			self.toXY([pos[0], pos[1] - size, pos[2]]),
			self.toXY([pos[0], pos[1] - size, pos[2] - (size/2)])
		])
		lines.append([
			self.toXY([pos[0], pos[1] - size, pos[2] - (size/2)]),
			self.toXY([pos[0], pos[1], pos[2] - (size/2)])
		])
		return lines

	def Destroy(self, object):
		try:
			self.scene.remove(object)
			return True
		except:
			# Return if object is already non-existant
			warn("Attempted to Destroy an unexistant object.")
			return False



	def renderScene(self):
		self.canvas.delete("all")

		renderData = []

		# 1.) Rendering scene data, finding furthest point from player, compiling data
		for object in self.scene:
			if object.type == "plane":
				pos = object.pos
				size = object.size
				render = self.renderPlane(pos=pos, size=size, axis=object.axis)

				# Bulky code; probably should be moved somewhere
				furthest = []
				furthest.append(self.Distance(self.player.pos, pos))
				furthest.append(self.Distance(self.player.pos, [pos[0] + size[0], pos[1], pos[2]]))
				furthest.append(self.Distance(self.player.pos, [pos[0] + size[0], pos[1], pos[2] + size[1]]))
				furthest.append(self.Distance(self.player.pos, [pos[0], pos[1], pos[2] + size[1]]))

				furthest = min(furthest) # Get furthest distance away from player

				renderData.append([furthest, render, [object.colour, object.outline]])
		
		# 2.) Sorting render order
		renderData.sort(
			key = lambda x: x[0],
			reverse = True

		)
		print(renderData)

		# 3.) Rendering data

		for render in renderData:
			self.canvas.create_polygon(render[1], fill=render[2][0], outline=render[2][1])


		self.canvas.create_text(20, 30, anchor="nw", font=("Purisa", 12),
			text=f"PyEngine3D V1.0\nREPL.IT EDITION - Expect Low Quality\n\nPlayer Position:\nX: {self.player.pos[0]}\nY: {self.player.pos[1]}\nZ: {self.player.pos[2]}\n\nWASD - Translate XZ\nSpace, Shift - Translate Y\nMouse - Look\nEsc - Exit\n\n{self.fps} FPS")
		return

	def Instantiate(self, type="plane", pos=[0, 0, 0], size=[10, 10], axis="x", colour="white", outline="black"):
		type = type.lower()
		if type == "plane":
			obj = Plane(pos=pos, size=size, axis=axis, colour=colour, outline=outline)
			self.scene.append(obj)


	def onMouse(self, pos):
		x = (((pos.x + 1) / self.screen[0]) - 0.502)
		y = (((pos.y + 1) / self.screen[1]) - 0.502)
		self.player.rotation = [int(x * 360), int(y * 360)]

	def mainLoop(self):
		with Listener(on_press=self.onPress, on_release=self.onRelease) as listener:
			self.fps = 1
			count = 10
			while not self.abort:
				s = time()

				# Key press handling
				c = 0
				for key in self.wasd:
					if key == True:
						if c == 0:
							self.player.pos[2] -= self.speed
						elif c == 2:
							self.player.pos[2] += self.speed
						elif c == 1:
							self.player.pos[0] += self.speed
						elif c == 3:
							self.player.pos[0] -= self.speed
						elif c == 4:
							self.player.pos[1] += self.speed
						elif c == 5:
							self.player.pos[1] -= self.speed
					c += 1
				
				self.renderScene()
				self.root.update()
				try:
					self.fps = int(1 / (time() - s))
				except:
					self.fps = "ERR"
	
class Player:
	def __init__(self, pos=[0, 0, 0], rotation=[0, 0]):
		self.pos = pos
		self.rotation = rotation

class Plane:
	def __init__(self, pos=[0, 0, 0], size=[10, 10], axis="x", colour="white", outline="black"):
		self.pos = pos
		self.size = size
		self.axis = axis
		self.colour = colour
		self.outline = outline
		self.type = "plane" # Reference purposes
	
