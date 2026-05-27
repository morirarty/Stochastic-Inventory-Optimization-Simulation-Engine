# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.23.8",
#     "matplotlib==3.10.9",
#     "numpy==2.4.4",
#     "pandas==3.0.2",
#     "scipy==1.17.1",
# ]
# ///

import marimo

__generated_with = "0.23.5"
app = marimo.App(
    width="medium",
    css_file="/usr/local/_marimo/custom.css",
    auto_download=["html"],
)


@app.cell
def _():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.stats import poisson

    # ==============================================================================
    # OPERATIONAL PARAMETERS CONFIGURATION
    # ==============================================================================
    # Scenario: High-demand electronics components supplier
    LAMBDA_DAY = 15       # Mean daily customer demand (Poisson rate)
    LEAD_TIME = 6         # Supplier lead time in days
    K_COST = 200.0        # Fixed setup/ordering cost per order ($)
    H_COST = 0.08         # Holding cost per unit per day ($/unit/day)
    P_COST = 15.0         # Stockout penalty cost per unit ($/unit)

    # Compute expected demand during lead time (Poisson mean parameter)
    THETA = LAMBDA_DAY * LEAD_TIME  # 15 units * 6 days = 90 units

    print("Parameters successfully initialized.")
    print(f"Expected Demand During Lead Time (Theta): {THETA} units")
    return (
        H_COST,
        K_COST,
        LAMBDA_DAY,
        LEAD_TIME,
        P_COST,
        THETA,
        np,
        pd,
        plt,
        poisson,
    )


@app.cell
def _(np, poisson):
    def calculate_expected_shortage(R, theta):
        """
        Computes n(R): The expected number of stockout units per replenishment cycle
        based on the conditional expectation under the Poisson distribution.
        """
        upper_bound = int(theta + 5 * np.sqrt(theta))  # Safe computational limit
        x = np.arange(R + 1, upper_bound)
        pmf_values = poisson.pmf(x, theta)
        expected_shortage = np.sum((x - R) * pmf_values)
        return expected_shortage

    print("Shortage calculation engine ready.")
    return (calculate_expected_shortage,)


@app.cell
def _(
    H_COST,
    K_COST,
    LAMBDA_DAY,
    P_COST,
    THETA,
    calculate_expected_shortage,
    np,
    poisson,
):
    def optimize_inventory_policy():
        print("Executing Stochastic Optimization Loop...")
    
        # Initialization: Use classical deterministic EOQ as the first primal guess
        Q_current = np.sqrt((2 * LAMBDA_DAY * K_COST) / H_COST)
        R_current = 0
    
        max_iterations = 100
        tolerance = 1e-4
    
        for i in range(max_iterations):
            # Optimize R using the partial derivative boundary condition: 
            # P(X > R) = (h * Q) / (\lambda * p)
            target_prob = (H_COST * Q_current) / (LAMBDA_DAY * P_COST)
            target_prob = min(max(target_prob, 0.0), 1.0)  # Boundary clipping
        
            # Calculate Reorder Point (R) via Inverse CDF (Percent Point Function)
            R_new = int(poisson.ppf(1 - target_prob, THETA))
        
            # Calculate expected shortage penalty n(R)
            n_R = calculate_expected_shortage(R_new, THETA)
        
            # Update Order Quantity (Q) based on optimized shortage expectation
            Q_new = np.sqrt((2 * LAMBDA_DAY * (K_COST + P_COST * n_R)) / H_COST)
        
            # Convergence Check
            if abs(Q_current - Q_new) < tolerance and R_current == R_new:
                print(f"Convergence successfully achieved at iteration {i+1}.")
                return Q_new, R_new
            
            Q_current = Q_new
            R_current = R_new
        
        print("Warning: Optimization reached max iterations without full convergence.")
        return Q_current, R_current

    # Run optimization to lock the best parameters
    Q_opt, R_opt = optimize_inventory_policy()
    print(f"\nOptimal Order Quantity (Q*) : {round(Q_opt, 2)} units")
    print(f"Optimal Reorder Point (R*)   : {R_opt} units")
    print(f"Calculated Safety Stock      : {int(R_opt - THETA)} units")
    return Q_opt, R_opt


