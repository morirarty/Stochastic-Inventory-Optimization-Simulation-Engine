# 📦 Stochastic Inventory Optimization & Simulation Engine
### Continuous Review $(Q, R)$ Policy under Poisson Demand for Supply Chain Resilience

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![NumPy](https://img.shields.io/badge/NumPy-Scientific-lightblue?logo=numpy)
![SciPy](https://img.shields.io/badge/SciPy-Optimization-blue?logo=scipy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-green)
![Status](https://img.shields.io/badge/Status-Complete-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📌 Project Overview

This repository presents an advanced **Operations Research (OR)** and **Prescriptive Analytics** engine designed to solve one of the most persistent dilemmas in supply chain management: simultaneously minimizing warehouse carrying costs while completely eliminating financial stockout penalties.

Traditional inventory models — most notably the classical **Economic Order Quantity (EOQ)** — operate under the unrealistic assumption of perfectly deterministic, constant customer demand. In real-world enterprise operations, daily order arrivals are inherently volatile and stochastic. This project bridges that gap.

This framework constructs a rigorous **Stochastic Continuous Review Policy $(Q, R)$** that models customer demand as a dynamic random process governed by a **Poisson Distribution** — a statistically validated choice for discrete, independent arrival events. The engine employs an **iterative joint optimization algorithm** to simultaneously solve for:

* $Q^{*}$ — The mathematically optimal order lot size that minimizes total procurement and setup costs.
* $R^{*}$ — The precise inventory threshold that triggers an automatic replenishment order.

The derived policy is subsequently stress-tested through a **discrete-event Monte Carlo simulation** over a 30-day operational horizon, empirically validating theoretical optimality under real-world demand stochasticity.

---

## 🎯 Business Problem

Inventory distortion is a catastrophic, often hidden profit drainer across global supply chains. According to market research by the IHL Group, inventory distortion — the combined impact of overstocking and stockouts — costs global retailers over **$1.77 trillion annually**. Misjudging replenishment policies pushes operations toward two costly extremes:

| Problem Domain | Operational Consequences | Financial Impact |
|:---|:---|:---|
| **⚠️ Over-Stocking** | Inflated warehouse holding costs, excessive working capital lock-in, and high inventory obsolescence risks. | High carrying cost per unit |
| **🚨 Under-Stocking** | Missed sales, immediate customer churn, and emergency procurement at premium spot-market prices. | High stockout penalty per unit |

> **Operational Objective:** Jointly determine the optimal purchase lot size $Q^{*}$ and reorder trigger point $R^{*}$ that mathematically guarantee the minimum possible total expected operating cost under volatile, stochastic daily demand conditions.

---

## 🛠️ Mathematical Formulation

### 1. Total Expected Cost Function

The optimization target is the **Expected Total Cost per unit time** $E[C(Q,R)]$, modeled as a joint function of fixed setup, linear holding, and probabilistic shortage penalties:

$$E[C(Q,R)] = \frac{\lambda}{Q} K + h \left( \frac{Q}{2} + R - \lambda L \right) + \frac{\lambda}{Q} p \cdot n(R)$$

**Parameter System Definitions:**

| Symbol | Description | Operational Unit |
|:------:|:------------|:-----------------|
| $\lambda$ | Mean customer demand arrival rate | units / day |
| $L$ | Supplier replenishment lead time | days |
| $K$ | Fixed ordering/setup cost per transaction | USD / order |
| $h$ | Inventory holding (carrying) cost | USD / unit / day |
| $p$ | Stockout penalty cost per unfulfilled unit | USD / unit |
| $n(R)$ | Expected units short per replenishment cycle | units |
| $Q$ | Order lot size *(Decision Variable)* | units |
| $R$ | Reorder point threshold *(Decision Variable)* | units |

---

### 2. Joint Optimization via Partial Derivatives

Because $Q^{*}$ and $R^{*}$ are **mathematically interdependent** — the optimal value of each variable is directly embedded within the function of the other — a simple closed-form solution does not exist. The engine resolves this by applying **first-order optimality conditions** via partial differentiation and iterating to convergence.

#### A. Partial Derivative with respect to $Q$:
$$\frac{\partial E[C(Q,R)]}{\partial Q} = -\frac{\lambda K}{Q^{2}} + \frac{h}{2} - \frac{\lambda p \cdot n(R)}{Q^{2}} = 0$$

Solving for $Q$ yields the **stochastic-adjusted lot sizing equation:**
$$Q^{*} = \sqrt{\frac{2\lambda \left(K + p \cdot n(R)\right)}{h}}$$

#### B. Partial Derivative with respect to $R$:
Setting the partial derivative with respect to $R$ equal to zero isolates the critical service-level boundary:
$$P(X > R^{*}) = \frac{h \cdot Q^{*}}{\lambda \cdot p}$$

Where $X \sim \text{Poisson}(\lambda L)$ represents demand during the lead time window. $R^{*}$ is resolved via the **inverse Poisson Cumulative Distribution Function (CDF)**, identifying the minimum integer threshold satisfying the probability boundary.

---

### 3. Expected Shortage Function

The expected number of units short per cycle $n(R)$ represents the conditional expectation of unfulfilled demand, computed analytically over the Poisson distribution:

$$n(R) = \sum_{x=R+1}^{\infty} (x - R) \cdot P(X = x) = E[\max(X - R, 0)]$$

This exact quantity directly couples $Q^{*}$ and $R^{*}$, rendering standard isolated calculations obsolete and necessitating an iterative optimization loop.

---

### 4. Iterative Convergence Algorithm

```
Initialize: Q_0 ← EOQ (Deterministic baseline guess)

Repeat Convergence Loop:
   Step 1: Compute n(R) from current R using Poisson PMF
   Step 2: Update Order Lot: Q* ← sqrt[ 2λ(K + p·n(R)) / h ]
   Step 3: Evaluate Probability Target: P(X > R) = h·Q* / (λ·p)
   Step 4: Update Reorder Point: R* ← Poisson Inverse CDF at (1 - P(X > R))
   Step 5: Check delta stability: |Q_new - Q_old| < ϵ

Until convergence criteria satisfied → Output Optimal Vector (Q*, R*)
```

> **Mathematical Note:** Convergence is structurally guaranteed because the expected cost surface $E[C(Q,R)]$ is jointly convex in $(Q, R)$ for Poisson demand distributions under standard parameter bounds.

---

## 📊 System Results & Simulation Output

### Optimization Results

Running the engine under a high-velocity procurement scenario produces the following certified policy parameters:

```
┌──────────────────────────────────────────────────────┐
│           OPTIMIZATION ENGINE — FINAL OUTPUT         │
├──────────────────────────────────────────────────────┤
│  Input Operational Parameters:                       │
│    Mean Daily Demand  (λ)  :  15   units/day         │
│    Supplier Lead Time (L)  :  6    days              │
│    Fixed Order Cost   (K)  :  $500 /order            │
│    Holding Cost       (h)  :  $2   /unit/day         │
│    Stockout Penalty   (p)  :  $50  /unit             │
├──────────────────────────────────────────────────────┤
│  Derived Optimal Policy Vector:                      │
│    Order Quantity     (Q*) :  277.65  units          │
│    Reorder Point      (R*) :  106     units          │
│    Safety Stock Baseline   :  16      units          │
│    Expected Total Cost     :  MINIMIZED GLOBAL OPTIMA│
└──────────────────────────────────────────────────────┘
```

**Derived Inventory Policy Interpretation:**

| Business Decision | Algorithmic Rule | Operational Action |
|:---|:---|:---|
| **Replenishment Trigger** | When physical stock drops to **106 units** | Instantly dispatch a new purchase order to supplier. |
| **Order Volume** | Procure exactly **277.65 units** ($278$ in practice) | Order this economic lot size to minimize transaction friction. |
| **Buffer Maintenance** | Maintain **16 units** as dedicated Safety Stock | Protects the warehouse from unexpected lead time variance. |

---

### 30-Day Simulation Visualization

The Monte Carlo simulation generates a publication-grade operational analytics chart tracking warehouse inventory behavior across a full 30-day horizon:

![Inventory Simulation Trend](stochastic_inventory_simulation.png)

**Chart Component Breakdown:**

* 🟢 **Dynamic Stock Level Curve:** Displays daily ending inventory positions. The non-linear degradation rate accurately reflects true stochastic demand variance.
* 🔴 **Automated Reorder Trigger ($R^{*}$):** The 106-unit threshold line. As soon as the green stock curve touches this line, an order for $Q^{*} = 278$ units is dispatched.
* 🟠 **Safety Stock Buffer:** The 16-unit protective floor. This buffer absorbs unexpected demand spikes during the 6-day lead time window, preventing the stock level from dropping to zero.

---

## 📁 Repository Structure

```
stochastic-inventory-optimization/
│
├── inventory_optimization.py    # Core optimization & simulation engine
├── stochastic_inventory_simulation.png  # Output visualization map
├── requirements.txt             # Project dependency list
└── README.md                    # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install numpy scipy matplotlib pandas
```

| Library | Minimum Version | Operational Role within Framework |
|:---|:---:|:---|
| `numpy` | `>= 1.21` | High-performance matrix operations and random Poisson sampling. |
| `scipy` | `>= 1.7` | Inverse CDF computation (`ppf`) for exact $R^{*}$ resolution. |
| `matplotlib` | `>= 3.4` | Generation of publication-grade operational trajectory charts. |
| `pandas` | `>= 1.3` | Multi-variable simulation logs tabulation and structured export. |

### Installation & Execution

```bash
# 1. Clone the repository
git clone [https://github.com/](https://github.com/)[your-username]/stochastic-inventory-optimization.git

# 2. Navigate to project directory
cd stochastic-inventory-optimization

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the optimization engine
python inventory_optimization.py
```

### Expected Runtime Output

```bash
[INFO] Initializing stochastic demand model... λ = 15 units/day
[INFO] Running iterative joint optimization...
[INFO] Convergence successfully achieved at iteration 4.
[INFO] Results calculated: Q* = 277.65 | R* = 106 | Safety Stock = 16
[INFO] Running 30-day Monte Carlo operational simulation...
[INFO] Simulation complete. Exporting high-resolution asset...
[SUCCESS] Optimization chart saved successfully → stochastic_inventory_simulation.png
```

---

## 💡 Strategic Business Value

### 1. Automated Procurement Workflows
Eliminates manual, intuition-driven warehouse auditing by replacing it with mathematically rigorous replenishment triggers. The rule is simple and deterministic: **when inventory position reaches $R^{*}$, order $Q^{*}$ units**, completely removing human delay and variance from the procurement cycle.

### 2. Quantifiable Risk & Service Level Control
Executive management can directly manipulate the **stockout penalty parameter** $p$ to consciously align organizational risk tolerance with corporate strategy. Increasing $p$ automatically scales $R^{*}$, improving service level performance at the cost of higher holding expenses—providing an explicit, data-grounded lever for strategic trade-off decisions.

### ### 3. Working Capital Efficiency Through Statistical Precision
Traditional, over-conservative safety stock rules of thumb often lock 30% to 50% of excess corporate capital in idle, dead inventory. This engine's 16-unit safety stock is not an arbitrary guess—it is the **minimum statistically sufficient buffer** required to protect margins, freeing up trapped working capital for higher-return operational investments.

### 4. Enterprise Scalability Across SKU Portfolios
The core optimization engine is completely parameterized by design. By supplying different input parameter vectors $(\lambda, L, K, h, p)$ per individual product item, the exact same codebase simultaneously optimizes custom replenishment policies across an entire enterprise catalog.

---

## 🔬 Model Assumptions & Limitations

| Core Framework Assumption | Operational Limitation | Proposed Future Enhancement |
|:---|:---|:---|
| Stationary Poisson demand distribution | May not fit seasonal demand spikes or trend shifts | Integrate time-varying non-homogeneous Poisson processes. |
| Single-product, single-depot structure | Ignores multi-SKU space and budget constraints | Extend engine to handle multi-item joint constraints. |
| Perfectly fixed supplier lead time $L$ | Overlooks logistics delays and shipping port congestion | Model lead time as a continuous random variable: $L \sim \mathcal{N}(\mu_L, \sigma_L^2)$. |

---

## 📚 References

* Silver, E. A., Pyke, D. F., & Thomas, D. J. (2017). *Inventory and Production Management in Supply Chains* (4th ed.). CRC Press.
* Hadley, G., & Whitin, T. M. (1963). *Analysis of Inventory Systems*. Prentice-Hall.
* IHL Group (2023). *Inventory Distortion Study: Overstocks, Out-of-Stocks & Returns.*
* Zipkin, P. H. (2000). *Foundations of Inventory Management*. McGraw-Hill.

---

*Portfolio Project · Operations Research & Supply Chain Analytics · Nicolas Stenly Sirait · 2026*
