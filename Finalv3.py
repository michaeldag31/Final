"""
Name: Michael D'Agostino
CS230: Section SN2
Data: "Colleges and Universities in the United States"
URL: *FILL IN LATER*

Description:

This program provides a variety of ways to examine the statistics of location data for U.S. colleges and universities.
A map is available for your use, as you're able to navigate between states and zoom in as desired.
In addition, a bar chart is available to show you the number of schools that each state has.
You may chose the states that you are viewing in the bar chart, and an average count of schools in a state in the U.S. is also provided.
"""


import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk
import csv


#gets map data
def get_data(filename):
    data = []

    firstLine = True #going line by line, don't want the header, skips the first row
    with open(filename, "r", errors="ignore") as file_open:
        line = csv.reader(file_open)
        for row in line:
            if firstLine:
                firstLine = False
            else:
                data.append([float(row[13]), float(row[14]), row[4], row[7]]) #creates a 2-d matrix, list of list
    file_open.close()
    return data


#puts data into state map
def map_state(data, state):
    map_data = []
    for entry in data:
        if entry[3] == state: #consolidates data further, gets the points for the states selected
            map_data.append(entry)
    df = pd.DataFrame(map_data, columns=['lat', 'lon', 'name','state']) #puts data into a dataframe
    st.dataframe(df) #shows the dataframe
    tool_tip = {"html": "University Name:<br/> <b>{name}</b> ",
            "style": { "backgroundColor": "steelblue",
                        "color": "white"}} #used class examples
    view_state = pdk.ViewState(latitude=df["lat"].median(), longitude=df["lon"].median(), zoom=8, pitch=0) #pydeck sets up the state view based on the datafram
    layer = pdk.Layer('ScatterplotLayer', data= df, get_position= '[lon, lat]', get_radius= 800, get_color= [255,0,0], pickable= True, marker= 50) #layers set up from dataframe


    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=[layer],
        tooltip= tool_tip
    ) #establishes the map based on above factors

    st.pydeck_chart(map) #puts map on streamlit

#gets a dictionary with the frequencies of each state - interacts with a dictionary
def state_freq(data):
    x = data.sort_values(by=['STATE']) #sort, pandas feature, more efficient with all states in order
    states = x['STATE'].tolist() #gets all the states in a list - interacts with a list. Also something using from outside of class
    consolidate_states = {}
    for state in states:
        if state not in consolidate_states:
            consolidate_states[state] = 1
        else:
            consolidate_states[state] += 1 #making a dictionary of each state and how many occurences it sees
    return consolidate_states

#bar graph - function with at least two parameters that returns a value
def schools_per_state(state_count, location, color='blue'):
    average = sum(state_count.values()) / len(state_count)
    x_axis = ["State Average"]
    y_axis = [average]
    for state in location:
        x_axis.append(state)
        y_axis.append(state_count[state])

    plt.bar(x_axis,y_axis,width=0.5, color=color) #plotting
    plt.xticks(rotation=45, fontsize=7)
    plt.xlabel("State")
    plt.ylabel("Count")
    plt.title("School Count Comparison by State")
    return plt


#main function that doesn't return anything
def main():
    st.write("Michael D'Agostino Final Project")
    list_of_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    state_choice = st.sidebar.selectbox('Select your state to view schools on the map', list_of_states)
    state_map_data = get_data('Postsecondary_School_Locations_-_Current.csv') #all the data
    st.write("Map of schools")
    map_state(state_map_data, state_choice) #data gets into the map
    all_data = pd.read_csv('Postsecondary_School_Locations_-_Current.csv') #entire csv as a dataframe
    count_of_each_state = state_freq(all_data)
    multiple_state_choice = st.sidebar.multiselect("Select the states that you want displayed in the bar chart", list_of_states)
    st.write("Graph of the number of schools in each state, compared to the average state's school count")
    colors=["blue", "red", "green", "yellow", "orange", "cyan", "black", "grey"]
    selected = st.sidebar.radio('Map Color:', colors)
    st.pyplot(schools_per_state(count_of_each_state, multiple_state_choice, selected)) #give dataframe to function, then graphing the function

main()

