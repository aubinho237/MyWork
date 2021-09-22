from logging import log
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import streamlit.components.v1 as components  
import os






def mon_decorateur(fonction):
    def mesure_execution():
        start_time = time.time()
        print('start_time: %.3f' % (start_time))
        result = fonction()
        stop_time = time.time()
        print('stop_time: %.3f' % (stop_time))
        total = stop_time - start_time
        print("temps d'execution: %.3f" % (total))
        return result
    return mesure_execution


st.title('LAB2_part3 Aubain NDAMKOU')

components.html("<html><body><h1>This is my static component with streamlit</h1></body></html>", width=200, height=200)

components.html("<html><body>We can use this script to handle visualisation</h1></body></html>", width=100, height=150)


_RELEASE = False



if not _RELEASE:
    _component_func = components.declare_component(
"my_component",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("my_component", path=build_dir)



def my_component(name, key=None):
 
    component_value = _component_func(name=name, key=key, default=0)
    return component_value


if not _RELEASE:
    import streamlit as st

    st.subheader("Bi directionnal component")

    num_clicks = my_component("let's get it")
    st.markdown("You've clicked %s times!" % int(num_clicks))

    st.markdown("---")
    st.subheader("Component with variable args")


    name_input = st.text_input("Enter a name", value="Streamlit")
    num_clicks = my_component(name_input, key="foo")
    st.markdown("You've clicked %s times!" % int(num_clicks))




# Streamlit native slider
v = st.slider("Use this as a slide button", 0, 100)
st.write(v)



@mon_decorateur
def chargement():
    latest_iteration = st.empty()
    bar = st.progress(0)
    for i in range(100):
        latest_iteration.text('Chargement des modèles')
        bar.progress(i + 1)
        time.sleep(0.1)
    'Chargement terminé'
    return bar
chargement()



def read_csv(file):
    df= pd.read_csv(file)
    return df
file1= "uber-raw-data-apr14.csv"
df=read_csv(file1)

st.write(df.head(10))
df["Date/Time"]= pd.to_datetime(df["Date/Time"])

def get_dom(dt):
    return dt.day 



def get_weekday(dt): 
    return dt.weekday() 


def optimise():
    df=read_csv(file1)
    st.write("Optimasation du dataset")
    st.write(df.head(10))
    df.describe()
    return df

optimise()


@mon_decorateur
def affichage_frequence():
    st.write("Affichage des fréquences d'apparition des variables")
    df['dom'] = df['Date/Time'].map(get_dom)
    plt.hist(df["dom"],bins = 30, rwidth=0.8, range=(0.5,30.5))
    plt.title('Frequency')
    st.pyplot()
    return True

affichage_frequence()

def count_rows(rows): 
     return len(rows)
by_date = df.groupby('dom').apply(count_rows)
plt.plot(by_date)


def get_hour(dt): 
    return dt.hour
df['hour']= df['Date/Time'].map(get_hour)

@mon_decorateur
def add_select_box():
    st.write("Choisissez une heure")
    values = df['Date/Time'].drop_duplicates()
    date_to_filter = st.selectbox('Choisir date', values)
    st.subheader(f'Données de chaque trip à {date_to_filter}')
    st.write(df[df['Date/Time'] == date_to_filter])
    return values

add_select_box()

@mon_decorateur
def frequency_date():
    plt.figure(figsize = (30, 15))
    plt.hist(df["hour"],bins=24,range=(0.5,24))
    plt.bar(range(1, 31), by_date.sort_values())
    plt.xticks(range(1, 31), by_date.sort_values().index)
    plt.xlabel('Date du mois')
    plt.ylabel('Frequence')
    plt.title('Fréquency')
    st.pyplot()
    return True

frequency_date()

@mon_decorateur
def frequency_weekday():
    plt.figure(figsize = (30, 15))
    df['weekday']= df['Date/Time'].map(get_weekday)
    plt.hist(df["weekday"],bins=7,range = (-.5,6.5), rwidth=0.8)
    plt.xlabel('Day of the week')
    plt.ylabel('Frequency')
    plt.title('Fréquency')
    st.pyplot()
    return True

frequency_weekday()




@mon_decorateur
def frequency_week():
    plt.figure(figsize = (30, 15))
    plt.hist(df.weekday, bins = 7, rwidth = 0.8, range = (-.5, 6.5))
    plt.xlabel('Jour de la semaine')
    plt.ylabel('Frequence')
    plt.title('Frequence par Heure - Uber - April 2014')
    plt.xticks(np.arange(7), 'Mon Tue Wed Thu Fri Sat Sun'.split())
    st.pyplot()
    return True

frequency_week()

@mon_decorateur
def logi_lati():
    plt.figure(figsize =(20,20), dpi=80)
    plt.scatter(df["Lat"],df['Lon'])
    plt.title('Longitude et Latitude')
    st.pyplot()
    return True

logi_lati()

def plot_lat():
    plt.figure(figsize = (20, 20))
    plt.plot(df.Lon, df.Lat, '.', ms = 2, alpha = .5)
    plt.xlim(-74.2, -73.7)
    plt.ylim(40.7, 41)
    plt.grid()
    st.pyplot()
    return True

plot_lat()


st.title ("Utilisation du Data NY TRIP 2015")
file2 = "ny-trips-data.csv"
ds= read_csv(file2)

