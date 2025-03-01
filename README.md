# Treasury Bond Price Sensitivity Analysis

A Python tool for analyzing how US Treasury bond prices respond to changes in interest rates, with a focus on the 1.25% Treasury maturing in 2050.

## Overview

This project provides tools to analyze and visualize:
- Price sensitivity to yield changes
- Modified duration and convexity effects
- Linear vs actual price approximations

![Treasury Price Sensitivity](treasury_sensitivity.png)

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
git clone https://github.com/tmopencell/treasury-analysis.git
cd treasury-analysis
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
