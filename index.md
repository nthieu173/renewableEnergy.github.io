![Summary figure](./images/infographic.svg)

# [Proposal](./proposal.md)

Climate change caused by human emission of greenhouse gas is an ongoing crisis that has and will continue to be a major part of our lives. It is clear that we must switch renewable sources of energy sooner rather than later to reverse this trend.

Current applications of machine learning techniques to renewable energy is mostly be limited to local prediction or optimization of renewable energy production and not on answering these important holistic questions. While forecasting wind power or solar power are doubtlessly important pieces of information in a fully renewable future which can help to ensure a sustained supply of energy, answers to holistic questions are much more import to policymakers and investors who shape the development of renewable energy in their local states.

We will answer these holistic questions by using machine learning techniques performed on data from the Energy and Information Administration (EIA) and other sources of geographical, demographic and economic data.

The full proposal can be read [here](./proposal.md).

# Data

Since we are interested in the adoption of renewable energy by states over time, we collected the following data from 1998 - 2016:
- Geographical:
    1. Average Annual Direct Normal Irradiance (DNI)
    2. Average Annual Precipitation
    3. Average Annual Snowfall
    4. Average Annual Temperature
    5. Average Annual Windspeed
    6. Total State Area
- Economic:
    7. Annual Gross Domestic Product (GDP)
    8. Annual Revenue of Electricity Providers
    9. Annual Subsidies (?)
    10. Average Electricity Price
    11. Prime Supplier of Residual Oil (?)
- Fossil Fuel Usage and Renewable Energy Production:
    12. Total Coal Consumption
    13. Total Natural Gas Consumption
    14. Hydroelectricity Capacity Potential
    15. Hydroelectricity Generation Potential
    16. Electricity Generated from Biomass
    17. Electricity Generated from Geothermal
    18. Electricity Generated from Hydroelectricity
    19. Electricity Generated from Natural Gas
    20. Electricity Generated from Other Renewable Sources
    21. Electricity Generated from Other Gases
    22. Electricity Generated from Petroleum
    23. Electricity Generated from Pump Storage
    24. Electricity Generated from Solar
    25. Electricity Generated from Wind
    26. Electricity Generated from Wood
    27. Percentage of Renewable Energy (Derived)

The collected data is organized in the following format:

| State | Year | feature_1 | feature_2 | ... | feature_n |
|-------|------|-----------|-----------|-----|-----------|


# [Unsupervised Learning](./unsupervised.md)

Using unsupervised learning, we aim to answer the questions:
- Are states with similar (absolute and/or relative) renewable energy production similar in other features?
- Which features most strongly impact renewable energy production in states?

To answer these questions, we will use:
- Principle Component Analysis (PCA)
- K-Means
- Gaussian Mixture Modelling (GMM)

Our results along with the full report can be read [here](./unsupervised.md).