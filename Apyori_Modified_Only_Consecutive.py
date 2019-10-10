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

file_path = "/Users/aasharashrestha/Documents/PycharmProjects/SeasonalTrends/Seasonality_Project/Paper_5/Project"
start = datetime.datetime.now()
print("Started at: ", start)
global freqSet
freqSet = defaultdict(int)

for key in freqSet:
    if isinstance(key, str):
        freqSet = {(k,): int(v) for k, v in freqSet.items()}

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
def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet, allowGaps):
        countNumberofTrnsactions = 0
        """calculates the support for items in the itemSet and returns a subset
       of the itemSet each of whose elements satisfies the minimum support"""
        _itemSet = list()
        localSet = defaultdict(int)

        for item in itemSet:
            if isinstance(item, str):
                freqSet = {(k,): int(v) for k, v in freqSet.items()}
                localSet = freqSet.copy()
                break
            else:
                if allowGaps:
                    for transaction in transactionList:
                        countNumberofTrnsactions += 1
                        if subset_in_order(item, transaction):
                            freqSet[item] += 1
                            localSet[item] += 1
                else:
                    lst = []
                    for i in item:
                        lst.append(int(i.split("_")[0]))

                    if isConsecutive(lst):
                        for transaction in transactionList:
                            countNumberofTrnsactions+=1

                            if subset_in_order(item, transaction):
                                item = tuple(sorted(item))
                                freqSet[item] += 1
                                localSet[item] += 1


        print("Number of times it checks transaction: ", countNumberofTrnsactions)
        for item, count in localSet.items():
            if isinstance(item,str):
                item = (item,)
            support = float(count)/len(transactionList)

            if support >= minSupport:
                    _itemSet.append(item)

        return _itemSet

@timing
def subset_in_order(sub,lst):
    j = iter(lst)
    sub = sorted(sub)
    for i in sub:
        while True:
            try:
                j_ = j.__next__()
            except StopIteration:
                return False
            if i == j_:
                break
    return True

@timing
def isConsecutive(l):
    # Checks if the sequence is continuous, not allowing any gaps in the sequence so that every events are in order
    if isinstance(l, frozenset):
        l = list(l)

    if isinstance(l[0], frozenset):
        lst = (list(x) for x in l)
        l = []
        for i in lst:
            l.append(i[0])

    if len(l) == 1:
        return True

    if (isinstance(l[0], tuple)):
        # Unpacking tuple and converting it to list
        tupToList = []
        for i in l:
            for j in i:
                tupToList.append(j)
        l = tupToList

    # if "_" in l[0]: #extracting tags and see if they are consecutive
    #     tupToList = []
    #     for key, val in enumerate(l):
    #         tupToList.append(int(l[key].split("_")[0]))
    #     l = tupToList
    l = [int(x) for x in l]
    l = sorted(l)
    n = len(l) - 1
    consecutive = sum(np.diff(l) == 1) >= n
    return (consecutive)

@timing
def inAscendingOrder(itemSet):
    flag = 0
    if (all(int(itemSet[i].split("_")[0]) < int(itemSet[i + 1].split("_")[0]) for i in range(len(itemSet) - 1))):
        flag = 1
    if (flag):
        return True
    else:
        return False


@timing
def joinSet(itemSet, length):
    itemSet_ = set()
    tuple_of_tuples = ()
    uniqueTagCheckSet = set()

    # comb = itertools.combinations(itemSet, length)

    for i in itemSet:
        for j in itemSet:
            # making sure that the values do not come from same column
            # uniqueTagCheckSet.add(i.split("_")[0])
            # uniqueTagCheckSet.add(j.split("_")[0])
            a = tuple(set(i + j))
            if len(a) == length:
                if (hasDuplicate(a) == False):
                    itemSet_.add(a)
    """Join a set with itself and returns the n-element itemsets"""
    return itemSet_

#check if tuple has duplicate value
def hasDuplicate(listOfTuple):
  count_map = {}
  for i in listOfTuple:
    count_map[i] = count_map.get(i, 0) + 1
  if any(v > 1 for v in count_map.values()):
    return True
  return False

@timing
def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = (record)
        transactionList.append(transaction)
        for item in transaction:
            if item not in freqSet:
                freqSet[item] = 1
            else:
                freqSet[item] +=1
            itemSet.add(item)              # Generate 1-itemSets
    return itemSet, transactionList

@timing
def isLessThan(a,b):
    '''Checks if elements in a is greater than equal to elements in b'''
    for i in a:
        for j in b:
            if int(i)>=int(j):
                return False
    return True

@timing
def runApriori(data_iter, minSupport, minConfidence, allowGaps):
    """
    run the apriori algorithm. data_iter is a record iterator
    Return both:
     - items (tuple, support)
     - rules ((pretuple, posttuple), confidence)
    """
    itemSet, transactionList = getItemSetTransactionList(data_iter)


    largeSet = dict()
    # Global dictionary which stores (key=n-itemSets,value=support)
    # which satisfy minSupport

    _rulesSet = set()
    # Dictionary which stores Association Rules

    oneCSet = returnItemsWithMinSupport(itemSet,
                                        transactionList,
                                        minSupport,
                                        freqSet,
                                        allowGaps)


    currentLSet = oneCSet
    k = 2
    while(currentLSet != []):

        largeSet[k-1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet,
                                                transactionList,
                                                minSupport,
                                                freqSet,
                                                allowGaps)
        currentLSet = currentCSet
        k = k + 1
        print("k: ", k)

    @timing
    def getSupport(item):
            """local function which Returns the support of an item"""
            if len(item) == 1:
                item = ''.join(item)
                # item = str(item)
            a = float(freqSet[item])
            b = len(transactionList)
            return float(freqSet[item])/len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item)) for item in value])

    count = 0
    for tup in toRetItems:
        if len(tup) != 1:
            # tup = sortedList(tup)
            tup = tuple(sorted(tup))
            i = tup[:len(tup)-1]
            j = tup[len(tup)-1:]

            _rulesSet.add((i, j))
    print("Number of Rules:", len(_rulesSet))

    for item in _rulesSet:
        confidence = 0
        # a = getSupport(element for tupl in item for element in tupl)
        a = getSupport(item[0] + item[1])
        b = getSupport(item[0])
        # print(item[0], " = ", b)
        # print(item[1], " = ", a)
        try:
            confidence = a / b
        except:
            print("the overflow has occured.")
            print(item[0], " = ", b)
            print(item[1], " = ", a)
            print(b)
            print(a)
        count += 1
        # removing the tags after underscores for every element
        print(item[0]," -> ", item[1], " : ", confidence)
        # print(list(re.sub('(.*)_\\w+', '\\1', x) for x in item[0]), " -> ",
        #       list(re.sub('(.*)_\\w+', '\\1', x) for x in item[1]), " : ", confidence)

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
file = file_path + '/txn_1.csv'
inFile = dataFromFile(file)
# runApriori(inFile,  0.0001, 0.0001, 1) #Params: FileName, minsupport, minconfidence, allowgaps(1,0)
runApriori(inFile,  0.0001, 0.0001, 0)
# runApriori(inFile,  0,0)

finish = datetime.datetime.now()
print("Finished at: ", finish)

time_taken = (finish - start)

df = pd.DataFrame(methodTimeLog.items(), columns=["Method", "Time Taken"])
print(df)
print("Time taken in seconds: ", time_taken.seconds)
print("Time taken in hours: ", time_taken.days)
