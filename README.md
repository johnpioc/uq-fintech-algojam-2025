# UQ Fintech AlgoJam

@CianWC and I participated in the UQ Fintech Algojam 2025 and this repository contains our trading algorithm written in Python. 

### Trading Strategy

We kept our trading strategy quite simple, using the following methods:

- **Mean Reversion**, using different windows for different instruments which worked well for highly volatile and noisy assets
- **Linear Regression** - we found that the instrument "Fried Chicken" tied it's value to two other assets, "Secret Spices" and "Raw Chicken". Using a linear regression model, we forecasted what the price of Fried Chicken should be using the prices of Raw Chicken and Secret Spices, and traded based on that forecasted price and the actual entry price.
- In most instruments, we used a strategy to buy an asset if it's price has decreased compared to the day before, and sold an asset if it's price has increased

### Returns

The competition was structured in a way where total price data spanned over two years, however we were only given the data for the first year.

Therefore, we had to create a strategy that not only optimised returns for the first year, but also gave us the best chance possible to achieve the highest returns on the unseen data (second year)

**1st Year Returns:** $2.55 million 

**2nd Year Returns:** TBD