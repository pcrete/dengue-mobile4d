from math import *
from csv import *
import json

def by_radius(target_streets, lat, lng, radius=500):

	# radius of the Earth in km
	r = 6371000.0	
	phi1, lamdha1 = radians(lat), radians(lng)

	to_remove = []
	for ind, features in enumerate(target_streets['features']):
	    coordinate = features['geometry']['coordinates']

	    x = len(coordinate)-1
	    while x >= 0:
	        phi2 = radians(float(coordinate[x][1]))
	        lamdha2 = radians(float(coordinate[x][0]))

	        diff_phi = phi2 - phi1
	        diff_lamdha = lamdha2 - lamdha1
	        distance = 2 * r * asin(sqrt(pow(sin((diff_phi) / 2), 2) + cos(phi1) * cos(phi2) * pow(sin((diff_lamdha) / 2), 2)))

	        if distance >= radius:
	            del features['geometry']['coordinates'][x]
	        x -= 1

	    if len(features['geometry']['coordinates']) == 0:
	        to_remove.append(ind)
	    

	for i in sorted(to_remove, reverse=True):
	    del target_streets['features'][i]

	return target_streets