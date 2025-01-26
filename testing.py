import numpy as np
import pandas as pd
from Sideify import testvector

array = [22,66,44,99,11,33,55]
array = np.array(array)

indices = np.arange(array.size)

input = np.column_stack((indices,array))
#print(input)

#rotated = testvector.rotation(input, 49)
#print(rotated)
#print("----")

def reduce_frames(input, transformed, interval):
    sortedxaxis = np.argsort(transformed[:,0])
    transformed = transformed[sortedxaxis]

    df = pd.DataFrame(transformed, columns=["indices","values"])
    df["block"] = (df.index // interval)
    print("----")
    print(df)
    dfcalculated = pd.DataFrame(columns=["indices","values"])
    dfcalculated["indices"] = (df.groupby("block")["indices"].mean())
    dfcalculated["values"] = (df.groupby("block")["values"].sum())
    print(dfcalculated)
    reduced_array = np.column_stack((dfcalculated["indices"], dfcalculated["values"]))

    return reduced_array

#reduce_frames(input, rotated, 3)

