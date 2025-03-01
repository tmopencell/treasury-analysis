import scipy.optimize as optimize
import matplotlib.pyplot as plt
import numpy as np

###########################################
# UK and Inflation-Linked Bond Functions
###########################################

def real_yield_to_nominal(real_yield, inflation_rate):
    """Convert real yield to nominal yield using Fisher equation
    (1 + nominal) = (1 + real)(1 + inflation)
    """
    return (1 + real_yield) * (1 + inflation_rate) - 1

def breakeven_inflation(nominal_price, real_price, T, nominal_coupon, real_coupon):
    """Calculate breakeven inflation rate between nominal and real bonds"""
    def objective(inflation):
        nominal_cf = nominal_coupon/2  # Semi-annual
        real_cf = real_coupon/2 * (1 + inflation)**T
        return nominal_price - real_price * (1 + inflation)**T

    # Use wider search range and handle potential errors
    try:
        return optimize.brentq(objective, -0.10, 0.25)  # Search between -10% and 25%
    except ValueError:
        # If brentq fails, try a grid search
        test_rates = np.linspace(-0.10, 0.25, 1000)
        values = [abs(objective(r)) for r in test_rates]
        return test_rates[np.argmin(values)]

def linker_price(fv, T, real_yield, inflation_rate, real_coup, freq=2):
    """Calculate inflation-linked bond price"""
    freq = float(freq)
    periods = T*freq
    real_coupon = real_coup/100*fv/freq
    
    # Inflate face value and coupons
    inflated_fv = fv * (1 + inflation_rate)**T
    
    dt = [(i+1)/freq for i in range(int(periods))]
    price = sum([real_coupon*(1 + inflation_rate)**t/(1+real_yield/freq)**(freq*t) for t in dt]) + \
            inflated_fv/(1+real_yield/freq)**(freq*T)
    return price

###########################################
# Analysis Parameters
###########################################

# UK Gilt 0.5% 2061
uk_par = 100
uk_T = 37  # Maturity in 2061
uk_coup = 0.5  # 0.5% coupon
uk_yield = 0.0445  # Current yield ~4.45%

# UK Index-linked 0.125% 2073
linker_par = 100
linker_T = 49  # Maturity in 2073
linker_coup = 0.125  # 0.125% coupon
linker_real_yield = -0.0175  # Current real yield ~-1.75%
inflation_rate = 0.041  # Current RPI inflation ~4.1%

###########################################
# Analysis and Visualization
###########################################

# 1. UK Gilt Price Sensitivity
rate_changes = np.arange(-4, 4.5, 0.5)  # Match treasury range
gilt_price_changes = []
gilt_prices = []

base_gilt_price = linker_price(uk_par, uk_T, uk_yield, 0, uk_coup)
for dr in rate_changes:
    new_rate = uk_yield + dr/100
    new_price = linker_price(uk_par, uk_T, new_rate, 0, uk_coup)
    pct_change = ((new_price / base_gilt_price) - 1) * 100
    gilt_price_changes.append(pct_change)
    gilt_prices.append(new_price)

# Find rate change needed for price = 100
gilt_prices = np.array(gilt_prices)
par_rate_change = np.interp(100, gilt_prices[::-1], rate_changes[::-1])
par_pct_change = ((100 / base_gilt_price) - 1) * 100

plt.figure(figsize=(12, 8))
plt.style.use('classic')

# Main price sensitivity curve
plt.plot(rate_changes, gilt_price_changes, 'b-', linewidth=2)

# Reference lines at current levels
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

# Add markers and labels for 1% yield changes
for dr in range(-3, 4):
    if dr != 0:
        idx = np.where(rate_changes == dr)[0][0]
        pct = gilt_price_changes[idx]
        # Vertical reference line
        plt.plot([dr, dr], [0, pct], 'k:', alpha=0.5)
        # Price change label with offset for readability
        x_offset = -0.4 if dr < 0 else 0.4
        # Move all labels down by 40% of their value
        y_offset = pct * -0.4  # Negative to move down
        plt.text(dr + x_offset, pct + y_offset, f'{pct:.1f}%', 
                horizontalalignment='right' if dr < 0 else 'left',
                verticalalignment='bottom' if pct > 0 else 'top')

