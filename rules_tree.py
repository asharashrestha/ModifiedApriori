import pandas as pd
from treelib import Node, Tree

df_rules = pd.read_csv("Rules.csv", dtype=str)

df_rules['LHS'] = df_rules.LHS.str.replace('[', '')
df_rules['LHS'] = df_rules.LHS.str.replace(']', '')

lhs = '\'2_Emergency\''
rhs = '\'3_Not Discharged\''

tree = Tree()
tree.create_node(lhs+"->"+rhs, "root")  # root node

my_queue = []

for index, row in df_rules.iterrows():
    left_rule = lhs +', ' + rhs
    if(row['LHS']== left_rule):
        left = row['LHS']
        right = row['RHS']
        a = left + ", "+ "\'"+ right + "\'"
        tree.create_node(left +"->"+ right + "[Conf:" + row["Conf"] + "]", a, parent="root")
        my_queue.append(left + ", \'"+ right + "\'")

while len(my_queue)!=0:
    elem = my_queue.pop(0)
    for index, row in df_rules.iterrows():
        if(row['LHS'] == elem):
            left = row['LHS']
            right = row['RHS']
            a = left + ", " + "\'" + right + "\'"
            tree.create_node(left + "->" + right + "[Conf:" + row["Conf"] + "]", a, parent= left)
            my_queue.append(left + ", \'" + right + "\'")



tree.show(line_type="ascii-em")

