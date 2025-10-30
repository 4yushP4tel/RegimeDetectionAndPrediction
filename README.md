# RegimeDetectionAndPrediction
Detect, Predict Market Regimes for Tech and Energy sectors

## Regime Detection
This portion of the project aims to cluster market conditions into regimes
This process is done using PCA on log returns of assets in the sector, correlations,
log bid-ask spread and volumes,

This will be used to fit a multivariate Hidden Markov Model which will allow us 
to find transition matrices. Knowing the current market conditions, we will be able
to infer the current qualitative market regime.

## Back Testing and Stress Testing
The results of this regime modelling will be back tested using data between 2020-2025
with rolling windows (on weeks) to extensively find if the results on a weekly basis
made sense with the probablistic projected regimes.

Stress testing will be done during periods such as 2007-2008, 2019-2020, end of 2025
which would help model periods of low liquidity and market fear, extremely bearish markets
and extremely bullish markets in moments of extreme volatility. 




