import matplotlib.pyplot as plt
import numpy as np

#Scenario 1
# x = [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]#Support Threshold. Confidence is kept as 0.
# # y1 = [14.604,8.164,6.894,6.293,6.175,5.877,6.038,4.188,3.18,3.247] #Our Algorithm
# # y2=[77.551,42.094,25.587,21.072,17.339,16.401,15.851,10.382,7.708,7.708] #Original Apriori

#Scenario 2
x = [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1]#Support Threshold. Confidence is kept as 0.
y1 = [30.908,27.36,24.676,24.229,23.904,24.041,23.517,23.365,23.605,23.482] #Our Algorithm
y2 = [144.327,61.377,28.954,25.454,24.417,24.886,23.71,23.752,24.149,23.477]#Original Apriori
fig = plt.figure()
fig.show()
ax = fig.add_subplot(111)

ax.plot(x,y1,c='g',marker=(8,2,0),ls='--',label='Our Algorithm')
ax.plot(x,y2,c='r',marker="v",ls='--', label='Original Apriori')

plt.xlabel("Support Threshold with Confidence as 0")
plt.ylabel("Time in Seconds")
plt.xticks(x)
plt.legend(loc=1)
plt.draw()
plt.show()