#!/usr/bin/python

import sys
import json 
import numpy as np
import pandas as pd 
import math
import time
from socialnetwork import *
from result import *

def main() :
	batchfile = sys.argv[1]  # './log_input/batch_log.json'
	streamfile = sys.argv[2] #' ./log_input/stream_log.json'
	outputfile = sys.argv[3] #' flagged_purchases.json'

###############################################################################################################
# Step 1 : (a) Read batchfile into 'df', and set 'D' and 'T'.
#          (b) Sort 'df' first in timestamp and then in col_index.
#          (c) Set 'db' as rows of 'df' where 'event_type=purchase'.
###############################################################################################################
	df = pd.read_json(batchfile, lines = True, dtype ={'id':str, 'id1':str, 'id2':str, 'amount':float }) # read batchfile and save as 'df' panda-DataFrame
	D = int(df.iloc[0]['D']) # D: number of degrees >=1
	T = int(df.iloc[0]['T']) # T: number of consecutive purchases >=2
	df.drop(['D','T'], axis=1, inplace=True) # drop columns with index 'D' and 'T'
	df = df[~df["event_type"].isnull()]	# delete unnecessary rows
	df['index_col'] = df.index # set new column as index
	df = df.sort_values(['timestamp','index_col']) # sort 'df' first by 'timestamp' and then by 'column_index'
	db = df.loc[df.event_type=='purchase'] # define new database with only 'event_type'='purchase'
	db = db.drop(['id1','id2','index_col','event_type'], axis=1) # drop unnecessary columns
###############################################################################################################
# Step 2 : From batchfile, create socialNetwork, a dictionary.
###############################################################################################################
	socialNetwork = {}
	socialNetwork = makeSocialNetwork(socialNetwork, df)

###############################################################################################################
# Step 3 : (a) Read streamfile into 'ds'.
#          (b) Sort 'ds' first in timestamp and then in col_index.
###############################################################################################################
	ds = pd.read_json(streamfile, lines = True, dtype ={'id':str, 'id1':str, 'id2':str, 'amount':float }) # read stream and save as 'ds' panda-DataFrame
	ds['index_col'] = ds.index # set new column as index
	ds = ds.sort_values(['timestamp','index_col']) # sort 'ds' first by 'timestamp' and then by 'column_index'
	
###############################################################################################################	
# Step 4 : For each row in the 'ds' (steamfile), check if there is any anomalous purchases and record them to 'out'. 
#		   Also append rows of 'ds' to 'db' if 'event_type'='purchase'. 
###############################################################################################################
	out = {} # dictionary of anomalies 
	for row in ds.itertuples() :
		# check_stream(row,db,D,T,out,socialNetwork)
		if row.event_type == "purchase" :
			# find id's D-depth friends.
			myFriends = []
			myFriends = findfriends(socialNetwork,myFriends,row.id,0,D,row.id)		
			dfriend = db.loc[db['id'].isin(myFriends)].tail(T)
			mydata= {"timestamp" : row.timestamp, "id" : str(row.id), "amount" : row.amount } 	
			# If a user's social network has made 2 or more purchases, check if the purchase is anomalous.
			if dfriend.shape[0] > 1 :
				out = record_anomaly(row.amount,dfriend['amount'].mean(),dfriend['amount'].std(ddof=0),row.index_col,out)				
			db = db.append(mydata, ignore_index=True)		
		elif row.event_type == "befriend" :
			socialNetwork = befriend(row.id1,row.id2,socialNetwork)
		elif row.event_type == "unfriend" :
			socialNetwork = unfriend(row.id1,row.id2,socialNetwork)

###############################################################################################################	
# Step 5 : Write the anomalous purchases in output file.
###############################################################################################################	
	write_jsonfile(outputfile,ds.iloc[list(out.keys())].sort_values(['index_col']),out)

if __name__ == "__main__":main() 