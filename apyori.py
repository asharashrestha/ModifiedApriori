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
t0 = time()

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
    if len(l) == 1:
        return False
    if "_" in str(l[0]):
        lst = []
        for i in l:
            lst.append(int(i.split("_")[0]))
        l = lst
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
                for transaction in transactionList:
                    countNumberofTrnsactions+=1
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

        # return set([i.union(j) for i in itemSet for j in itemSet if int(i) < int(j) and len(i.union(j)) == length])
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
            _subsets = map(frozenset, [x for x in subsets(item)])
            for element in _subsets:
                remain = item.difference(element)
                if len(remain) > 0:
                    confidence = getSupport(item)/getSupport(element)
                    if confidence >= minConfidence:
                        toRetRules.append(((tuple(element), tuple(remain)),
                                           confidence))
    return toRetItems, toRetRules


# def printResults(items, rules):
#     """prints the generated itemsets sorted by support and the confidence rules sorted by confidence"""
#     for item, support in sorted(items, key=lambda (item, support): support):
#         print ("item: %s , %.3f" % (str(item), support))
#     print ("\n------------------------ RULES:")
#     for rule, confidence in sorted(rules, key=lambda (rule, confidence): confidence):
#         pre, post = rule
#         print ("Rule: %s ==> %s , %.3f" % (str(pre), str(post), confidence))
@timing
def printRules(rules):
    count = 0
    filter_count = 0
    for ind, val in enumerate(sorted(rules, key = lambda tup: (-tup[1]))): #sort rules by confidence
        lhs_rhs, conf = val
        # lhs, rhs = map(lambda x, y: x,y = i for i in lhs_rhs)
        lhs, rhs = lhs_rhs

        count+=1
        tag_list = []
        tag_list.append(int(rhs[0].split("_")[0]))

        for i in lhs:
            tag_list.append(int(i.split("_")[0]))
        #Filtering Rules so that no gaps are allowed between orders. And constraining RHS to only one element.
        if isConsecutive(tag_list):
            if len(rhs) == 1:
                if all(int(rhs[0].split("_")[0]) > int(i.split("_")[0]) for i in lhs):
                    print(lhs, '->', rhs, ":", conf)
                    filter_count+=1
        # print(lhs[0], '->', rhs[0], ":", conf) #print rules without filter
    print("Number of Rules without filter: ", count)

    print("Number of Rules after filter: ",filter_count)

# @timing
# def dataFromFile(fname):
#     """Function which reads from the file and yields a generator"""
#     file_iter = open(fname)
#     for line in file_iter:
#         line = line.strip().rstrip(',')
#         # # print("LIne: ", line)
#         # ind_item_list=[]
#         # for i in line:
#         #     ind_item_list.append(i.strip(',') + 'tag_1')
#         #     # print(ind_item_list)
#         # # Remove trailing comma
#         record = (line.split(','))
#         yield record

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
# inFile = dataFromFile("/Users/aasharashrestha/Documents/PycharmProjects/SeasonalTrends/Seasonality_Project/Paper_5/Project/test.csv")

inFile = dataFromFile('/Users/aasharashrestha/Documents/PycharmProjects/SeasonalTrends/Seasonality_Project/Paper_5/Project/Data/ScenarioA.csv')
items, rules = runApriori(inFile,  0.01, 0)

printRules(rules)

finish = datetime.datetime.now()
print("Finished at: ", finish)

time_taken = (finish - start)

df = pd.DataFrame(methodTimeLog.items(), columns=["Method", "Time Taken"])
print(df)

print("Training time:", round(time()-t0, 3), "s")
print("Time taken in seconds: ", time_taken.seconds)
print("Time taken in hours: ", time_taken.days)

#filtering rules
# def filterRules(rules):
#     for ind, val in enumerate(rules):
#         print(val)
#         lhs_rhs, conf = val
#         for i in lhs_rhs:
#             lhs, rhs = lhs_rhs
#             print(lhs, " and ",rhs)
#         break

# filterRules(rules)