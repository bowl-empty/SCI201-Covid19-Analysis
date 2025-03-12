import pandas as pd
import numpy as np
from data_old import clean_data



def linear_regression(density_infection_rate):
    '''
    Perform linear regression on the data

    Parameter:
        - density_infection_rate (pd.dataframe):
                        Population_Density     Infection_Rate
            State_Name          ...                 ...
                ...
            State_Name          ...                 ...
    '''

    pass



if __name__ == "__main__":
    density_infection_rate = clean_data()
    linear_regression(density_infection_rate)

    pass
