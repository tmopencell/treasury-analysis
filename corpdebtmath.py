import scipy.optimize as optimize
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

###########################################
# Corporate Bond Math Functions
###########################################

def corp_ytm(price, fv, T, coup, credit_spread, freq=2, guess=0.05):
    """Calculate Corporate Bond Yield to Maturity
    price: Current bond price
    fv: Face Value
    T: Time to Maturity (years)
    coup: Annual coupon rate (%)
    credit_spread: Credit spread over risk-free rate (bps)
    freq: Payment frequency per year (2 = semi-annual)
    guess: Initial YTM guess
    """
    freq = float(freq)
    periods = T*freq
    coupon = coup/100*fv/freq
    spread_decimal = credit_spread/10000  # Convert bps to decimal
    
    dt = [(i+1)/freq for i in range(int(periods))]
    ytm_func = lambda y: sum([coupon/(1+(y+spread_decimal)/freq)**(freq*t) for t in dt]) + \
                        fv/(1+(y+spread_decimal)/freq)**(freq*T) - price
    return optimize.newton(ytm_func, guess)

def corp_price(fv, T, rf_rate, credit_spread, coup, freq=2):
    """Calculate corporate bond price given risk-free rate and credit spread
    fv: Face Value
    T: Time to maturity (years)
    rf_rate: Risk-free rate (decimal)
    credit_spread: Credit spread in basis points
    coup: Annual coupon rate (%)
    freq: Payment frequency per year
    """
    freq = float(freq)
    periods = T*freq
    coupon = coup/100*fv/freq
    spread_decimal = credit_spread/10000
    
    total_rate = rf_rate + spread_decimal
    dt = [(i+1)/freq for i in range(int(periods))]
    price = sum([coupon/(1+total_rate/freq)**(freq*t) for t in dt]) + \
            fv/(1+total_rate/freq)**(freq*T)
    return price

def credit_duration(price, par, T, coup, spread, freq=2, dy=0.0001):
    """Calculate credit spread duration
    Measures price sensitivity to changes in credit spread
    """
    spread_up = spread + dy*10000  # Convert to bps
    spread_down = spread - dy*10000
    
    price_up = corp_price(par, T, 0, spread_up, coup, freq)
    price_down = corp_price(par, T, 0, spread_down, coup, freq)
    
    credit_dur = -(price_up - price_down)/(2*price*dy)
    return credit_dur

def default_probability(credit_spread, recovery_rate=0.4):
    """Estimate annual default probability from credit spread
    Using simplified calculation: spread = PD * (1-RR)
    credit_spread: in basis points
    recovery_rate: expected recovery in default (decimal)
    """
    spread_decimal = credit_spread/10000
    pd = spread_decimal/(1-recovery_rate)
    return pd

def oas_price(fv, T, rf_rate, credit_spread, coup, volatility, freq=2, steps=50):
    """Calculate option-adjusted spread price
    Adds interest rate volatility consideration
    """
    dt = T/steps
    u = np.exp(volatility * np.sqrt(dt))
    d = 1/u
    p = (1 - d)/(u - d)
    
    rates = np.zeros(steps + 1)
    rates[0] = rf_rate
    
    for i in range(1, steps + 1):
        rates[i] = rates[i-1] * u
    
    prices = np.zeros(steps + 1)
    prices[:] = fv
    
    for i in range(steps-1, -1, -1):
        for j in range(i+1):
            r = rates[j]
            prices[j] = (p * prices[j+1] + (1-p) * prices[j]) * np.exp(-(r + credit_spread/10000) * dt)
            if i % (freq * T/steps) == 0:  # Add coupon payments
                prices[j] += coup/100 * fv/freq
    
    return prices[0]

def z_spread(price, treasury_curve, cash_flows, payment_times):
    """Calculate Z-spread over treasury curve"""
    def npv(spread):
        total = 0
        for cf, t in zip(cash_flows, payment_times):
            r = np.interp(t, [x[0] for x in treasury_curve], [x[1] for x in treasury_curve])
            # Ensure positive discount rate and proper scaling
            discount_rate = max(0.0001, r + spread/10000)  # Convert bps to decimal
            total += cf / ((1 + discount_rate/2)**(2*t))  # Semi-annual compounding
        return total - price
    
    try:
        return optimize.brentq(npv, 0, 500, maxiter=100)  # Increased max iterations
    except ValueError as e:
        print(f"Z-spread calculation failed: {e}")
        return None

