
import tkinter as tk
import pandas as pd
from treelib import Node, Tree
import os


class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.om_variable = tk.StringVar()
        ageChoices  = self.use_age()
        LOSChoices = self.use_LOS()
        DXChoices = self.use_DX()
        HACChoices = self.use_HAC()

        self.om_variable.set("SELECT")
        self.om_variable.trace("w", self.setfilter)
        self.filter = None

        # self.vsb = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        # self.canvas.configure(yscrollcommand=self.vsb.set)
        # self.vsb.pack(side="right", fill="y")

        b1 = tk.Button(self, text="Age", width=12, command=lambda: self.changeOption(ageChoices))
        b2 = tk.Button(self, text="LOS", width=12, command=lambda: self.changeOption(LOSChoices))
        b3 = tk.Button(self, text="Primary DX", width=12, command=lambda: self.changeOption(DXChoices))
        b4 = tk.Button(self, text="HAC Septicemia", width=12, command=lambda: self.changeOption(HACChoices))
        b5 = tk.Button(self, text="Show Rules", width=12, command=self.createRulesTree)
        # l1 = tk.Label(self, text="", command=self.showTree())

        self.om = tk.OptionMenu(self, self.om_variable, *ageChoices)
        self.om.configure(width=20)

        b1.grid(row=0,column=1,columnspan=1)#pack(side="left")
        b2.grid(row=0,column=2,columnspan=1)#.pack(side="left")
        b3.grid(row=0,column=3,columnspan=1)#.pack(side="left")
        b4.grid(row=0,column=4,columnspan=1)#.pack(side="left")
        b5.grid(row=0,column=5,columnspan=1)#.pack(side="left")
        self.om.grid(row=0,column=6,columnspan=1)#pack(side="left")

    def changeOption(self,choices):
        self._reset_option_menu(choices, 0)


    def setfilter(self,*args):
        self.filter = self.om_variable.get()
        print(self.om_variable.get())

    def createRulesTree(self):
        '''

        :param
        :return:
        '''
        print(self.filter)
        df_rules = pd.read_csv("Rules.csv", dtype=str)

        df_rules['LHS'] = df_rules.LHS.str.replace('[', '')
        df_rules['LHS'] = df_rules.LHS.str.replace(']', '')
        df_rules['LHS'] = df_rules.LHS.str.replace('\'', '')

        # filter df for LHS with the argument given by user.
        if self.filter != None:
            df_rules = df_rules[df_rules['LHS'].str.contains(self.filter)]

        for index, row in df_rules.iterrows():
            lhs = row['LHS']
            rhs = row['RHS']
            if ',' not in lhs:  # keeping such rules as rules where # of elem in lhs and rhs is 1.
                tree = Tree()
                tree.create_node(lhs + "->" + rhs + "[Conf: " + row["Conf"] + "]", "root")  # root node

                my_queue = []

                for index, row in df_rules.iterrows():
                    left_rule = lhs + ', ' + rhs
                    if (row['LHS'] == left_rule):
                        left = row['LHS']
                        right = row['RHS']
                        a = left + ", " + right
                        tree.create_node(left + "->" + right + "[Conf:" + row["Conf"] + "]", a, parent="root")
                        my_queue.append(left + ", " + right)

                while len(my_queue) != 0:
                    elem = my_queue.pop(0)
                    for index, row in df_rules.iterrows():
                        if (row['LHS'] == elem):
                            left = row['LHS']
                            right = row['RHS']
                            a = left + ", " + right  # concatenating lhs and rhs to find the result in lhs of dataframe
                            tree.create_node(left + "->" + right + "[Conf:" + row["Conf"] + "]", a, parent=left)
                            my_queue.append(left + ", " + right)

                tree.show(line_type="ascii-em")
                if os.path.exists("tree.txt"):
                    os.remove("tree.txt")

                tree.save2file('tree.txt', line_type='ascii-em')
                self.showTree()

    def showTree(self):
        f = open('tree.txt', 'r')
        text = ""
        for i in range(10):
            contents = f.read()
            text += contents

        text = text
        txt = tk.Label(self,text=text,justify="left")
        txt.grid(columnspan = 6)
        # return txt
        f.close()
        # txt.pack(side = tk.BOTTOM)

    def _reset_option_menu(self, options, index=None):
        '''reset the values in the option menu

        if index is given, set the value of the menu to
        the option at the given index
        '''
        menu = self.om["menu"]
        menu.delete(0, "end")
        for string in options:
            menu.add_command(label=string,
                             command=lambda value=string:
                                  self.om_variable.set(value))

        if index is not None:
            self.om_variable.set(options[index])

    def use_age(self):
        '''Switch the option menu to display Age'''
        filepath = "/Users/ashara/Documents/Data/Scenario1_Top10CCS.csv"
        df = pd.read_csv(filepath)
        choices = list(set(df.AGE_GROUP.unique()))
        return choices

    def use_LOS(self):
        '''Switch the option menu to display LOS'''
        filepath = "/Users/ashara/Documents/Data/Scenario1_Top10CCS.csv"
        df = pd.read_csv(filepath)
        choices = list(set(df.LOS.unique()))
        return choices

    def use_DX(self):
        '''Switch the option menu to display Primary Dx'''
        filepath = "/Users/ashara/Documents/Data/Scenario1_Top10CCS.csv"
        df = pd.read_csv(filepath)
        choices = list(set(df.PRIMARY_DX.unique()))
        return choices

    def use_HAC(self):
        '''Switch the option menu to display HAC'''
        filepath = "/Users/ashara/Documents/Data/Scenario1_Top10CCS.csv"
        df = pd.read_csv(filepath)
        choices = list(set(df.DEVELOPED_SEPTICEMIA.unique()))
        return choices


if __name__ == "__main__":
    app = SampleApp()
    app.title("Show Rules Tree")
    app.mainloop()