# Add par marker
plt.plot([par_rate_change], [par_pct_change], 'ro')  # Red dot at par point
plt.plot([par_rate_change, par_rate_change], [0, par_pct_change], 'r:', alpha=0.5)
plt.text(par_rate_change + 0.1, par_pct_change, f'Par: {par_rate_change:.1f}%', 
        color='red', horizontalalignment='left')

plt.grid(True, alpha=0.2)
plt.xlabel('Change in Yield (%)', fontsize=10)
plt.ylabel('Price Change (%)', fontsize=10)
plt.title(f'UK Gilt 0.5% 2061 Price Sensitivity\nCurrent Price: £{base_gilt_price:.2f}, YTM: {uk_yield*100:.2f}%',
          fontsize=12, pad=20)

plt.savefig('uk_gilt_sensitivity.png',
            dpi=300,
            bbox_inches='tight',
            facecolor='white')
plt.close()

# 2. Linker Price Sensitivity to Real Yields
real_rate_changes = np.arange(-4, 4.5, 0.5)  # Match treasury range
linker_price_changes = []

base_linker_price = linker_price(linker_par, linker_T, linker_real_yield, inflation_rate, linker_coup)
for dr in real_rate_changes:
    new_real_rate = linker_real_yield + dr/100
    new_price = linker_price(linker_par, linker_T, new_real_rate, inflation_rate, linker_coup)
    pct_change = ((new_price / base_linker_price) - 1) * 100
    linker_price_changes.append(pct_change)

plt.figure(figsize=(12, 8))
plt.style.use('classic')

# Main price sensitivity curve
plt.plot(real_rate_changes, linker_price_changes, 'b-', linewidth=2)

# Reference lines at current levels
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

# Add markers and labels for 1% yield changes
for dr in range(-3, 4):
    if dr != 0:
        idx = np.where(real_rate_changes == dr)[0][0]
        pct = linker_price_changes[idx]
        # Vertical reference line
        plt.plot([dr, dr], [0, pct], 'k:', alpha=0.5)
        # Price change label with offset for readability
        x_offset = -0.4 if dr < 0 else 0.4
        # Move all labels down by 40% of their value
        y_offset = pct * -0.4  # Negative to move down
        plt.text(dr + x_offset, pct + y_offset, f'{pct:.1f}%', 
                horizontalalignment='right' if dr < 0 else 'left',
                verticalalignment='bottom' if pct > 0 else 'top')

plt.grid(True, alpha=0.2)
plt.xlabel('Change in Real Yield (%)', fontsize=10)
plt.ylabel('Price Change (%)', fontsize=10)
plt.title(f'UK Index-linked 0.125% 2073 Real Yield Sensitivity\nCurrent Price: £{base_linker_price:.2f}, Real Yield: {linker_real_yield*100:.2f}%',
          fontsize=12, pad=20)

plt.savefig('uk_linker_sensitivity.png',
            dpi=300,
            bbox_inches='tight',
            facecolor='white')
plt.close()

# 3. Inflation Sensitivity
inflation_changes = np.arange(-4, 4.5, 0.5)  # Match other ranges
inflation_price_changes = []

for di in inflation_changes:
    new_inflation = inflation_rate + di/100
    new_price = linker_price(linker_par, linker_T, linker_real_yield, new_inflation, linker_coup)
    pct_change = ((new_price / base_linker_price) - 1) * 100
    inflation_price_changes.append(pct_change)

plt.figure(figsize=(12, 8))
plt.style.use('classic')

# Main price sensitivity curve
plt.plot(inflation_changes, inflation_price_changes, 'b-', linewidth=2)

# Reference lines at current levels
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

