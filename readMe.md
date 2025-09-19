# American-style Put Options (Monte Carlo with Backward Induction)

This tool provides a simulation-based framework to price **American-style put options** using the **Monte Carlo method** combined with **backward induction (Longstaff–Schwartz)**. The implementation estimates the option value by simulating the underlying asset’s price paths and determining the optimal exercise strategy at each time step.

---

## Table of Contents
- [Launch App](#launch-app)
- [Preview](#preview)
- [Methodology](#methodology)
- [Features of the Code](#features-of-the-code)

---

## Launch App

[Open App](https://monte-carlo-american-put.streamlit.app/)

---

## Preview
<img width="1912" height="954" alt="msedge_D1ulgBzj3R" src="https://github.com/user-attachments/assets/fe7bdf6b-7155-42a1-99a8-3efe3233cf26" />

---

## Methodology

Pricing American options requires handling **early exercise**, which adds complexity compared to European options. The valuation here follows these steps.

1. **Simulating Asset Paths**  
   The asset price follows a geometric Brownian motion:

   ![equation](https://latex.codecogs.com/svg.latex?\color{white}S_{t+\Delta%20t}=S_t\exp\Big((r-\tfrac{\sigma^2}{2})\Delta%20t+\sigma\sqrt{\Delta%20t}\,Z\Big))

   where:

   - ![equation](https://latex.codecogs.com/svg.latex?\color{white}r) : Risk-free interest rate  
   - ![equation](https://latex.codecogs.com/svg.latex?\color{white}\sigma) : Volatility of the asset  
   - ![equation](https://latex.codecogs.com/svg.latex?\color{white}\Delta%20t=T/n_{\text{steps}}) : Time increment  
   - ![equation](https://latex.codecogs.com/svg.latex?\color{white}Z\sim\mathcal{N}(0,1)) : Standard normal random variable

2. **Payoff Calculation**  
   At each time step, the (put) payoff is:

   ![equation](https://latex.codecogs.com/svg.latex?\color{white}\text{Payoff}=\max(K-S_t,0))

   where ![equation](https://latex.codecogs.com/svg.latex?\color{white}K) is the strike price.

3. **Backward Induction**  
   Starting from the option’s final payoff at maturity \(T\), the code evaluates whether exercising the option is optimal at each step:

   - If the option is **in the money (ITM)**, calculate the immediate exercise value and the continuation value using regression:

     $$\text{Continuation Value} = \text{Expected Discounted Payoff}$$

   - Compare the two values to decide:

     $$V_t = \max(\text{Immediate Exercise Value},\ \text{Continuation Value})$$

4. **Regression for Continuation Value (LSM)**  
   The continuation value is estimated with a quadratic basis in ![equation](https://latex.codecogs.com/svg.latex?\color{white}S_t):

   ![equation](https://latex.codecogs.com/svg.latex?\color{white}\text{Continuation%20Value}\approx%20a_0+a_1S_t+a_2S_t^2)

   where ![equation](https://latex.codecogs.com/svg.latex?\color{white}a_0,a_1,a_2) are regression coefficients.

5. **Monte Carlo Estimation**  
   Averaging across simulated paths yields the American put price at inception:

   ![equation](https://latex.codecogs.com/svg.latex?\color{white}\text{Option%20Price}\approx\mathbb{E}[V_0])

---

## Features of the Code

- **Interactive inputs**  
  Spot price, strike, risk-free rate, volatility, time to maturity, number of simulations, and number of time steps.

- **Efficient implementation**  
  Vectorized GBM simulation and **Longstaff–Schwartz** regression (quadratic basis) for continuation values.

- **Robust early-exercise handling**  
  Exercise decision made only for in-the-money paths; out-of-the-money paths continue with discounted value.

