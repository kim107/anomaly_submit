# Table of Contents
1. [Data Structure](README.md#Data-Structures)
2. [Algorithm](README.md#Algorithm)
3. [Files](README.md#Files)

# Data Structure

* **df** : DataFrame read from the file 'batch_log.json', (pandas-DataFrame).

	columns of df : "D", "T", "event_type", "timestamp", "id", "id1", "id2", "amount"

* **ds** : DataFrame read from the file 'stream_log.json', (pandas-DataFrame). 

	columns of df : "event_type", "timestamp", "id", "id1", "id2", "amount"

* **db** : our (previous) database from **df** and **ds** with "event_type"="purchase", (pandas-DataFrame).

	**db** is used to calculate mean and std of latest **T** transactions of user's **D**-depth friends.

* **D** : the number of degrees that defines a user's social network.

* **T** : the number of consecutive purchases made by a user's social network.

* **socialNetwork** : dictionary of current social network. 

	 e.g. if '1' and '2' are friends, then socialNetwork = {'1':'2', '2':'1'}

* **myFriends** : user's **D**-depth friends, (list).

* **dfriend** : latest **T** transactions of user's **D**-depth friends.

* **out** : records anomalous purchases, (dictionary of tuples).

# Algorithm

See the file **src/process_log.py**

1 Read *batch_log_json* and create **df** and our main database **db**.

*	(a) Read **batch_log.json** and set **df**, **D** and **T**.

*	(b) Sort **df** first in *timestamp* and then in *index_col*.

*	(c) Set **db** = rows of **df** where *event_type=purchase*.

2 From **df**, create **socialNetwork**

3 Read *stream_log.json* and set **ds**

*	(a) Read *stream_log.json* into **ds**.

*	(b) Sort **ds** first in *timestamp* and then in *index_col*.


4 In **ds** (stream_log.json), check if there are any anomalous purchases and record them to **out**. Also append rows of **ds** with *"event_type"* = *"purchase"* to **db**. 

5 Write the anomalous purchases in **flagged_purchases.json**.

# Files
## Source files under folder src :
* process_log.py : main algorithm

* socialnetwork.py : contains functions associated with social network.

* result.py : contains functions associated with finding anomalous purchases and writing results.

* tests.py : contains unit tests

#### process_log.py : main algorithm, see section **Algorithm**

#### socialnetwork.py :

1. befriend :

	input : two individuals : **a** (string) and **b** (string) and **socialNetwork** (dictionary).
 
	output : updated **socialNetwork** with **a** and **b** friends.

2. unfriend : 

	input : two individuals : **a** (string) and **b** (string) and **socialNetwork** (dictionary).
 
	output : updated **socialNetwork** (dictionary) with **a** and **b** not friends.
 
3. findfriends : find D-depth friends recursively. 

	1-depth friends : friends, 2-depth friends : friends and friends of friends, and etc. 
 
	input : **socialNetwork** (dictionary), **myFriends** (List), **i** : user (string),
         **depth** : steps in recursion (int), **D** : depth (int),          
         **master** : the first user **i** in **depth** = 0.
         
	output : updated **myFriends** (List).

4. makeSocialNetwork : Create **socialNetwork** from **df** by iterating over each row.

	input : **socialNetwork** (dictionary), **df** (pandas-DataFrame).
         
	output : updated **socialNetwork** (dictionary) with **a** and **b** not friends.

### result.py

1. record_anomaly : If my_amount is anomalous, then add it to the dictionary **out**. An anomalous amount is anything greater than mean + 3*sd.

	input : **my_amount** : my purchase amount (float), 
        	**anomaly_mean** : mean of amount of purchases in my network (float),
	        **anomaly_stdv** : standard deviation of amount of purchases in my network (float),
        	**index** : current index (int),
	        **out** : dictionary of tuples (mean, std) in an appropriate format,

	output : **out**        

2. write_jsonfile : write anomalous purchases in an appropriate format.

	input : **filename** (string)
        **ds** (pandas-DataFrame)
        **out** : dictionary of tuples (mean, std) in an appropriate format        
