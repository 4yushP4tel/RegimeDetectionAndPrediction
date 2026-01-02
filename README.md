# RegimeDetectionAndPrediction

Detect and Predict Market Regimes for the Tech sector using the XLK index

## Regime Detection

This part of the project identifies different market regimes in the tech sector.
The process involves:
- 	Computing log returns of sector assets, along with correlations, bid-ask spreads, and trading volumes.
-   Applying PCA to reduce dimensionality and capture the main factors driving market behavior.
-   Using these factors as input to a multivariate Hidden Markov Model (HMM), which estimates regime-dependent parameters and transition probabilities.

By fitting the HMM, we can:
-   Infer the current market regime given observed data.
-   Analyze transition dynamics between regimes, which can help anticipate future market conditions.