@app.cell
def _(LAMBDA_DAY, LEAD_TIME, Q_opt, R_opt, np, pd):
    def run_warehouse_simulation(Q_opt, R_opt, days=30, seed=42):
        np.random.seed(seed)
        realized_demand = np.random.poisson(LAMBDA_DAY, days)
    
        current_inventory = int(Q_opt)  # Initializing with full single lot
        inventory_in_transit = 0
        delivery_day = -1
    
        simulation_log = []
    
        for day in range(days):
            demand = realized_demand[day]
        
            # Process supplier arrival
            if delivery_day == day:
                current_inventory += int(Q_opt)
                inventory_in_transit = 0
                delivery_day = -1
            
            initial_stock = current_inventory
        
            # Process customer demand fulfillment
            if current_inventory >= demand:
                current_inventory -= demand
                fulfilled_sales = demand
                stockout_units = 0
            else:
                fulfilled_sales = current_inventory
                stockout_units = demand - current_inventory
                current_inventory = 0
            
            # Continuous Review Check: Trigger (Q, R) policy
            inventory_position = current_inventory + inventory_in_transit
            order_triggered = "NO"
        
            if inventory_position <= R_opt and inventory_in_transit == 0:
                order_triggered = "YES (Order Q* Placed)"
                inventory_in_transit = int(Q_opt)
                delivery_day = day + LEAD_TIME
            
            simulation_log.append({
                "Day": day + 1,
                "Initial Stock": initial_stock,
                "Demand": demand,
                "Sales Fulfilled": fulfilled_sales,
                "Stockout Units": stockout_units,
                "Ending Stock": current_inventory,
                "Order Decision": order_triggered
            })
        
        return pd.DataFrame(simulation_log)

    # Execute simulation
    df_results = run_warehouse_simulation(Q_opt, R_opt)
    print("Simulation logs generated. Showing first 10 days:")
    print(df_results.head(10).to_string(index=False))
    return (df_results,)


@app.cell
def _(Q_opt, R_opt, THETA, df_results, plt):
    def generate_portfolio_chart(df, Q_opt, R_opt):
        plt.figure(figsize=(14, 6.5))
        plt.grid(True, linestyle='--', alpha=0.6, zorder=1)
    
        # Plot inventory level
        plt.plot(df['Day'], df['Ending Stock'], marker='o', color='#2ca02c', 
                 linewidth=2.5, label='Ending Inventory Level', zorder=3)
    
        # Plot critical policy thresholds
        plt.axhline(y=R_opt, color='#d62728', linestyle='--', linewidth=2, 
                    label=f'Optimal Reorder Point (R* = {R_opt} units)')
    
        safety_stock = int(R_opt - THETA)
        plt.axhline(y=safety_stock, color='#ff7f0e', linestyle=':', linewidth=2, 
                    label=f'Safety Stock Baseline ({safety_stock} units)')
    
        # Highlight order events
        order_days = df[df['Order Decision'].str.contains('YES')]
        plt.scatter(order_days['Day'], order_days['Ending Stock'], color='#d62728', 
                    s=130, marker='v', edgecolor='black', zorder=4, 
                    label='Replenishment Order Triggered (Q*)')
    
        plt.title('Stochastic Inventory Control Simulation — Continuous Review (Q, R) Policy', 
                  fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Simulation Timeline (Days)', fontsize=12, labelpad=10)
        plt.ylabel('Warehouse Inventory Level (Units)', fontsize=12, labelpad=10)
    
        plt.xlim(1, len(df))
        plt.ylim(0, max(df['Initial Stock']) + 30)
        plt.xticks(df['Day'])
        plt.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='#e0e0e0', fontsize=10)
    
        plt.savefig('stochastic_inventory_simulation.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("Visualization saved successfully as 'stochastic_inventory_simulation.png'.")

    # Generate the plot
    generate_portfolio_chart(df_results, Q_opt, R_opt)
    return


if __name__ == "__main__":
    app.run()
