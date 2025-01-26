import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

deg = 90
theta = deg * (np.pi)/180

x = np.linspace(0,2*np.pi,16)
testsin = np.sin(x)
originalsin = np.column_stack((x,testsin)) #stacks (x,y)

def rotation(input, deg):
    theta = deg * (np.pi)/180 #convert input deg to rad, since all internal work done in rad

    R = np.array([[np.cos(theta), -np.sin(theta)],
                [np.sin(theta), np.cos(theta)]])

    transformed = np.dot(input, R.T) #MATRIX MUL
    return transformed


interval = 2
input = originalsin
transformed = rotation(input,deg)
#print(input)
#print("----")
#print(transformed)

def reduce_frames(input, transformed, interval):
    sortedxaxis = np.argsort(transformed[:,1]) #sort by low-->high y values, since this is 90 deg up. what to do if at say 37 deg? maybe just put an if statement for past 45deg
    transformed = transformed[sortedxaxis]

    df = pd.DataFrame(transformed, columns=["indices","values"])
    df["block"] = (df.index // interval)
    #print("----")
    #print(df)
    dfcalculated = pd.DataFrame(columns=["indices","values"])
    dfcalculated["indices"] = (df.groupby("block")["indices"].mean())
    dfcalculated["values"] = (df.groupby("block")["values"].sum())
    dfcalculated = dfcalculated.sort_values(by="indices")
    #print(dfcalculated)
    reduced_array = np.column_stack((dfcalculated["indices"], dfcalculated["values"]))

    return reduced_array


reduced_array = reduce_frames(input, transformed, interval)
#print("----")
#print(reduced_array)
def show_plots(input, transformed, extra):

    plt.scatter(input[:, 0], input[:, 1])
    plt.scatter(transformed[:, 0], transformed[:, 1])
    plt.scatter(extra[:, 0], extra[:, 1])
    plt.show()

#show_plots(input,reduced_array, transformed)