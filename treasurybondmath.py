# Simple calculation of ZCB.
def zcb(fv,y,t):
    """
    To Calculate Price of Zero Coupon Bond = Face Value / (1+y)^t
    fv: Face Value of Bond
    y: Annual Yield or Rate
    t: Time to Maturity
    """
    return fv/(1+y)**t

# Calculate 2 Years ZCB Price.
print(zcb(100,0.02,2))


import scipy.optimize as optimize
import matplotlib.pyplot as plt
import numpy as np

###########################################
# Bond Math Functions
###########################################

def b_ytm(price, fv, T, coup, freq=2, guess=0.05):
    """Calculate Yield to Maturity using Newton's method
    price: Current bond price
    fv: Face Value
    T: Time to Maturity (years)
    coup: Annual coupon rate (%)
    freq: Payment frequency per year (2 = semi-annual)
    guess: Initial YTM guess
    """
    freq = float(freq)
    periods = T*freq
    coupon = coup/100*fv/freq  # Semi-annual coupon payment
    dt = [(i+1)/freq for i in range(int(periods))]
    ytm_func = lambda y: sum([coupon/(1+y/freq)**(freq*t) for t in dt]) + fv/(1+y/freq)**(freq*max(dt)) - price
    return optimize.newton(ytm_func, guess)

def b_price(fv, T, ytm, coup, freq=2):
    """Calculate bond price given YTM
    fv: Face Value
    T: Time to Maturity (years)
    ytm: Yield to Maturity (as decimal)
    coup: Annual coupon rate (%)
    freq: Payment frequency per year (2 = semi-annual)
    """
    freq = float(freq)
    periods = T*freq
    coupon = coup/100*fv/freq
    dt = [(i+1)/freq for i in range(int(periods))]
    price = sum([coupon/(1+ytm/freq)**(freq*t) for t in dt]) + fv/(1+ytm/freq)**(freq*T)
    return price

def mod_duration(price, par, T, coup, freq, dy=0.01):
    """Calculate Modified Duration using central difference approximation"""
    ytm = b_ytm(price, par, T, coup, freq)
    ytm_minus = ytm - dy
    price_minus = b_price(par, T, ytm_minus, coup, freq)
    ytm_plus = ytm + dy
    price_plus = b_price(par, T, ytm_plus, coup, freq)
    mduration = (price_minus-price_plus)/(2*price*dy)
    return mduration

def b_convexity(price, par, T, coup, freq, dy=0.01):
    """Calculate bond convexity using central difference approximation"""
    ytm = b_ytm(price, par, T, coup, freq)
    ytm_minus = ytm - dy
    price_minus = b_price(par, T, ytm_minus, coup, freq)
    ytm_plus = ytm + dy
    price_plus = b_price(par, T, ytm_plus, coup, freq)
    convexity = (price_minus+price_plus-2*price)/(price*dy**2)
    return convexity

###########################################
# Analysis of 2050 Treasury
###########################################

# Bond parameters
par = 100
T = 26.2  # Time to maturity in years
coup = 1.25  # Coupon rate (%)
freq = 2  # Semi-annual payments
current_price = 50.0360

# Calculate key metrics
current_ytm = b_ytm(current_price, par, T, coup, freq)
mdur = mod_duration(current_price, par, T, coup, freq)
conv = b_convexity(current_price, par, T, coup, freq)

print(f"Current YTM: {current_ytm*100:.4f}%")
print(f"Modified Duration: {mdur:.4f}")
print(f"Convexity: {conv:.4f}\n")

###########################################
# Price Change Analysis Table
###########################################

print("Rate Change | Linear Approx | With Convexity | Actual Price | % Change")
print("-" * 75)

# Show detailed price changes for 1% increments
for dr in range(-4, 5):
    if dr != 0:  # Skip 0% change
        dr_decimal = dr/100
        
        # Linear approximation (duration only)
        linear_change = -mdur * dr * current_price
        
        # With convexity adjustment
        convexity_adjustment = 0.5 * conv * (dr_decimal)**2 * current_price
        total_change = linear_change + convexity_adjustment
        
        # Actual price using full calculation
        new_ytm = current_ytm + dr_decimal
        actual_price = b_price(par, T, new_ytm, coup, freq)
        pct_change = ((actual_price / current_price) - 1) * 100
        
        print(f"{dr:+4d}%      | ${linear_change:8.2f}  | ${total_change:8.2f}  | ${actual_price:8.2f} | {pct_change:+7.2f}%")

print("\n")

###########################################
# Price Sensitivity Analysis
###########################################

# Calculate price changes for different yield scenarios
rate_changes = np.arange(-4, 4.5, 0.5)  # Range of yield changes to analyze
pct_changes = []
for dr in rate_changes:
    new_ytm = current_ytm + dr/100
    actual_price = b_price(par, T, new_ytm, coup, freq)
    pct_change = ((actual_price / current_price) - 1) * 100
    pct_changes.append(pct_change)

###########################################
# Visualization
###########################################

# Create plot
plt.figure(figsize=(12, 8))
plt.style.use('classic')

# Main price sensitivity curve
plt.plot(rate_changes, pct_changes, 'b-', linewidth=2)

# Reference lines at current levels
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

# Add markers and labels for 1% yield changes
for dr in range(-3, 4):  # Changed from range(-4, 5) to range(-3, 4)
    if dr != 0:
        idx = np.where(rate_changes == dr)[0][0]
        pct = pct_changes[idx]
        # Vertical reference line
        plt.plot([dr, dr], [0, pct], 'k:', alpha=0.5)
        # Price change label with offset for readability
        x_offset = -0.4 if dr < 0 else 0.4
        # Move all labels down by 40% of their value
        y_offset = pct * -0.4  # Negative to move down
        plt.text(dr + x_offset, pct + y_offset, f'{pct:.1f}%', 
                horizontalalignment='right' if dr < 0 else 'left',
                verticalalignment='bottom' if pct > 0 else 'top')

# Formatting
plt.grid(True, alpha=0.2)
plt.xlabel('Change in Yield (%)', fontsize=10)
plt.ylabel('Price Change (%)', fontsize=10)
plt.title(f'1.25% Treasury 2050 Price Sensitivity\nCurrent Price: ${current_price:.2f}, YTM: {current_ytm*100:.2f}%',
          fontsize=12, pad=20)

# Save visualization
plt.savefig('treasury_sensitivity.png', 
            dpi=300, 
            bbox_inches='tight',
            facecolor='white')
plt.close()