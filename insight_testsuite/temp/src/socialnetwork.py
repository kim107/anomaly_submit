#!/usr/bin/python

import sys
import json 
import numpy as np
import pandas as pd 

def befriend(a,b,socialNetwork) :
	""" Make a and b friends in socialNetwork.
	"""
	if a not in socialNetwork.keys() :
		socialNetwork[a] = [b]
	elif b not in socialNetwork[a]:
		socialNetwork[a].append(b)
	if b not in socialNetwork.keys() :
		socialNetwork[b] = [a]
	elif a not in socialNetwork[b]:
		socialNetwork[b].append(a)
	return socialNetwork

def unfriend(a,b,socialNetwork) :
	""" Unfriend a and b in socialNetwork.
	"""
	if a in socialNetwork.keys() :
		if b in socialNetwork[a] :
			socialNetwork[a].remove(b)
		if socialNetwork[a] == [] :
			del socialNetwork[a]
	if b in socialNetwork.keys() :
		if a in socialNetwork[b] :	
			socialNetwork[b].remove(a)
		if socialNetwork[b] == [] :
			del socialNetwork[b]
	return socialNetwork
	

def findfriends(socialNetwork,myFriends,i,depth,D,master) :
	""" Return list of friends 'myFriends', who are D-depth friends of 'i', excluding 'master'.
		e.g. 2-depth friends: friends, and friends of friends. 
	"""
	if depth > 0 :
		if i not in myFriends :
			if i != master :
				myFriends.append(i)
	depth = depth + 1
	if depth < D+1 :
		for j in socialNetwork[i] :
			myFriends = findfriends(socialNetwork,myFriends,j,depth,D,master)
		return myFriends
	else :
		return myFriends

def makeSocialNetwork(socialNetwork, df):
	""" Create 'socialNetwork' of type 'dictionary' from pandas-DataFrame 'df' by iterating over each row.
	"""
	for row in df.itertuples() :
		a = row.id1
		b = row.id2
		if row.event_type == 'befriend':					
			socialNetwork = befriend(a,b,socialNetwork)			
		if row.event_type == 'unfriend' :			
			socialNetwork = unfriend(a,b,socialNetwork)			
	return socialNetwork