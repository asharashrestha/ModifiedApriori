"""
Description     : Simple Python implementation of the Apriori Algorithm
Usage:
    $python apriori.py -f DATASET.csv -s minSupport  -c minConfidence
    $python apriori.py -f DATASET.csv -s 0.15 -c 0.6
"""

import datetime
from itertools import chain, combinations
from collections import defaultdict
import time
from functools import wraps
from time import time
import pandas as pd
import numpy as np

start = datetime.datetime.now()
print("Started at: ", start)

methodTimeLog = dict()

def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        fName = str(f).split(" ")[1]
        # print ('Elapsed time:',f ,format(end-start))
        if fName not in methodTimeLog:
            methodTimeLog[fName] = end - start
        else:
            methodTimeLog[fName] = methodTimeLog[fName] + (end - start)

        methodTimeLog[fName] += end-start
        return result
    return wrapper

@timing
def subsets(arr):
    """ Returns non empty subsets of arr"""
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

@timing
def isConsecutive(l):
    n = len(l) - 1
    return (sum(np.diff(sorted(l)) == 1) >= n)

@timing
def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
        countNumberofTrnsactions = 0
        """calculates the support for items in the itemSet and returns a subset
       of the itemSet each of whose elements satisfies the minimum support"""
        _itemSet = set()
        localSet = defaultdict(int)

        for item in itemSet:
            if len(item) > 1:
                lst = []
                for i in item:
                    lst.append(int(i.split("_")[0]))
                if isConsecutive(lst):
                    for transaction in transactionList:
                        countNumberofTrnsactions+=1
                        if item.issubset(transaction):
                                freqSet[item] += 1
                                localSet[item] += 1
            else:
                for transaction in transactionList:
                    countNumberofTrnsactions += 1
                    if item.issubset(transaction):
                        freqSet[item] += 1
                        localSet[item] += 1


        print("Number of times it checks transaction: ", countNumberofTrnsactions)
        for item, count in localSet.items():
                support = float(count)/len(transactionList)

                if support >= minSupport:
                        _itemSet.add(item)

        return _itemSet

@timing
def joinSet(itemSet, length):
    """Join a set with itself and returns the n-element itemsets"""
    tempItemSet = set()
    for i in itemSet:
        for j in itemSet:
            if len(i.union(j)) == length:
                tempItemSet.add(i.union(j))
    return tempItemSet

@timing
def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = (record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))              # Generate 1-itemSets
    return itemSet, transactionList

@timing
def runApriori(data_iter, minSupport, minConfidence):
    """
    run the apriori algorithm. data_iter is a record iterator
    Return both:
     - items (tuple, support)
     - rules ((pretuple, posttuple), confidence)
    """
    itemSet, transactionList = getItemSetTransactionList(data_iter)

    freqSet = defaultdict(int)
    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    assocRules = dict()
    # Dictionary which stores Association Rules

    oneCSet = returnItemsWithMinSupport(itemSet,
                                        transactionList,
                                        minSupport,
                                        freqSet)

    currentLSet = oneCSet
    k = 2
    while(currentLSet != set([])):
        largeSet[k-1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet,
                                                transactionList,
                                                minSupport,
                                                freqSet)
        currentLSet = currentCSet
        k = k + 1
        print("k: ", k)

    @timing
    def getSupport(item):
            """local function which Returns the support of an item"""
            return float(freqSet[item])/len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item))
                           for item in value])

    toRetRules = []
    for key, value in list(largeSet.items())[1:]:
        for item in value:
            item = sorted(list(item))
            a = item[:len(item)-1]
            b = item[len(item)-1:]

            a = frozenset(a)
            b = frozenset(b)
            item = frozenset(item)
            confidence = getSupport(item)/getSupport(a)
            if confidence >= minConfidence:
                toRetRules.append(((tuple(a), tuple(b)),
                                   confidence))
    return toRetItems, toRetRules


@timing
def printRules(rules):
    count = 0
    for ind, val in enumerate(sorted(rules, key = lambda tup: (-tup[1]))): #sort rules by confidence
        lhs_rhs, conf = val
        # lhs, rhs = map(lambda x, y: x,y = i for i in lhs_rhs)
        lhs, rhs = lhs_rhs
        count+=1
        print(lhs, '->', rhs, ":", conf)
        # print(lhs[0], '->', rhs[0], ":", conf)
    print("Number of Rules: ", count)


@timing
def dataFromFile(fname):
    """Function which reads from the file and yields a generator"""
    file_iter = open(fname)
    for line in file_iter:
        line = line.strip().rstrip(',')
        record = (line.split(','))
        recordWithTag = []  # new list after tag is added
        for key, val in enumerate(record):
            if val !="":
                val = str(key + 1) + "_" + val
                recordWithTag.append(val)
        yield recordWithTag


start = datetime.datetime.now()
print("Started at: ", start)

# inFile = dataFromFile('Adm_ICD_Proc.csv')
inFile = dataFromFile('txn_1.csv')
items, rules = runApriori(inFile,  0.0001, 0.0001)

printRules(rules)

finish = datetime.datetime.now()
print("Finished at: ", finish)

time_taken = (finish - start)

df = pd.DataFrame(methodTimeLog.items(), columns=["Method", "Time Taken"])
print(df)
print("Time taken in seconds: ", time_taken.seconds)
print("Time taken in hours: ", time_taken.days)
