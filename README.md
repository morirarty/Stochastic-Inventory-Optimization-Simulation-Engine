# 📦 Stochastic Inventory Optimization & Simulation Engine
### Continuous Review (Q, R) Policy under Poisson Demand for Supply Chain Resilience

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![NumPy](https://img.shields.io/badge/NumPy-Scientific-lightblue?logo=numpy)
![SciPy](https://img.shields.io/badge/SciPy-Optimization-blue?logo=scipy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📌 Project Overview

This repository features an advanced **Operations Research (OR)** and **Prescriptive Analytics** tool designed to solve the classical corporate dilemma: minimizing warehouse carrying costs while completely neutralizing financial stockout penalties. 

Unlike traditional, simplistic Economic Order Quantity (EOQ) models that assume deterministic customer demand, this framework constructs a **Stochastic Continuous Review Policy $(Q, R)$**. It treats client demand as a dynamic stochastic process modeled via a **Poisson Distribution**. The engine employs an iterative mathematical optimization routine to jointly solve for the absolute lowest-cost Order Quantity ($Q^*$) and Reorder Point ($R^*$), followed by a discrete day-to-day empirical warehouse simulation run to stress-test and validate the policy.

---

## 🎯 Business Problem

Inventory mismatches account for significant margin drainage across global supply chains. Misjudging warehouse policies directly leads to two costly extremes:

| Problem Domain | Cost Drivers & Operational Bottlenecks |
|:---|:---|
| **Excessive Over-Stocking** | Inflated warehouse holding costs ($h$), capital tying, and stock obsolescence risks. |
| **Premature Under-Stocking** | Severe stockout penalty costs ($p$), missed revenue, and compromised customer service levels. |

> **Objective:** Jointly optimize the purchase lot size ($Q$) and safety-net reorder point ($R$) to mathematically guarantee the lowest possible total expected operating cost under volatile daily order flows.

---

## 🛠️ Mathematical Formulation

The system defines the Expected Total Cost function per unit time $E[C(Q,R)]$ by combining holding fees, fixed setup costs, and probabilistic shortage penalties:

$$E[C(Q,R)] = \frac{\lambda}{Q} K + h \left( \frac{Q}{2} + R - \lambda L \right) + \frac{\lambda}{Q} p \cdot n(R)$$

Where:
- $\lambda$ = Mean customer demand arrival rate per day.
- $L$ = Supplier lead time (days).
- $K$ = Fixed setup/ordering cost per transaction.
- $h$ = Inventory carrying cost per unit per day.
- $p$ = Stockout penalty cost per item.
- $n(R)$ = Expected number of units short per cycle.

### Optimization via Partial Derivatives

Because the optimal order lot $Q^*$ and critical warning threshold $R^*$ are mathematically coupled, the engine minimizes the objective function by seeking the stationary point. We evaluate the first-order partial derivatives and set them to zero:

$$\frac{\partial E[C(Q,R)]}{\partial Q} = -\frac{\lambda K}{Q^2} + \frac{h}{2} - \frac{\lambda p \cdot n(R)}{Q^2} = 0$$

Solving for $Q$ yields the stochastic-adjusted lot sizing equation:

$$Q^* = \sqrt{\frac{2\lambda (K + p \cdot n(R))}{h}}$$

Concurrently, evaluating the partial derivative with respect to $R$ ($\frac{\partial E[C]}{\partial R} = 0$) isolates the exact cumulative probability boundary governed by the inverse Poisson Cumulative Distribution Function (CDF):

$$P(X > R^*) = \frac{h \cdot Q^*}{\lambda \cdot p}$$

The script runs an iterative algorithm that cyclically refines $Q^*$ and $R^*$ until convergence limits are fully satisfied.

---

## 📊 System Results & Performance Visualizer

Running the script initializes a high-demand procurement scenario ($\lambda=15$ units/day, $L=6$ days) and outputs precise policy constraints:

```
=== SYSTEM RUNTIME RESULTS ===
Optimal Order Quantity (Q*) : 277.65 units
Optimal Reorder Point (R*)   : 106 units
Calculated Safety Stock      : 16 units
```

The model generates a comprehensive execution log and exports a publication-grade analytics visualization map tracking the warehouse's physical behavior across a 30-day operating horizon:

![Inventory Simulation Trend](stochastic_inventory_simulation.png)

### Operational Graph Insights:
- **The Dynamic Stock Curve (Green):** Displays daily ending stock positions. The degradation rate changes every day, accurately portraying real-world market variance.
- **The Automated Reorder Trigger (Red Line):** As soon as stock drops to or below $R^* = 106$ units, the engine instantly dispatches an order request for an additional $Q^* = 277.65$ units.
- **The Safety Buffer Zone (Orange Line):** Represents the buffer preventing stock depletion during the 6-day lead-time delay, effectively protecting against unexpected spikes in customer demand.

---

## 🚀 Getting Started

### Installation & Execution

1. Clone the repository and install dependencies:
```bash
git clone [https://github.com/yourusername/stochastic-inventory-optimization.git](https://github.com/yourusername/stochastic-inventory-optimization.git)
cd stochastic-inventory-optimization
pip install numpy pandas matplotlib scipy
```

2. Execute the engine optimization script:
```bash
python inventory_optimization.py
```

---

## 💡 Strategic Business Value

1. **Automated Procurement Workflows**
   Replaces manual gut-feeling warehouse auditing with strict, mathematical triggers, eliminating human error in recurring supplier communications.
2. **Quantifiable Risk Exposure**
   Allows executive management to consciously adjust service-level targets by varying the penalty cost parameter ($p$), balancing cost saving with customer satisfaction.
3. **Data-Grounded Capital Reallocation**
   By defining explicit Safety Stock baselines (e.g., 16 units), capital previously tied up in bloated buffer stock is freed for high-growth operations.

---

*Portfolio Project · Operations Research & Supply Chain Analytics · Nicolas Stenly Sirait · 2026*
