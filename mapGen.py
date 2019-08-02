import os
import numpy as np
import noise
import random
from PIL import Image

SCRIPT_PATH = (os.path.dirname(os.path.abspath(__file__)))
SEED = random.randint(1,100000)

# Image Dimensions
width = 2048	
height = 1024
shape = (height, width)

#Perlin Noise Parameters
scale = 200
octaves = 5
persistence = .5
lacunarity = 2.0
land_bias = 0.0		# Recommeneded range: -0.25 to 0.25  --- Negative for more water, Positive for more land, 0 for neutral

#Filters
filter1_on = True
filter2_on = False

def main():

	#Make first filter into an object and convert to range 0 and 1
	filter1 = filter("geography12.png", 0.67)
	filter1_prepared = filter1.prepare_filter()

	#Make initial world filled with noise layers and pre-set filter
	world = make_noise(filter1_prepared, filter1)

	#Change unbounded range to range of 0 and 1
	interpolated_world = interpolate_world(world)

	#Creates an array from the interpolated world that adds land_bias and the second filter
	refined_world = refine_world(interpolated_world)

	#Create array for colored world from refined world
	colored_world = add_color(refined_world)

	#Image output
	image_output(colored_world)

class filter:
	def __init__(self, name, bias, path=SCRIPT_PATH + "\\filters"):
		self.name = name
		self.bias = bias
		self.path = path

	def prepare_filter(self):

		##load red value as grayscale ('g' or 'b' would work as well) 
		img = Image.open(self.path + "/" + self.name, mode="r").convert('L')

		##save as array and divide by 255 to convert to range between 0 and 1
		filter_array = np.array(img) / 255

		return filter_array

def make_noise(filter_arr=None, filter_obj=None):

	#Make an array from layers of perlin noise and preset filters

	#Create empty array
	world = np.zeros(shape)

	#Fill world array with noise values
	for i in range(shape[0]):
		for j in range(shape[1]):
			
			#fill with noise
			world[i][j] = noise.pnoise3(i/scale, 
										j/scale, 
										SEED,
										octaves = octaves, 
										persistence = persistence, 
										lacunarity = lacunarity, 
										repeatx= width, 
										repeaty= height, 
										base= 0)

			#Apply pre-set filter
			world[i][j] = world[i][j] - ((filter_arr[i][j]) * filter_obj.bias)

			#add more noise layers
			for k in range(1,4):
				world[i][j] = world[i][j] + noise.pnoise3(i/(scale * (3 * k)), 
										j/(scale * (5 * k)), 
										SEED, 
										octaves = int(octaves + k), 
										persistence = persistence / k, 
										lacunarity = lacunarity * k, 
										repeatx= width, 
										repeaty= height, 
										base= 0)
	return world

def interpolate_world(unbound_world):

	#Scales elements in an array to the range 0 and 1

	return np.interp(unbound_world, (unbound_world.min(), unbound_world.max()), (0, 1))

def refine_world(crude_world):

	#Modifications to world after it has been generated from noise and interpolated to a range between 0 and 1

	#Adds land bias and pre-set filter
	for i in range(shape[0]):
		for j in range(shape[1]):
			crude_world[i][j] = crude_world[i][j] + land_bias #- ((filter2[i][j]) * filter2_bias)

	return crude_world


def add_color(grayworld):

	#Zone Colors

	water_deep = [50,50,135]
	water_medium = [50,50,150]
	water_shallow = [50,50,165]
	sand_low = [195,180,125]
	sand_high = [165, 155, 95]
	fauna_low = [25,145,25]
	fauna_medium = [25,130,25]
	fauna_high = [25,115,25]
	
	#Color the world!

	colored_world = np.zeros(grayworld.shape+(3,))
	
	for i in range(shape[0]):
		for j in range(shape[1]):
			
			if grayworld[i][j]  < 0.28:
				colored_world[i][j] = water_deep

			elif grayworld[i][j]  >= 0.28 and grayworld[i][j] < 0.38:
				colored_world[i][j] = water_medium

			elif grayworld[i][j]  >= 0.38 and grayworld[i][j] < 0.46:
				colored_world[i][j] = water_shallow

			elif grayworld[i][j] >= 0.46 and grayworld[i][j] < 0.48:
				colored_world[i][j] = sand_low

			elif grayworld[i][j] >= 0.48 and grayworld[i][j] < .5:
				colored_world[i][j] = sand_high

			elif grayworld[i][j] >= 0.5 and grayworld[i][j] < 0.6:
				colored_world[i][j] = fauna_low

			elif grayworld[i][j] >= 0.6 and grayworld[i][j] < 0.7:
				colored_world[i][j] = fauna_medium

			elif grayworld[i][j] >= 0.7:
				colored_world[i][j] = fauna_high
	
	return colored_world

def image_output(world):

	##converts array to a color image
	img = Image.fromarray((world).astype('uint8'), 'RGB')

	##Image output options
	##shows image
	img.show()
	##saves as PNG file with name: "map{SEED}" to specified directory
	img.save(SCRIPT_PATH + f"\\maps\\map{SEED}.png")
	##saves to current directory
	#img.save("map2.png")

if __name__ == "__main__":
	main()