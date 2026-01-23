# ![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)


### Global Fertility Trends: An Exploratory Data Analysis and Interactive Visualisation


### Introduction
This project investigates global fertility patterns, with a particular focus on how birth rates have changed across countries and over time. Fertility rate, defined as the average number of births per woman, is a key demographic indicator that reflects social, economic, and cultural conditions. Understanding long term fertility trends provides insight into population dynamics, development trajectories, and global demographic transitions.
The project combines exploratory data analysis (EDA), statistical modelling, and interactive visualisation through a Streamlit web application.

### Data Sources
Two primary datasets were used:
- World Bank Fertility Rate Data (1960–2023)
Source: https://data.worldbank.org/indicator/SP.DYN.TFRT.IN
This dataset provides annual fertility rates for countries worldwide.
- World Bank Country Metadata
Source: https://api.worldbank.org/v2/country?format=json&per_page=400
This dataset includes regional classifications, socioeconomic indicators, and geographic metadata used for mapping and contextual analysis.

### Data Preparation and Cleaning
The raw CSV file obtained from the World Bank contained four initial rows of metadata, which prevented correct parsing. These rows were removed using:
pd.read_csv("API_SP.DYN.TFRT.IN_DS2_en_csv_v2_230.csv"", skiprows=4)


### Subsequent cleaning steps included:
- Removing rows with missing fertility values
- Inspecting column types and unique values
- Assessing the distribution of missing data
- Printing sample rows to understand the dataset structure
These steps ensured the dataset was suitable for analysis and visualisation.

### Exploratory Data Analysis
The EDA process focused on identifying temporal and geographic patterns in fertility rates.
Line Graph Analysis
Interactive line charts were developed to compare fertility trends across countries. These visualisations highlight long‑term declines in most regions, as well as notable exceptions and regional variations.

<img width="1010" height="547" alt="Lines" src="https://github.com/user-attachments/assets/a943fd17-cfb6-40ce-b6de-be5bd0371b16" />


### Distribution Analysis
A distribution plot was created to examine the global spread of fertility rates. The distribution exhibited two distinct peaks, suggesting heterogeneous demographic profiles across countries.
Further optimisation is required to refine axis labels and improve interpretability.

<img width="1789" height="8628" alt="Distribution" src="https://github.com/user-attachments/assets/617795d5-b188-495d-b4b2-3ffa4961b7d7" />



### Additional Visualisations
Additional plots and analyses are available in the Jupyter Notebook and the project’s image directory.

### Statistical Modelling
A linear regression model was initially implemented to estimate fertility trends and generate simple projections. While this approach provided a baseline understanding, linear models are not well‑suited to demographic processes, which are inherently non‑linear.
Future iterations will incorporate more appropriate modelling techniques, such as polynomial regression or time‑series models, to improve predictive accuracy.

<img width="1788" height="690" alt="Regression" src="https://github.com/user-attachments/assets/449d26c0-6f16-4323-8491-2791d109f3b9" />


### Application Development
All analytical components were consolidated into a Python script and integrated into a Streamlit application. The app enables users to:
- Compare fertility trends across countries
- Explore long‑term global patterns
- Interact with dynamic charts and filters
- View a global choropleth map of fertility rates
The primary development focus was on creating a clear and accessible user interface. Although several areas remain open for improvement, the application was successfully deployed.
Live Application:
https://globalbirthrate.streamlit.app/

### Business Requirements
The application is designed to meet the following business requirements:
- Analyse long‑term fertility trends to support demographic planning and policy development.
- Enable cross‑country and regional comparisons to identify demographic disparities and benchmark performance.
- Provide geographic visualisation of fertility patterns to support high‑level strategic decision‑making.
- Offer baseline forecasting capabilities to assist with scenario planning and resource allocation.
- Deliver an accessible, interactive analytical tool suitable for non‑technical stakeholders.
- Support evidence‑based evaluation of demographic and socioeconomic factors influencing fertility rates.

### Future Work
Planned enhancements include:
- Allowing users to toggle between slope and percentage trend metrics
- Implementing non‑linear regression models for more realistic projections
- Incorporating additional variables (e.g., climate, conflict, migration) to contextualise fertility trends
- Improving labelling and clarity in distribution plots
- Refining UI components for greater usability

### Jupyter Notebook
The notebook contains exploratory work, including intermediate steps and duplicated code segments. These were intentionally retained to document the full analytical workflow.

###GDPR

As all data was publicly available and anomnays no privacy concerns. 

###Aknowledgements 

First of all I would like to thank my tutor at the Code Insitute for having patients and supplying us with everything we needed to complete the project. 

I would also like to thank the World Bank for providing the data that formed the foundation of this work.

Finally, I want to acknowledge Copilot, which was used during the development of this project.