# Add markers and labels for 1% inflation changes
for di in range(-3, 4):
    if di != 0:
        idx = np.where(inflation_changes == di)[0][0]
        pct = inflation_price_changes[idx]
        # Vertical reference line
        plt.plot([di, di], [0, pct], 'k:', alpha=0.5)
        # Price change label with offset for readability
        x_offset = -0.4 if di < 0 else 0.4
        # Move all labels down by 40% of their value
        y_offset = pct * -0.4  # Negative to move down
        plt.text(di + x_offset, pct + y_offset, f'{pct:.1f}%', 
                horizontalalignment='right' if di < 0 else 'left',
                verticalalignment='bottom' if pct > 0 else 'top')

plt.grid(True, alpha=0.2)
plt.xlabel('Change in Inflation Rate (%)', fontsize=10)
plt.ylabel('Price Change (%)', fontsize=10)
plt.title(f'UK Index-linked 0.125% 2073 Inflation Sensitivity\nCurrent Inflation: {inflation_rate*100:.1f}%',
          fontsize=12, pad=20)

plt.savefig('uk_inflation_sensitivity.png',
            dpi=300,
            bbox_inches='tight',
            facecolor='white')
plt.close()

# 4. Breakeven Analysis
inflation_changes = np.arange(-4, 4.5, 0.5)  # ±4% range
nominal_values = []
real_values = []

# Calculate base prices and breakeven
base_nominal = linker_price(uk_par, uk_T, uk_yield, 0, uk_coup)
base_real = linker_price(linker_par, linker_T, linker_real_yield, inflation_rate, linker_coup)
breakeven = breakeven_inflation(base_nominal, base_real, uk_T, uk_coup, linker_coup)

# Calculate values and percentage differences
for di in inflation_changes:
    nominal_price = linker_price(uk_par, uk_T, uk_yield, 0, uk_coup)
    real_price = linker_price(linker_par, linker_T, linker_real_yield, inflation_rate + di/100, linker_coup)
    
    # Convert to percentage difference from nominal
    nominal_pct = 0  # Nominal is reference line
    real_pct = ((real_price / nominal_price) - 1) * 100
    
    nominal_values.append(nominal_pct)
    real_values.append(real_pct)

plt.figure(figsize=(12, 8))
plt.style.use('classic')

# Plot percentage differences
plt.plot(inflation_changes, nominal_values, 'b-', linewidth=2, label='Nominal Gilt (0.5% 2061)')
plt.plot(inflation_changes, real_values, 'r-', linewidth=2, label='Index-linked Gilt (0.125% 2073)')

# Reference lines
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

# Add current inflation marker
plt.axvline(x=0, color='orange', linestyle=':', alpha=0.5, 
            label=f'Current RPI: {inflation_rate*100:.1f}%')

# Add markers for key changes
for di in range(-3, 4):
    if di != 0:
        idx = np.where(inflation_changes == di)[0][0]
        pct = real_values[idx]
        plt.plot([di, di], [0, pct], 'k:', alpha=0.5)
        x_offset = -0.4 if di < 0 else 0.4
        y_offset = pct * -0.4
        plt.text(di + x_offset, pct + y_offset, f'{pct:.1f}%',
                horizontalalignment='right' if di < 0 else 'left',
                verticalalignment='bottom' if pct > 0 else 'top')

plt.grid(True, alpha=0.2)
plt.xlabel('Change in Inflation Rate (%)', fontsize=10)
plt.ylabel('Price Difference from Nominal (%)', fontsize=10)
plt.title('Index-linked vs Nominal Gilt Value\nRelative Performance Analysis',
          fontsize=12, pad=20)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig('uk_breakeven_analysis.png',
            dpi=300,
            bbox_inches='tight',
            facecolor='white')
plt.close()

# Print key metrics
print(f"\nUK Ultra-Long Bond Analysis")
print(f"-------------------------")
print(f"Nominal Gilt (0.5% 2061):")
print(f"  Price: £{base_gilt_price:.2f}")
print(f"  YTM: {uk_yield*100:.2f}%")
print(f"\nIndex-linked Gilt (0.125% 2073):")
print(f"  Price: £{base_linker_price:.2f}")
print(f"  Real Yield: {linker_real_yield*100:.2f}%")
print(f"\nBreakeven Inflation: {breakeven*100:.2f}%")
print(f"Current RPI: {inflation_rate*100:.1f}%") 