###########################################
# Peer Comparison Data
###########################################

peer_data = {
    'Microsoft 2.921% 2060': {'spread': 82, 'rating': 'AAA'},
    'Amazon 2.70% 2060': {'spread': 88, 'rating': 'AA'},
    'Apple 2.55% 2060': {'spread': 80, 'rating': 'AA+'},
}

###########################################
# Treasury Curve Data
###########################################

treasury_curve = [
    (1, 0.0450),   # 1Y
    (2, 0.0455),   # 2Y
    (5, 0.0460),   # 5Y
    (10, 0.0465),  # 10Y
    (20, 0.0470),  # 20Y
    (30, 0.0479),  # 30Y
]

###########################################
# Analysis of Alphabet 2.25% 2060 Bond
###########################################

# Bond parameters
par = 100
T = 36.2  # Maturity in 2060 (about 36.2 years from now)
coup = 2.25  # 2.25% coupon
rf_rate = 0.0479  # Using 30Y Treasury yield as risk-free rate
credit_spread = 85  # Alphabet's AA2/AA+ rating spread (approximately)
freq = 2  # Semi-annual payments
recovery_rate = 0.4  # Standard senior unsecured recovery rate

# Calculate metrics
price = corp_price(par, T, rf_rate, credit_spread, coup, freq)
credit_dur = credit_duration(price, par, T, coup, credit_spread, freq)
pd = default_probability(credit_spread, recovery_rate)

print(f"Alphabet 2.25% 2060 Bond Analysis")
print(f"--------------------------------")
print(f"Price: ${price:.2f}")
print(f"Credit Duration: {credit_dur:.2f}")
print(f"Annual Default Probability: {pd*100:.4f}%")
print(f"Yield to Maturity: {(rf_rate + credit_spread/10000)*100:.2f}%")

# Create spread sensitivity analysis
spread_changes = np.arange(-500, 550, 50)  # -500 to +500 bps in 50bps steps
pct_changes = []

base_price = corp_price(par, T, rf_rate, credit_spread, coup, freq)
for ds in spread_changes:
    new_spread = credit_spread + ds
    new_price = corp_price(par, T, rf_rate, new_spread, coup, freq)
    pct_change = ((new_price / base_price) - 1) * 100
    pct_changes.append(pct_change)

# Additional Analysis
volatility = 0.15  # Interest rate volatility
oas_price = oas_price(par, T, rf_rate, credit_spread, coup, volatility)

# Calculate cash flows for Z-spread
payment_times = np.arange(0.5, T+0.5, 0.5)
cash_flows = [coup/100 * par/2] * len(payment_times)
cash_flows[-1] += par
z_spd = z_spread(price, treasury_curve, cash_flows, payment_times)

print("\nAdvanced Metrics")
print("---------------")
print(f"Option-Adjusted Price: ${oas_price:.2f}")
print(f"Z-spread: {z_spd:.0f} bps")

print("\nPeer Comparison")
print("--------------")
for name, data in peer_data.items():
    print(f"{name}: {data['spread']} bps ({data['rating']})")

###########################################
# Visualizations
###########################################

# 1. Credit Spread Sensitivity
plt.figure(figsize=(12, 8))
plt.style.use('classic')

plt.plot(spread_changes, pct_changes, 'b-', linewidth=2)
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

# Add markers for key spread changes
for ds in [-500, -250, 250, 500]:  # Adjusted marker points
    idx = np.where(spread_changes == ds)[0][0]
    pct = pct_changes[idx]
    plt.plot([ds, ds], [0, pct], 'k:', alpha=0.5)
    plt.text(ds + 5, pct, f'{pct:.1f}%',
            horizontalalignment='left' if ds > 0 else 'right',
            verticalalignment='bottom' if pct > 0 else 'top')

plt.grid(True, alpha=0.2)
plt.xlabel('Change in Credit Spread (bps)', fontsize=10)
plt.ylabel('Price Change (%)', fontsize=10)
plt.title(f'Alphabet 2.25% 2060 Credit Spread Sensitivity\nCurrent Spread: {credit_spread} bps',
          fontsize=12, pad=20)

plt.savefig('alphabet_spread_sensitivity.png',
            dpi=300,
            bbox_inches='tight',
            facecolor='white')
plt.close()

# 2. Interest Rate Sensitivity
rate_changes = np.arange(-4, 4.5, 0.5)  # Match treasury range of ±4%
rate_price_changes = []

