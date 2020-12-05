![Summary figure](./images/infographic.svg)

# [Proposal](./proposal.md)

Climate change caused by human emission of greenhouse gas is an ongoing crisis that has and will continue to be a major part of our lives. It is clear that we must switch renewable sources of energy sooner rather than later to reverse this trend.

Current applications of machine learning techniques to renewable energy is mostly be limited to local prediction or optimization of renewable energy production and not on answering these important holistic questions. While forecasting wind power or solar power are doubtlessly important pieces of information in a fully renewable future which can help to ensure a sustained supply of energy, answers to holistic questions are much more import to policymakers and investors who shape the development of renewable energy in their local states.

We will answer these holistic questions by using machine learning techniques performed on data from the Energy and Information Administration (EIA) and other sources of geographical, demographic and economic data.

The full proposal can be read [here](./proposal.md).

# [Data](./data.md)

Since we are interested in the adoption of renewable energy by states over time, we collected the following data from 1998 - 2016:
- Geographical:
    + Average Annual Direct Normal Irradiance (DNI)
    + Average Annual Precipitation
    + Average Annual Snowfall
    + Average Annual Temperature
    + Average Annual Windspeed
    + Total State Area
- Economic:
    + Annual Gross Domestic Product (GDP) in units of millions of $USD.
    + Annual Revenue of Electricity Providers
    + Annual Subsidies towards energy providers and products, in units of millions of $USD.
    + Average Electricity Price
    + Prime Supplier of Residual Oil: the supply for heavier oil and is the primary fuel for oil power plants.
- Fossil Fuel Usage and Renewable Energy Production:
    + Total Coal Consumption
    + Total Natural Gas Consumption
    + Hydroelectricity Capacity Potential
    + Hydroelectricity Generation Potential
    + Electricity Generated from Coal
    + Electricity Generated from Biomass
    + Electricity Generated from Geothermal
    + Electricity Generated from Hydroelectricity
    + Electricity Generated from Natural Gas
    + Electricity Generated from Other Renewable Sources
    + Electricity Generated from Other Gases
    + Electricity Generated from Petroleum
    + Electricity Generated from Pump Storage
    + Electricity Generated from Solar
    + Electricity Generated from Wind
    + Electricity Generated from Wood
    + Percentage of Renewable Energy (Derived)

Information about data collection and preproccessing can be found [here](./data.md).

# [Unsupervised Learning](./unsupervised.md)

Using unsupervised learning, we aim to answer the questions:
- Are states with similar (absolute and/or relative) renewable energy production similar in other features?
- Which features most strongly impact renewable energy production in states?
- Are states with low renewable energy production less green because they are fettered by geographical limitations?

To answer these questions, we will use:
- Principle Component Analysis (PCA)
- K-Means
- Gaussian Mixture Modelling (GMM)

Our results along with the full report can be read [here](./unsupervised.md).

# [Supervised Learning](./supervised.md)

A key question that we asked ourselves is: are we able to predict the price of electricity in a state accurately using the dataset that we had. Using supervised learning, we aim to create a machine learning model that predicts the price of electricity in a state based off the features that we collected earlier. To guage the accuracy of our model, we calculated the mean squared error for the predictions of our model on the unseen data from 2017 to 2019. 

Our results along with the full report can be read [here](./supervised.md).