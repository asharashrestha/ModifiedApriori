import pandas as pd
from treelib import Node, Tree
from time import time
import datetime

t0 = time()

start = datetime.datetime.now()
print("Started at: ", start)

df_rules = pd.read_csv("Rules.csv", dtype=str)

df_rules['LHS'] = df_rules.LHS.str.replace('[', '')
df_rules['LHS'] = df_rules.LHS.str.replace(']', '')
df_rules['LHS'] = df_rules.LHS.str.replace('\'', '')

rules_len_2_set = set()

for index, row in df_rules.iterrows():
    lhs_split = []
    lhs = row['LHS']
    rhs = row['RHS']
    if ',' not in lhs: # keeping such rules as rules where # of elem in lhs and rhs is 1.
        tree = Tree()
        tree.create_node(lhs+"->"+rhs + "[Conf: "+ row["Conf"]+"]", "root")  # root node

        my_queue = []

        for index, row in df_rules.iterrows():
            left_rule = lhs +', ' + rhs
            if(row['LHS']== left_rule):
                left = row['LHS']
                right = row['RHS']
                a = left + ", " + right
                tree.create_node(left +"->"+ right + "[Conf:" + row["Conf"] + "]", a, parent="root")
                my_queue.append(left + ", "+ right)

        while len(my_queue)!=0:
            elem = my_queue.pop(0)
            for index, row in df_rules.iterrows():
                if(row['LHS'] == elem):
                    left = row['LHS']
                    right = row['RHS']
                    a = left + ", " + right # concatenating lhs and rhs to find the result in lhs of dataframe
                    tree.create_node(left + "->" + right + "[Conf:" + row["Conf"] + "]", a, parent= left)
                    my_queue.append(left + ", " + right)

        tree.show(line_type="ascii-em")

print("Tree Generation Time:", round(time()-t0, 3), "s")