base_price = corp_price(par, T, rf_rate, credit_spread, coup, freq)
for dr in rate_changes:
    new_rate = rf_rate + dr/100
    new_price = corp_price(par, T, new_rate, credit_spread, coup, freq)
    pct_change = ((new_price / base_price) - 1) * 100
    rate_price_changes.append(pct_change)

plt.figure(figsize=(12, 8))
plt.style.use('classic')

# Main price sensitivity curve
plt.plot(rate_changes, rate_price_changes, 'b-', linewidth=2)

# Reference lines
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

# Add markers and labels for 1% changes
for dr in range(-3, 4):
    if dr != 0:
        idx = np.where(rate_changes == dr)[0][0]
        pct = rate_price_changes[idx]
        # Vertical reference line
        plt.plot([dr, dr], [0, pct], 'k:', alpha=0.5)
        # Price change label with offset
        x_offset = -0.4 if dr < 0 else 0.4
        # Move all labels down by 40% of their value
        y_offset = pct * -0.4  # Negative to move down
        plt.text(dr + x_offset, pct + y_offset, f'{pct:.1f}%', 
                horizontalalignment='right' if dr < 0 else 'left',
                verticalalignment='bottom' if pct > 0 else 'top')

plt.grid(True, alpha=0.2)
plt.xlabel('Change in Yield (%)', fontsize=10)
plt.ylabel('Price Change (%)', fontsize=10)
plt.title(f'Alphabet 2.25% 2060 Price Sensitivity\nCurrent Price: ${base_price:.2f}, YTM: {(rf_rate + credit_spread/10000)*100:.2f}%',
          fontsize=12, pad=20)

plt.savefig('alphabet_rate_sensitivity.png',
            dpi=300,
            bbox_inches='tight',
            facecolor='white')
plt.close()

# 3. Peer Comparison
plt.figure(figsize=(12, 6))

peers = list(peer_data.keys()) + ['Alphabet 2.25% 2060']
spreads = [data['spread'] for data in peer_data.values()] + [credit_spread]
ratings = [data['rating'] for data in peer_data.values()] + ['AA2/AA+']

# Create horizontal bar chart
y_pos = np.arange(len(peers))
plt.barh(y_pos, spreads, alpha=0.6)
plt.yticks(y_pos, peers)

# Add spread and rating labels
for i, v in enumerate(spreads):
    plt.text(v + 1, i, f'{v}bps\n{ratings[i]}', va='center')

plt.xlabel('Credit Spread (bps)', fontsize=10)
plt.title('Tech Mega-Cap Long-Duration Bond Comparison', fontsize=12)
plt.grid(True, alpha=0.2, axis='x')

plt.savefig('alphabet_peer_comparison.png',
            dpi=300,
            bbox_inches='tight',
            facecolor='white')
plt.close()

# 4. Combined Sensitivity Analysis
plt.figure(figsize=(12, 8))
plt.style.use('classic')

# Create rate and spread combinations
rate_changes = np.arange(-2, 2.5, 0.5)  # Smaller range for readability
spread_changes = np.array([-500, -250, 0, 250, 500])  # Key spread changes in bps

# Create matrix of price changes
combined_changes = np.zeros((len(spread_changes), len(rate_changes)))
for i, ds in enumerate(spread_changes):
    for j, dr in enumerate(rate_changes):
        new_rate = rf_rate + dr/100
        new_spread = credit_spread + ds
        new_price = corp_price(par, T, new_rate, new_spread, coup, freq)
        pct_change = ((new_price / base_price) - 1) * 100
        combined_changes[i, j] = pct_change

# Plot multiple lines for different spread scenarios
for i, ds in enumerate(spread_changes):
    label = f'Spread {ds:+d}bps'
    plt.plot(rate_changes, combined_changes[i], linewidth=2, 
            label=label, alpha=0.8)

# Reference lines
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)

# Add markers for current point
plt.plot([0], [0], 'ko', label='Current')

plt.grid(True, alpha=0.2)
plt.xlabel('Change in Interest Rate (%)', fontsize=10)
plt.ylabel('Price Change (%)', fontsize=10)
plt.title(f'Alphabet 2.25% 2060 Combined Sensitivity Analysis\nCurrent Price: ${base_price:.2f}, YTM: {(rf_rate + credit_spread/10000)*100:.2f}%',
          fontsize=12, pad=20)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig('alphabet_combined_sensitivity.png',
            dpi=300,
            bbox_inches='tight',
            facecolor='white')
plt.close()

# Add more corporate-specific functions...

