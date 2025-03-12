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
        - county_state_land_area (pd.dataframe), with index: "County", and columns: "State", "Land_Area"
    '''

    df = pd.read_csv("data/land_area.csv")
    county_state = df["NAME"].str.split(', ', expand=True)
    county_state.columns = ["County", "State"]

    county_state_land_area = pd.concat([county_state, df["AREALAND"]], axis=1)
    county_state_land_area["County"] = county_state_land_area["County"].str.split(' ').str[0]
    county_state_land_area = county_state_land_area.rename(columns={"AREALAND": "Land_Area"})
    county_state_land_area["County"] = county_state_land_area["County"].str.strip()
    county_state_land_area = county_state_land_area.set_index("County")

    return county_state_land_area


    

def compute_state_infections_2020():
    '''
    Count the # of infections within each state in 2020

    Return:
        - county_state_infections (pd.dataframe), with index: "County", and columns: "State", "Infections"
    '''

    df = pd.read_csv("data/infection.csv")
    infections = df.loc[:, "1/22/20": "12/31/20"].sum(axis=1)

    county_state_infections = pd.concat([df["Admin2"], df["Province_State"], infections], axis=1)
    county_state_infections.columns = ["County", "State", "Infections"]
    county_state_infections["County"] = county_state_infections["County"].str.strip()
    county_state_infections = county_state_infections.set_index("County")

    return county_state_infections



def compute_state_population_2020():
    '''
    Count the # of infections within each state in 2020

    Return:
        - county_state_population (pd.dataframe), with index: "County", and columns: "State", "Population"
    '''

    df = pd.read_excel("data/population.xlsx")

    # .Autauga County, Alabama -- .Weston County, Wyoming
    county_state_combined = df.iloc[4: 3148, 0].to_frame()
    county_state_combined.columns = ["County_State"]
    county_state = county_state_combined["County_State"].str.split(", ", expand=True)
    county_state.columns = ["County", "State"]
    county_state["County"] = county_state["County"].str.split(' ').str[0].str[1:]

    population = df.iloc[4: 3148, 1]

    county_state_population = pd.concat([county_state, population], axis=1)
    county_state_population.columns = ["County", "State", "Population"]
    county_state_population = county_state_population.reset_index(drop=True)
    county_state_population["County"] = county_state_population["County"].str.strip()
    county_state_population = county_state_population.set_index("County")

    return county_state_population



def resolve_missing_county(county_state_land_area, county_state_infections, county_state_population):
    pass



def combine_county(county_state_land_area, county_state_infections, county_state_population):
    '''
    Combine the counties that belong to the same state together

    Parameters:
        - county_state_land_area (pd.dataframe): 
        - county_state_infections (pd.dataframe):
        - county_state_population (pd.dataframe):
    
    Return:
        - state_land_area (pd.dataframe):
        - state_infections (pd.dataframe):
        - state_population (pd.dataframe):
    '''

    pass



def compute_density_infection_rate(state_all_info):
    pass



def clean_data():
    county_state_land_area = compute_state_land_area()
    # county_state_infections = compute_state_infections_2020()
    # county_state_population = compute_state_population_2020()

    # resolve_missing_county(county_state_land_area, county_state_infections, county_state_population)
    # state_land_area, state_infections, state_population = combine_county(county_state_land_area, county_state_infections, county_state_population)
    # combine_county(county_state_land_area, county_state_infections, county_state_population)

    # density_infection_rate = compute_density_infection_rate(state_land_area, state_infections, state_population)

    # return density_infection_rate



if __name__ == "__main__":
    clean_data()
