# ![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

### Global Fertility Trends 

### Introduction & Motivation

In this project I decided to look into global population trends. I wanted to see how birth rates have changed across time and location. 

### Data Sources 

This project uses two data sets

https://data.worldbank.org/indicator/SP.DYN.TFRT.IN - Data from this page includes global fertility rates (births per woman) from 1960 to 2023

https://api.worldbank.org/v2/country?format=json&per_page=400 - This includes social econimc, and regional map data. 

### Overview 

- The project includes an interactive streamlit app that is able to compare contries birth rates across time.
- Explore long term trends
- Visulise global patterns on an interacitve map
- Interact with charts and filters

It's desighned for anyone interested in demodraphic changes. 

### App 
Acess here - https://globalbirthrate.streamlit.app/ 

### EDA

The raw .csv from data.worldbank.org/indicator/SP.DYN.TFRT.IN was initally hard to read and I kept getting errors, co-pilot was used to help read the csv. The problem was that the first 4 rows contained meta data from the world bank. 

<img width="975" height="43" alt="Screenshot 2026-01-23 120927" src="https://github.com/user-attachments/assets/41480a8d-2c85-447f-aa58-241d4baf0cfa" />

A simple - skiprows=4) fixed the errors. 

All rows with NaN fertility rates were dropped 

The info was then checked 

<class 'pandas.core.frame.DataFrame'>
Index: 16928 entries, 0 to 17023
Data columns (total 5 columns):
 #   Column          Non-Null Count  Dtype  
---  ------          --------------  -----  
 0   Country Name    16928 non-null  object 
 1   Country Code    16928 non-null  object 
 2   Indicator Name  16928 non-null  object 
 3   Year            16928 non-null  int32  
 4   FertilityRate   16928 non-null  float64
dtypes: float64(1), int32(1), object(3)
memory usage: 727.4+ KB
None

The first 20 lines were then printed to get a better understanding of the raw data

Then checked the unique values per column  

Checked number of NaN values per column

Then a list of data types that are numeric

This was my way to get a better understanding of the data and how to use it. 

### Visulizations 

Co-pilot was used throughout this process for optimisation of graphs. 

<img width="1010" height="547" alt="Lines" src="https://github.com/user-attachments/assets/059a229d-aaa3-4746-b4b3-6aecf3c1a8d9" />

