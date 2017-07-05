
import unittest
import doctest
import os
import sys
import imp
from result import *
from socialnetwork import *



class TestSocialnetwork(unittest.TestCase):

    def test_befriend(self):
        socialNetwork = {"a":["b"], "b":["a"]}        
        self.assertEqual(socialNetwork, befriend("a","b",{}), "function befriend is not working")
        socialNetwork2 = {"a":["b","c"], "b":["a"], "c":["a"]}        
        self.assertEqual(socialNetwork2, befriend("a","c",socialNetwork), "function befriend is not working")

    def test_unfriend(self):
        socialNetwork2 = {"a":["b","c"], "b":["a"], "c":["a"]}        
        socialNetwork = {"a":["b"], "b":["a"]}        
        self.assertEqual(socialNetwork, unfriend("c","a",socialNetwork2), "function unfriend is not working")        
        self.assertEqual({}, unfriend("a","b",socialNetwork), "function unfriend is not working") 
        self.assertEqual({}, unfriend("a","b",{}), "function unfriend is not working") 

    def test_findfriends(self):
        socialNetwork = {"1":["3","2"], "2":["1"], "3":["1"]}                        
        self.assertEqual(["1"], findfriends(socialNetwork,[],"2",0,1,"2"), "function findfriends is not working")
        a=findfriends(socialNetwork,[],"2",0,2,"2")
        result = ["1","3"]        
        boolr = True
        for i in a :
            if i not in result :
                boolr = False
        for i in result :
            if i not in a :
                boolr = False
        self.assertTrue(boolr, "function findfriends is not working")
        socialNetwork = {"1":["3","2"], "2":["1","3","4","9"], "3":["1","2"], "4":["2","5","7"], "5":["4","7"], "6":["5","8"], "7":["4"], "8":["6"], "9":["2","10"], "10":["9"]}                        
        a=findfriends(socialNetwork,[],"1",0,3,"1")
        result = ["2","3","4","5","7","9","10"]        
        boolr = True
        for i in a :
            if i not in result :
                boolr = False
        for i in result :
            if i not in a :
                boolr = False
        self.assertTrue(boolr, "function findfriends is not working")

    def test_makeSocialNetwork(self):
        tmp = [{'event_type': 'befriend', 'id1':'1', 'id2':'2'},
                {'event_type': 'befriend', 'id1':'2', 'id2':'3'},
                {'event_type': 'befriend', 'id1':'1', 'id2':'3'},
                {'event_type': 'befriend', 'id1':'3', 'id2':'2'},
                {'event_type': 'unfriend', 'id1':'3', 'id2':'2'},
                {'event_type': 'unfriend', 'id1':'3', 'id2':'2'},
                {'event_type': 'unfriend', 'id1':'3', 'id2':'4'}]
        socialNetwork = {"1":["2","3"], "2":["1"], "3":["1"]}                        
        df = pd.DataFrame(tmp)
        # print(df.info(), type(df))
        self.assertEqual(socialNetwork, makeSocialNetwork({}, df), "function makeSocialNetwork is not working")

class TestResult(unittest.TestCase):

    def test_record_anomaly(self):
        out={}
        out = record_anomaly(100.0,1.0,4.0,0,out)
        boolr = out[0][0] == "1.00" and out[0][1] =="4.00"
        self.assertTrue(boolr, "function findfriends is not working")
        
    

if __name__ == "__main__":
    unittest.main(exit=False)         
