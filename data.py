import pandas as pd
import numpy as np


def remove_comma():
    '''
    Remove the extra comma at the end of each line, remove the second invalid line

    USE THIS FUNCTION ONLY ONCE
    '''

    path = "data/land_area.csv"
    with open(path, "r") as land_file:
        lines = land_file.readlines()
    
    lines = [line.strip()[:-1] + "\n" for line in lines]

    with open(path, "w") as land_file:
        land_file.writelines(lines)



def compute_state_land_area():
    '''
    Compute the land area of each state

    Return:
        - county_state_land_area (pd.dataframe), with index: "County_State", and column: "Land_Area"
    '''

    df = pd.read_csv("data/land_area.csv")

    county_state_land_area = pd.concat([df["NAME"], df["AREALAND"]], axis=1)
    county_state_land_area.columns = ["County_State", "Land_Area"]
    county_state_land_area["County_State"] = county_state_land_area["County_State"].str.replace(" County", "").str.replace(" Parish", "").str.replace(" Municipio", "").str.replace("city", "City")


    # drop non-int values (if any)
    county_state_land_area = county_state_land_area[county_state_land_area["Land_Area"].apply(lambda x: isinstance(x, int))]      # during operations pd may change it into int?

    county_state_land_area.set_index("County_State", inplace=True)

    # double check 
    county_state_land_area.index = county_state_land_area.index.str.strip()
    assert county_state_land_area["Land_Area"].dtype == int, "compute_state_land_area: not np.int64"
    # assert county_state_land_area.index.dtype == str, "compute_state_land_area: not str"

    # print(county_state_land_area)

    return county_state_land_area


    

def compute_state_infections_2020():
    '''
    Count the # of infections within each state in 2020

    Return:
        - county_state_infections (pd.dataframe), with index: "County_State", and column: "Infections"
    '''

    df = pd.read_csv("data/infection.csv")
    infections = df.loc[:, "1/22/20": "12/31/20"].sum(axis=1)

    county_state_infections = pd.concat([df["Admin2"], df["Province_State"], infections], axis=1)
    county_state_infections.columns = ["County", "State", "Infections"]
    county_state_infections["County_State"] = county_state_infections["County"] + ", " + county_state_infections["State"]
    county_state_infections.drop(columns=["County", "State"], inplace=True)

    # drop non-int values (if any)
    county_state_infections = county_state_infections[county_state_infections["Infections"].apply(lambda x: isinstance(x, int))]

    county_state_infections.set_index("County_State", inplace=True)

    # double check
    county_state_infections.index = county_state_infections.index.str.strip()
    assert county_state_infections["Infections"].dtype == int, "compute_state_infections_2020: not np.int64"
    # assert county_state_infections.index.dtype == str, "compute_state_land_area: not str"

    # print(county_state_infections)

    return county_state_infections



def compute_state_population_2020():
    '''
    Count the # of infections within each state in 2020

    Return:
        - county_state_population (pd.dataframe), with index: "County_State", and column: "Population"
    '''

    df = pd.read_excel("data/population.xlsx")

    # .Autauga County, Alabama -- .Weston County, Wyoming
    county_state_population = pd.concat([df.iloc[4: 3148, 0], df.iloc[4: 3148, 1]], axis=1)
    county_state_population.reset_index(drop=True, inplace=True)
    county_state_population.columns = ["County_State", "Population"]
    county_state_population["County_State"] = county_state_population["County_State"].str[1:].str.replace(" County", "").str.replace("city", "City")

    # drop non-int values (if any)
    county_state_population = county_state_population[county_state_population["Population"].apply(lambda x: isinstance(x, int))]
    county_state_population["Population"] = county_state_population["Population"].astype(int)

    county_state_population.set_index("County_State", inplace=True)

    # double check
    county_state_population.index = county_state_population.index.str.strip()
    assert county_state_population["Population"].dtype == int, "compute_state_population_2020:  Numerical values are not in integers"

    # print(county_state_population)

    return county_state_population



def resolve_missing_county(county_state_land_area, county_state_infections, county_state_population):
    '''
    Only want to analyze the county present in all three dataframes, and since after that they'll share the same counties, we can concat three dataframes together

    Parameters:
        - county_state_land_area (pd.dataframe), with index: "County_State", and column: "Land_Area"
        - county_state_infections (pd.dataframe), with index: "County_State", and column: "Infections"
        - county_state_population (pd.dataframe), with index: "County_State", and column: "Population"

    Return:
        - county_state_info (pd.dataframe), with index: "County_State", and columns: "Land_Area", "Infections", "Population"

    '''

    common_county_state = county_state_land_area.index.intersection(county_state_infections.index).intersection(county_state_population.index)
    
    county_state_land_area = county_state_land_area.loc[common_county_state]
    county_state_infections = county_state_infections.loc[common_county_state]
    county_state_population = county_state_population.loc[common_county_state]

    # print(county_state_land_area.index.value_counts())
    assert len(county_state_land_area.index) == len(county_state_infections.index) == len(county_state_population.index)

    # sort based on county-state pair for consistency
    county_state_land_area.sort_index(inplace=True)
    county_state_infections.sort_index(inplace=True)
    county_state_population.sort_index(inplace=True)

    county_state_info = pd.concat([county_state_land_area, county_state_infections, county_state_population], axis=1)

    # print(county_state_info)

    return county_state_info




def combine_county(county_state_info):
    '''
    Combine the counties that belong to the same state together

    Parameter:
        - county_state_info (pd.dataframe), with index: "County_State", and columns: "Land_Area", "Infections", "Population"
    
    Return:
        - state_info (pd.dataframe), with index: "State", and columns: "Land_Area", "Infections", "Population"
    '''

    county_state_info.index = county_state_info.index.str.split(", ").str[-1].str.strip()
    state_info = county_state_info.sort_index()
    
    state_info = state_info.groupby(level=0).sum()
    # print(state_info)

    return state_info



def compute_density_infection_rate(state_info):
    '''
    Compute the population density and infection rate for each state

    Parameter:
        - state_info (pd.dataframe), with index: "State", and columns: "Land_Area", "Infections", "Population"

    Return:
        - state_density_rate (pd.dataframe), with index: "State", and columns: "Density", "Rate"
    '''

    state_density_rate = pd.DataFrame()

    state_density_rate["Density"] = state_info["Population"] / state_info["Land_Area"]
    state_density_rate["Rate"] = state_info["Infections"] / state_info["Population"]

    # print(state_density_rate)

    return state_density_rate



def clean_data():
    county_state_land_area = compute_state_land_area()
    county_state_infections = compute_state_infections_2020()
    county_state_population = compute_state_population_2020()

    county_state_info = resolve_missing_county(county_state_land_area, county_state_infections, county_state_population)
    state_info = combine_county(county_state_info)

    state_density_rate = compute_density_infection_rate(state_info)

    return state_density_rate



if __name__ == "__main__":
    clean_data()
