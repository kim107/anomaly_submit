#!/usr/bin/python

import json 
import numpy as np
import pandas as pd 
import math

def record_anomaly(my_amount,anomaly_mean,anomaly_std,index,out):
	""" If my_amount is anomalous, and add it to the dictionary 'out'.
		An anomalous amount is anything greater than mean + 3*sd.
	"""
	if my_amount > anomaly_mean + 3 * anomaly_std :
		out[index] = '%.2f'%((math.floor(anomaly_mean*100))/100.0), '%.2f'%((math.floor(anomaly_std*100))/100.0)
	return out
		
def write_jsonfile(filename,ds,out):
	""" write anomalous purchases in an appropriate format.
	"""
	i=0
	with open(filename, 'w') as fout:
		for row in ds.itertuples() :	
			mydata= {"event_type" : "purchase", "timestamp" : row.timestamp, "id" : str(int(row.id)), "amount" : str('%.2f'%(row.amount)), "mean": str(out[row.index_col][0]), "std": str(out[row.index_col][1])}
			a= '{' + '\"event_type\":\"{event_type}\", \"timestamp\":\"{timestamp}\", \"id\": \"{id}\", \"amount\": \"{amount}\", \"mean\": \"{mean}\", \"sd\": \"{std}\"'.format(**mydata) +'}'
			if i < ds.shape[0]-1:
				a= a+'\n'
				i=i+1
			fout.write(a)