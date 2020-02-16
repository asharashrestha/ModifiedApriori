from tkinter import *
import pandas as pd
from treelib import Node, Tree
from time import time
import datetime
import rules_tree

t0 = time()

start = datetime.datetime.now()
print("Started at: ", start)

#method to show tree dumped in the file after createRule gets completed.
def showTree():
    f = open('tree.txt', 'r')
    text = ""
    for i in range(10):
        contents = f.read()
        # t = list(contents)
        # break
        text += contents
    txt = Label( text=text, justify=LEFT)
    f.close()
    txt.pack()
# #Method to create rule tree:
# def createRulesTree():
#     rules_tree.main("1_a")


def createRulesTree(filter=None):
    df_rules = pd.read_csv("Rules.csv", dtype=str)

    df_rules['LHS'] = df_rules.LHS.str.replace('[', '')
    df_rules['LHS'] = df_rules.LHS.str.replace(']', '')
    df_rules['LHS'] = df_rules.LHS.str.replace('\'', '')

    rules_len_2_set = set()

    #filter df for LHS with the argument given by user.
    if filter!=None:
        df_rules = df_rules[df_rules['LHS'].str.contains(filter)]

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
            tree.save2file('tree.txt',line_type='ascii-em')
            showTree()

#It starts by creating a Tk object and pass it to a tkinter frame created with Frame()
root = Tk()
root.title("Tk dropdown example")
mainframe = Frame(root)

#A grid is added to the frame which will hold the combo-box.
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 100)

#The popup menu contains a list of options which is defined in the variable choices.
# A Tkinter variable is created with the line:
tkvar = StringVar(root)

# Dictionary with options
filepath = "/Users/ashara/Documents/Data/Scenario1_Top10CCS.csv"
df = pd.read_csv(filepath)
tkvar.set('Select') # set the default option

#The default value of the variable is set with the .set() method.
#We create the Tkinter combobox with:

#dropdown for Age Group
choices = set(df.AGE_GROUP.unique())
popupMenu = OptionMenu(mainframe, tkvar, *choices)
Label(mainframe, text="Choose an event").grid(row = 1, column = 1)
popupMenu.grid(column =1)

# #dropdown for LOS
# choices = set(df.PRIMARY_DX.unique())
# popupMenu_1 = OptionMenu(mainframe, tkvar, *choices)
# popupMenu_1.grid(column =1)
#
# #dropdown for PRIMARY_DX
# choices = set(df.PRIMARY_DX.unique())
# popupMenu_2 = OptionMenu(mainframe, tkvar, *choices)
# popupMenu_2.grid(column =1)
#
# #dropdown for DEVELOPED_SEPTICEMIA
# choices = set(df.DEVELOPED_SEPTICEMIA.unique())
# popupMenu_3 = OptionMenu(mainframe, tkvar, *choices)
# popupMenu_3.grid(row = 5, column =1)


#Buttont0 = time()

start = datetime.datetime.now()
print("Started at: ", start)
print("Value from popmenu: ", mainframe.getvar() tkvar.get())
Btn1 = Button(root, text="Show Rule Tree",  command=lambda : createRulesTree(popupMenu))
# xbBrowse = Button(frameN, text="Browse...", font=fontReg, command=lambda : createRulesTree())

Btn1.pack()

#if event chosen then filter the LHS by this event.

mainframe.mainloop()

