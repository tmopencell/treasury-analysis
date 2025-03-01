# Treasury and Corporate Bond Analysis

A Python tool for analyzing bond price sensitivity to market changes, focusing on two case studies:
1. US Treasury 1.25% 2050 - Pure interest rate risk
2. Alphabet 2.25% 2060 - Combined interest rate and credit risk

## Understanding Bond Price Sensitivity

### What Makes Bond Prices Move?
Bond prices change primarily due to two factors:
1. Interest Rate Changes (affects all bonds)
2. Credit Risk Changes (affects corporate bonds only)

### Interest Rate Risk and Convexity
When interest rates change, bond prices move in the opposite direction. This relationship is captured by two key metrics:

1. **Duration**: The first-order (linear) price sensitivity
   - Example: A duration of 17.89 means a 1% rise in rates should cause a 17.89% price decline
   - Works well for small rate changes
   - Simple rule: Price Change ≈ -Duration × Rate Change
   - Linear approximation becomes less accurate for larger moves

2. **Convexity**: The bond price's curvature effect
   - Makes bonds more valuable by creating an asymmetric return profile
   - Helps in two ways:
     * Limits price declines when rates rise
     * Enhances price gains when rates fall
   - More important for longer-dated bonds
   - Example from our Treasury analysis:
     * 4% rate rise = 55% price decline
     * 4% rate fall = 89% price gain
     * Without convexity, both would be about 72%

![Treasury Price Sensitivity](treasury_sensitivity.png)

### Credit Risk: The Corporate Bond Component
Corporate bonds face an additional risk: changes in the company's creditworthiness.

1. **Credit Spreads Explained**:
   - Extra yield investors demand over Treasury rates
   - Measured in basis points (bps) where 100 bps = 1%
   - Reflects market's view of company's credit risk
   - Example: Alphabet's 85 bps spread means investors demand 0.85% extra yield
   - Fun fact: While negative spreads seem implausible (why pay more for more risk?), 
     they're not impossible! With Alphabet (AA2/AA+) and the US Treasury (Aaa/AA+) 
     sharing an S&P rating, we're just one more US downgrade away from some 
     interesting conversations about what "risk-free" really means! 😉

2. **Credit Spread Sensitivity**
![Credit Spread Sensitivity](alphabet_spread_sensitivity.png)
- Shows how Alphabet bond price changes with credit spread moves
- Wide range (±500bps) captures stress scenarios like:
  * Credit rating downgrades
  * Market stress periods
  * Industry-specific challenges
- Similar convex shape to interest rate sensitivity

3. **Combined Risk Analysis**
![Combined Sensitivity](alphabet_combined_sensitivity.png)
- Real-world scenario analysis
- Shows five different credit spread scenarios
- Each line shows rate sensitivity at that spread level
- Key observations:
  * Risks can compound (rates up + spreads wider)
  * Or offset (rates up + spreads tighter)
  * Stress scenarios often see both moving adversely

4. **Peer Comparison Context**
![Peer Comparison](alphabet_peer_comparison.png)
- Compares major tech companies' credit spreads
- Shows relative market perception of credit risk
- Tighter spread = Lower perceived risk
- Current spreads (in bps):
  * Microsoft (AAA): 82
  * Apple (AA+): 80
  * Alphabet (AA2/AA+): 85
  * Amazon (AA): 88

### Practical Implications

1. **For Investors**:
   - Long-duration bonds offer higher potential returns but more risk
   - Credit spread exposure adds another return/risk dimension
   - Convexity provides some protection against large adverse moves
   - Need to consider both risks when evaluating corporate bonds

2. **Risk Management**:
   - Duration measures first-order rate risk
   - Credit spread duration measures first-order credit risk
   - Convexity important for large market moves
   - Combined analysis essential for stress testing

3. **Market Context**:
   - Current environment features:
     * Elevated rate volatility
     * Changing credit conditions
     * Tech sector evolution
   - Makes understanding these sensitivities crucial

## Overview

This project provides tools to analyze and visualize:
- Price sensitivity to yield changes
- Modified duration and convexity effects
- Linear vs actual price approximations

## Key Features

### Bond Mathematics
- Zero-coupon bond pricing
- Yield to Maturity (YTM) calculation using Newton's method
- Modified duration calculation
- Convexity analysis

### Analysis Tools
- Price change predictions using:
  - Linear approximation (duration only)
  - Convexity-adjusted approximation
  - Exact calculation
- Visual representation of price sensitivity
- Detailed comparative analysis table

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tmopencell/bondmath.git
cd bondmath
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the analysis:
```bash
python src/bondmath.py
```

This will generate:
1. A table showing price changes for different yield scenarios
2. A visualization saved as 'treasury_sensitivity.png'

## Sample Output
```
Current YTM: 4.7897%
Modified Duration: 17.8943
Convexity: 441.7098

Rate Change | Linear Approx | With Convexity | Actual Price | % Change
---------------------------------------------------------------------------
-3%        | $ 2685.86  | $ 2884.64  | $  67.91 | +35.71%
-2%        | $ 1790.57  | $ 1932.41  | $  60.93 | +21.77%
-1%        | $  895.29  | $ 1028.17  | $  54.31 |  +8.54%
+1%        | $ -895.29  | $ -883.18  | $  46.37 |  -7.33%
+2%        | $-1790.57  | $-1766.36  | $  43.23 | -13.60%
+3%        | $-2685.86  | $-2649.54  | $  40.53 | -19.00%
```

