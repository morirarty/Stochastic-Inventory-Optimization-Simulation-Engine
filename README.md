# 📦 Stochastic Inventory Optimization & Simulation Engine
### Continuous Review (Q, R) Policy under Poisson Demand for Supply Chain Resilience

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![NumPy](https://img.shields.io/badge/NumPy-Scientific-lightblue?logo=numpy)
![SciPy](https://img.shields.io/badge/SciPy-Optimization-blue?logo=scipy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-green)
![Status](https://img.shields.io/badge/Status-Complete-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📌 Project Overview

This repository presents an advanced **Operations Research (OR)** and **Prescriptive Analytics** engine designed to solve one of the most persistent dilemmas in supply chain management: simultaneously minimizing warehouse carrying costs while eliminating financial stockout penalties.

Traditional inventory models — most notably the **Economic Order Quantity (EOQ)** — operate under the unrealistic assumption of perfectly deterministic, constant customer demand. In practice, daily order arrivals are inherently unpredictable. This project directly addresses that gap.

This framework constructs a **Stochastic Continuous Review Policy (Q, R)** that models customer demand as a dynamic random process governed by a **Poisson Distribution** — a statistically validated choice for modeling discrete, independent arrival events such as customer purchase orders. The engine employs an **iterative joint optimization algorithm** to simultaneously solve for:

- **Q\*** — The mathematically optimal order lot size that minimizes total procurement cost
- **R\*** — The precise inventory threshold that triggers an automatic replenishment order

The derived policy is subsequently stress-tested through a **discrete-event Monte Carlo simulation** over a 30-day operational horizon, empirically validating theoretical optimality under real-world demand stochasticity.

---

## 🎯 Business Problem

Inventory mismanagement is one of the largest hidden cost drivers across global supply chains. A 2023 IHL Group study estimated that inventory distortion — the combined effect of overstocking and stockouts — costs global retailers **$1.77 trillion annually**. Misjudging replenishment policies pushes operations toward one of two costly extremes:

| Problem Domain | Operational Consequences | Financial Impact |
|:---|:---|:---|
| **Over-Stocking** | Inflated warehouse holding costs, excessive capital lock-in, obsolescence risk | High carrying cost per unit |
| **Under-Stocking** | Missed sales, customer churn, emergency procurement at premium prices | High stockout penalty per unit |

> **Objective:** Jointly determine the optimal purchase lot size $Q^{*}$ and reorder trigger point $R^{*}$ that mathematically guarantee the minimum possible total expected operating cost under volatile, stochastic daily demand conditions.

---

## 🛠️ Mathematical Formulation

### 1. Total Expected Cost Function

The optimization target is the **Expected Total Cost per unit time** $E[C(Q,R)]$, composed of three distinct cost components:

$$E[C(Q,R)] = \frac{\lambda}{Q} K + h \left( \frac{Q}{2} + R - \lambda L \right) + \frac{\lambda}{Q} p \cdot n(R)$$

**Parameter Definitions:**

| Symbol | Description | Unit |
|:------:|:------------|:-----|
| $\lambda$ | Mean customer demand arrival rate | units/day |
| $L$ | Supplier replenishment lead time | days |
| $K$ | Fixed ordering/setup cost per transaction | USD/order |
| $h$ | Inventory holding (carrying) cost | USD/unit/day |
| $p$ | Stockout penalty cost per unfulfilled unit | USD/unit |
| $n(R)$ | Expected units short per replenishment cycle | units |
| $Q$ | Order lot size (decision variable) | units |
| $R$ | Reorder point threshold (decision variable) | units |

---

### 2. Joint Optimization via Partial Derivatives

Because $Q^{*}$ and $R^{*}$ are **mathematically interdependent** — each optimal value is a function of the other — a simple closed-form solution does not exist. The engine resolves this by applying **first-order optimality conditions** and iterating to convergence.

**Partial derivative with respect to Q:**

$$\frac{\partial E[C(Q,R)]}{\partial Q} = -\frac{\lambda K}{Q^{2}} + \frac{h}{2} - \frac{\lambda p \cdot n(R)}{Q^{2}} = 0$$

Solving for $Q$ yields the **stochastic-adjusted lot sizing equation:**

$$Q^{*} = \sqrt{\frac{2\lambda \left(K + p \cdot n(R)\right)}{h}}$$

**Partial derivative with respect to R:**

Setting the partial derivative with respect to R equal to zero isolates the critical service-level boundary:

$$P(X > R^* ) = \frac{h \cdot Q^* }{\lambda \cdot p}$$

Where $X \sim \text{Poisson}(\lambda L)$ represents demand during lead time. $R^{*}$ is resolved via the **inverse Poisson CDF**, identifying the minimum integer threshold satisfying the above probability condition.

---

### 3. Expected Shortage Function

The expected number of units short per cycle $n(R)$ is computed analytically over the Poisson demand distribution during lead time:

$$n(R) = \sum_{x=R+1}^{\infty} (x - R) \cdot P(X = x) = E[\max(X - R, 0)]$$

This quantity directly links $Q^{*}$ and $R^{*}$, making iterative joint optimization necessary.

---

### 4. Iterative Convergence Algorithm

```
Initialize: Q₀ ← EOQ (deterministic baseline)

Repeat:
    Step 1: Compute n(R) from current R using Poisson PMF
    Step 2: Update Q* ← sqrt[ 2λ(K + p·n(R)) / h ]
    Step 3: Compute P(X > R) = h·Q* / (λ·p)
    Step 4: Update R* ← Poisson inverse CDF at (1 - P(X > R))
    Step 5: Check convergence |Q_new - Q_old| < ε

Until convergence criteria satisfied → Output (Q*, R*)
```

**Convergence is guaranteed** because the cost function $E[C(Q,R)]$ is jointly convex in $(Q, R)$ for Poisson demand under standard parameter conditions.

---

## 📊 System Results & Simulation Output

### Optimization Results

Running the engine under a high-velocity procurement scenario produces the following certified policy parameters:

```
╔══════════════════════════════════════════════════════╗
║           OPTIMIZATION ENGINE — FINAL OUTPUT         ║
╠══════════════════════════════════════════════════════╣
║  Input Parameters:                                   ║
║    Mean Daily Demand  (λ)  :  15   units/day         ║
║    Supplier Lead Time (L)  :  6    days              ║
║    Fixed Order Cost   (K)  :  $500 /order            ║
║    Holding Cost       (h)  :  $2   /unit/day         ║
║    Stockout Penalty   (p)  :  $50  /unit             ║
╠══════════════════════════════════════════════════════╣
║  Optimal Policy:                                     ║
║    Order Quantity     (Q*) :  277.65  units          ║
║    Reorder Point      (R*) :  106     units          ║
║    Safety Stock            :  16      units          ║
║    Expected Total Cost     :  Minimized ✅           ║
╚══════════════════════════════════════════════════════╝
```

**Derived Inventory Policy Interpretation:**

| Decision | Action |
|:---------|:-------|
| When stock drops to **106 units** | Immediately place a replenishment order |
| Order size every cycle | **277.65 units** (278 units in practice) |
| Safety buffer maintained | **16 units** above mean lead-time demand |

---

### 30-Day Simulation Visualization

The Monte Carlo simulation generates a publication-grade operational analytics chart tracking warehouse inventory behavior across a full 30-day horizon:

![Inventory Simulation Trend](stochastic_inventory_simulation.png)

**Chart Component Breakdown:**

| Visual Element | Color | Interpretation |
|:--------------|:-----:|:--------------|
| Dynamic Stock Level Curve | 🟢 Green | Daily ending inventory position. Non-linear degradation rate reflects true stochastic demand variance |
| Automated Reorder Trigger | 🔴 Red Line | The $R^{*} = 106$ unit threshold. When stock touches this line, an order for $Q^{*} = 278$ units is dispatched |
| Safety Stock Buffer | 🟠 Orange Line | The 16-unit protective floor absorbing unexpected demand spikes during the 6-day lead time window |
| Replenishment Events | ↑ Arrows | Instantaneous stock jumps representing order arrivals after lead time delay |

---

## 📁 Repository Structure

```
stochastic-inventory-optimization/
│
├── inventory_optimization.py            # Core optimization & simulation engine
├── stochastic_inventory_simulation.png  # Output visualization
├── requirements.txt                     # Dependency list
└── README.md                            # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install numpy scipy matplotlib pandas
```

| Library | Version | Role |
|:--------|:-------:|:-----|
| `numpy` | >= 1.21 | Array operations & random Poisson sampling |
| `scipy` | >= 1.7 | Poisson CDF/PPF for R* computation |
| `matplotlib` | >= 3.4 | Simulation trajectory visualization |
| `pandas` | >= 1.3 | Results tabulation & export |

### Installation & Execution

```bash
# 1. Clone the repository
git clone https://github.com/[your-username]/stochastic-inventory-optimization.git

# 2. Navigate to project directory
cd stochastic-inventory-optimization

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the optimization engine
python inventory_optimization.py
```

### Expected Output

```bash
[INFO] Initializing stochastic demand model...  λ = 15 units/day
[INFO] Running iterative joint optimization...
[INFO] Convergence achieved at iteration 4
[INFO] Q* = 277.65 | R* = 106 | Safety Stock = 16
[INFO] Running 30-day Monte Carlo simulation...
[INFO] Simulation complete. Exporting visualization...
[SUCCESS] Output saved → stochastic_inventory_simulation.png
```

---

## 💡 Strategic Business Value

### 1. Automated Procurement Workflows
Eliminates manual, intuition-driven warehouse auditing by replacing it with mathematically rigorous replenishment triggers. The rule is simple and deterministic: **when stock reaches $R^{*}$, order $Q^{*}$ units** — removing latency and human error from the procurement cycle entirely.

### 2. Quantifiable Risk & Service Level Control
Executive management can directly manipulate the **stockout penalty parameter** $p$ to consciously set organizational risk tolerance. Increasing $p$ raises $R^{*}$, improving service level at the cost of higher holding expenses — providing a transparent, data-grounded lever for strategic trade-off decisions.

### 3. Capital Efficiency Through Safety Stock Precision
Traditional over-conservative safety stock policies often lock 30–50% excess capital in idle inventory. This engine's 16-unit safety stock is not a guess — it is the **minimum statistically sufficient buffer** for the specified service level, freeing excess working capital for higher-return operational investments.

### 4. Scalability Across SKU Portfolios
The optimization engine is fully parameterized by design. By supplying different $(\lambda, L, K, h, p)$ values per SKU, the same codebase simultaneously optimizes replenishment policies across an entire product catalog — making it directly applicable to enterprise-scale inventory management systems.

---

## 🔬 Model Assumptions & Limitations

| Assumption | Limitation | Future Enhancement |
|:-----------|:-----------|:-------------------|
| Poisson demand distribution | May not fit all product categories | Fit distribution empirically per SKU via AIC/BIC selection |
| Single product, single depot | Cannot model multi-SKU interactions | Multi-item joint replenishment extension |
| Fixed lead time $L$ | Ignores lead time variability | Stochastic lead time modeled as $L \sim \text{Normal}(\mu_L, \sigma_L)$ |
| Constant cost parameters | Real costs fluctuate seasonally | Dynamic cost parameterization via time-series inputs |
| No capacity constraints | Unlimited warehouse space assumed | Capacitated inventory model integration |

---

## 📚 References

- Silver, E.A., Pyke, D.F., & Thomas, D.J. (2017). *Inventory and Production Management in Supply Chains* (4th ed.). CRC Press.
- Hadley, G. & Whitin, T.M. (1963). *Analysis of Inventory Systems*. Prentice-Hall.
- IHL Group (2023). *Inventory Distortion Study: Overstocks, Out-of-Stocks & Returns.*
- Zipkin, P.H. (2000). *Foundations of Inventory Management*. McGraw-Hill.

---

*Portfolio Project · Operations Research & Supply Chain Analytics · Nicolas Stenly Sirait · 2026*
