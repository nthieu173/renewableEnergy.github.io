# Analysis of Renewable Energy Production in the US
Using machine learning techniques to analyze the significance of factors affecting renewable energy production in the US.

TODO:
Summary Figure
Determine time frame of analysis - data availability?
Are we even doing the analysis over time? 


## Introduction 

## Methods

### Data
Data on the production of renewable energy by state and the retail price of electricity ([renewable](https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_5_6_a) vs non-renewable) by state will be obtained from the US Energy Information Administration. In order to identify the factors that might affect the price and adoption of renewable energy in the US, data will be obtained from the following sources:

+ Geographical information from the National Oceanic and Atmospheric Administration:
    - [Average wind direction and speed](https://www.ncdc.noaa.gov/societal-impacts/wind/)
    - [Average solar radiation](https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/solar-radiation) (1991-2010)
    - [Waterway mileage](https://www.statista.com/statistics/187350/us-inland-waterway-mileage-2008/) and [reservoir size](https://waterdata.usgs.gov/nwis/current/?type=lake&group_key=state_cd&site_no_name_select=siteno)
    - [Temperature](https://www.ncdc.noaa.gov/temp-and-precip/us-maps/1/202007)
    - [Precipitation](https://www.ncdc.noaa.gov/temp-and-precip/us-maps/1/202007)
    - [Size of state](https://www.census.gov/geographies/reference-files/2010/geo/state-area.html) [//]: # (has water body data too)

+ Taxes
    - [Oil and gas production](https://www.ncsl.org/research/energy/oil-and-gas-severance-taxes.aspx)

+ Demographic information from the [Census Bureau](https://www.census.gov/quickfacts/fact/table/US/PST045219)
+ [Political affliation](https://www.pewforum.org/religious-landscape-study/compare/party-affiliation/by/state/)

### Unsupervised Learning
We will identify the factors that are the most relevant in our analysis with PCA and use (??) method to analyze how these factors affect the production of renewable energy in the US. 

### Supervised Learning
[//]: # (We could do something like predicting the energy price given certain information?)

## Results 

## Discussion

best outcome, what it would mean, what is next.....

## References
list containing at least three references, preferably peer reviewed