## Technical Details

### Bond Pricing Formula
The price of a bond is calculated as the present value of all future cash flows:

P = Σ(C/(1+y)^t) + F/(1+y)^T

Where:
- C = Coupon payment
- y = Yield to maturity
- t = Time to each payment
- F = Face value
- T = Time to maturity

### Modified Duration
Measures the percentage price change for a 1% change in yield:

Modified Duration = -(1/P)(dP/dy)

### Convexity
Measures the curvature of the price-yield relationship:

Convexity = (1/P)(d²P/dy²)

## Requirements
- Python 3.x
- NumPy
- SciPy
- Matplotlib

## License
MIT

## Author
tmopencell

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Developed Market Bonds and Inflation-Protected Securities

### UK Government Bonds
Analysis of ultra-long dated nominal and inflation-linked Gilts, focusing on:
1. UKT 0.5% 2061 - A low-coupon, long-duration conventional Gilt
2. UKTI 0.125% 2073 - An ultra-long inflation-linked Gilt

#### Nominal Gilt Analysis
![UK Gilt Sensitivity](uk_gilt_sensitivity.png)
- Shows extreme duration risk in ultra-long, low-coupon bonds
- Price changes are highly asymmetric due to convexity
- Marks the yield change required to reach par (100 pence)
- Demonstrates why these bonds are favored by liability-matching investors

#### Inflation-Linked Gilt Analysis
Three key risk factors analyzed:

1. **Real Yield Sensitivity**
![UK Linker Sensitivity](uk_linker_sensitivity.png)
- Shows price response to changes in real yields
- Demonstrates even greater duration risk than nominal bonds
- Particularly relevant given current negative real yields

2. **Inflation Sensitivity**
![UK Inflation Sensitivity](uk_inflation_sensitivity.png)
- Direct price impact of changing inflation expectations
- Critical for understanding inflation protection mechanics
- Shows upside potential in high inflation scenarios

3. **Breakeven Analysis**
![UK Breakeven Analysis](uk_breakeven_analysis.png)
- Compares nominal vs inflation-linked bond values
- Shows breakeven inflation rate (where returns equalize)
- Includes historical context with recent RPI peaks
- Helps assess relative value between nominal and real bonds

### Key Market Features

1. **Ultra-Long Duration**
   - Both bonds have extreme interest rate sensitivity
   - Small yield changes create large price movements
   - Convexity effects are particularly pronounced
   - Critical for pension fund liability matching

2. **Inflation Protection**
   - Index-linked Gilts provide direct inflation hedge
   - Principal and coupons adjust with UK RPI
   - Currently showing negative real yields
   - Popular with inflation-sensitive investors

3. **Market Context**
   - Current nominal yield: 4.45% (UKT 0.5% 2061)
   - Current real yield: -1.75% (UKTI 0.125% 2073)
   - RPI inflation: 4.1%
   - Breakeven inflation rate provides market's inflation forecast

4. **Investment Implications**
   - Duration risk management is crucial
   - Inflation expectations drive relative value
   - Negative real yields reflect high inflation protection demand
   - Breakeven rates help assess relative value

### Understanding Inflation Protection (or "Why Your Money Might Not Buy That Coffee Tomorrow")

Imagine you lend someone $100 today, and they promise to pay you back $105 in a year. Sounds good, right? 
Well... what if a cup of coffee that costs $5 today costs $6 next year? 🤔

This is where inflation-protected bonds come in, and they're basically the bond market saying "We got you!"

#### How It Works (A Simple Story)
1. **Regular Bond**: 
   - You lend $100
   - Get $2 each year (2% coupon)
   - Get $100 back at the end
   - Meanwhile, inflation is eating your lunch (literally!)

2. **Inflation-Protected Bond**:
   - You lend $100
   - The $100 grows with inflation
   - Your coupons grow with inflation
   - It's like having a tiny economist adjusting your returns daily

#### Real World Example: UKTI 0.125% 2073
- Looks like a tiny 0.125% coupon (yes, that's not a typo!)
- But... both principal and coupons adjust with UK RPI
- If inflation is 4.1%:
  * Your £100 investment is now worth £104.10
  * Your coupon is 0.125% of £104.10
  * Next year, both will adjust again
  * And again... (for 50 years!)

#### The Plot Twist: Negative Real Yields
Current real yield of -1.75% means investors are saying:
- "Inflation protection is so valuable..."
- "...we'll pay extra for it..."
- "...even though we know we'll lose 1.75% per year in real terms!"
- (This is like paying for insurance on your coffee budget 😉)

#### Why This Matters (Beyond Coffee)
Consider pension funds:
- Promise to pay retirees for 30+ years
- Need to match future inflation-linked payments
- Can't just hope inflation behaves
- Would rather lose a little in real terms than risk losing a lot in inflation terms
