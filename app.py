import streamlit as st
import numpy as np
import pandas as pd
import math
from numpy.polynomial.polynomial import polyfit, polyval


def monte_carlo_american_put(S0, K, r, sigma, T, n_sim=10000, n_steps=50):
    dt = T / n_steps
    discount = math.exp(-r * dt)

    # Simulate paths
    S = np.zeros((n_sim, n_steps + 1))
    S[:, 0] = S0
    for i in range(1, n_steps + 1):
        z = np.random.randn(n_sim)
        S[:, i] = S[:, i - 1] * \
            np.exp((r - 0.5 * sigma**2) * dt + sigma * math.sqrt(dt) * z)

    payoff = np.maximum(K - S, 0.0)
    V = payoff[:, -1]

    # Backward induction
    for t in range(n_steps - 1, 0, -1):
        itm = payoff[:, t] > 0
        X = S[itm, t]
        Y = V[itm] * discount
        if len(X) > 0:
            coeffs = polyfit(X, Y, 2)
            continuation = polyval(X, coeffs)
            exercise = payoff[itm, t]
            V[itm] = np.where(exercise > continuation,
                              exercise, V[itm] * discount)
        else:
            V = V * discount

    return np.mean(V) * discount


st.markdown("<h2 style='font-size:24px;'>American Option Pricing via Monte Carlo</h2>",
            unsafe_allow_html=True)
st.write("Calculate American put option prices using Monte Carlo simulation.")

# user input
S0 = st.number_input("Spot Price (S0)", min_value=1.0, value=40.0, step=1.0)
K = st.number_input("Strike Price (K)", min_value=1.0, value=40.0, step=1.0)
r = st.number_input("Risk-Free Rate (r)", min_value=0.0,
                    max_value=1.0, value=0.06, step=0.01)
sigma = st.number_input("Volatility (sigma)", min_value=0.01,
                        max_value=1.0, value=0.2, step=0.01)
T = st.number_input("Time to Maturity (T)", min_value=0.01,
                    max_value=10.0, value=1.0, step=0.1)
n_sim = st.number_input("Number of Simulations", min_value=1000,
                        max_value=100000, value=10000, step=1000)
n_steps = st.number_input("Number of Time Steps",
                          min_value=10, max_value=100, value=50, step=10)


if st.button("Calculate Price"):
    try:
        price = monte_carlo_american_put(
            S0, K, r, sigma, T, int(n_sim), int(n_steps))
        st.subheader(f"Calculated American Put Option Price: {price:.4f}")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
