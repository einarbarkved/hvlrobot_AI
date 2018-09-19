import numpy as np
import pandas as pd
import os

file_name = 'training_data.npy'
training_data = list(np.load(file_name))



df = pd.DataFrame(training_data)
print(df.head())