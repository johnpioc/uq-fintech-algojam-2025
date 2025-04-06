import numpy as np
from sklearn.linear_model import LinearRegression


class Algorithm():
    def __init__(self, positions):
        self.data = {}
        self.positionLimits = {}
        self.day = 0
        self.positions = positions
        self.last_prices = {}
        self.pnl_history = {}

    def get_current_price(self, instrument):
        return self.data[instrument][-1]

    def get_positions(self):
        currentPositions = self.positions
        positionLimits = self.positionLimits
        desiredPositions = {ins: 0 for ins in positionLimits}

        trade_instruments = [
            "Dawg Food", "Raw Chicken", "Secret Spices", "Fried Chicken",
            "Goober Eats", "UQ Dollar", "Purple Elixir",
            "Quantum Universal Algorithmic Currency Koin", "Fintech Token"
        ]

        # Update PNL tracking
        if self.day >= 1:
            for ins in trade_instruments:
                if len(self.data[ins]) >= 2 and ins in self.last_prices and ins in currentPositions:
                    price_change = self.data[ins][-1] - self.last_prices[ins]
                    daily_pnl = price_change * currentPositions[ins]
                    if ins not in self.pnl_history:
                        self.pnl_history[ins] = []
                    self.pnl_history[ins].append(daily_pnl)
                    self.last_prices[ins] = self.data[ins][-1]

        for ins in trade_instruments:
            print(f"{ins}: ${self.get_current_price(ins)}")

        # Strategy
        if self.day >= 2:
            for ins in trade_instruments:
                if ins == "Purple Elixir":
                    self.adaptive_mean_reversion(desiredPositions, ins, 5, positionLimits, 0.005)
                elif ins == "Dawg Food":
                    self.adaptive_mean_reversion(desiredPositions, ins, 3, positionLimits, 0.01)
                elif ins == "Goober Eats":
                    self.adaptive_mean_reversion(desiredPositions, ins, 30, positionLimits, 0.005)
                elif ins == "Fried Chicken":
                    self.fried_chicken_arbitrage(desiredPositions, positionLimits)
                elif ins == "Secret Spices":
                    self.Rolling_Mean(desiredPositions, ins, 3, positionLimits, 0.0001)
                elif ins == "Fintech Token":
                    self.Rolling_Mean(desiredPositions, ins, 5, positionLimits, 0.001)
                else:
                    desiredPositions[ins] = positionLimits[ins] if self.data[ins][-2] > self.data[ins][-1] else - \
                    positionLimits[ins]

        # Budget optimization with dynamic PNL/unit
        total_value = sum(abs(desiredPositions[ins] * self.get_current_price(ins)) for ins in desiredPositions)
        if total_value > 0:
            if total_value > 600000:
                scale_factor = 600000 / total_value
                for ins in desiredPositions:
                    desiredPositions[ins] = max(-positionLimits[ins],
                                                min(positionLimits[ins], int(desiredPositions[ins] * scale_factor)))
            elif total_value < 600000:
                remaining_budget = 600000 - total_value
                pnl_per_unit = {}
                for ins in trade_instruments:
                    if ins in self.pnl_history and self.pnl_history[ins]:
                        window = min(30, len(self.pnl_history[ins]))
                        total_pnl = sum(self.pnl_history[ins][-window:])
                        pnl_per_unit[ins] = abs(total_pnl / positionLimits[ins]) if total_pnl != 0 else 0.01
                    else:
                        pnl_per_unit[ins] = 0.01

                priority_order = sorted(trade_instruments,
                                        key=lambda ins: pnl_per_unit[ins] * (
                                                    1 + 0.2 * abs(desiredPositions[ins] / positionLimits[ins])),
                                        reverse=True)
                for ins in priority_order:
                    if remaining_budget <= 0:
                        break
                    current_price = self.get_current_price(ins)
                    if desiredPositions[ins] == 0:
                        max_value = abs(positionLimits[ins] * current_price)
                        additional_value = min(remaining_budget, max_value)
                        if additional_value > 0:
                            desiredPositions[ins] = int(additional_value / current_price) if self.data[ins][-2] > \
                                                                                             self.data[ins][
                                                                                                 -1] else -int(
                                additional_value / current_price)
                            desiredPositions[ins] = max(-positionLimits[ins],
                                                        min(positionLimits[ins], desiredPositions[ins]))
                            remaining_budget -= abs(desiredPositions[ins] * current_price)
                    elif abs(desiredPositions[ins]) < positionLimits[ins]:
                        current_value = abs(desiredPositions[ins] * current_price)
                        max_additional_value = abs(positionLimits[ins] * current_price) - current_value
                        additional_value = min(remaining_budget, max_additional_value)
                        if additional_value > 0:
                            direction = 1 if desiredPositions[ins] > 0 else -1
                            additional_units = int(additional_value / current_price)
                            desiredPositions[ins] += direction * additional_units
                            desiredPositions[ins] = max(-positionLimits[ins],
                                                        min(positionLimits[ins], desiredPositions[ins]))
                            remaining_budget -= abs(additional_units * current_price)

        for ins in trade_instruments:
            pos_percent = round(abs(desiredPositions[ins] / positionLimits[ins] * 100)) if positionLimits[
                                                                                               ins] > 0 else 0
            print(f"{ins}: Position {desiredPositions[ins]} ({pos_percent}% of limit)")

        print("Ending Algorithm for Day:", self.day, "\n")
        return desiredPositions

    def Rolling_Mean(self, desiredPositions, ins, mean_window, positionLimits, threshold):
        rolling_mean = np.mean(self.data[ins][-mean_window:])
        current_price = self.get_current_price(ins)
        if current_price < rolling_mean * (1 - threshold):
            desiredPositions[ins] = positionLimits[ins]
        elif current_price > rolling_mean * (1 + threshold):
            desiredPositions[ins] = -positionLimits[ins]
        else:
            desiredPositions[ins] = 0

    def adaptive_mean_reversion(self, desiredPositions, ins, mean_window, positionLimits, threshold):
        rolling_mean = np.mean(self.data[ins][-mean_window:])
        current_price = self.get_current_price(ins)
        deviation = (current_price - rolling_mean) / rolling_mean
        if deviation < -threshold:
            position_scale = min(1.0, abs(deviation) / (threshold * 3))
            desiredPositions[ins] = int(positionLimits[ins] * position_scale)
        elif deviation > threshold:
            position_scale = min(1.0, abs(deviation) / (threshold * 3))
            desiredPositions[ins] = -int(positionLimits[ins] * position_scale)
        else:
            desiredPositions[ins] = 0

    def fried_chicken_arbitrage(self, desiredPositions, positionLimits):
        if len(self.data['Fried Chicken']) < 20:
            return

        X = np.array([
            [self.data['Secret Spices'][i], self.data['Raw Chicken'][i]]
            for i in range(len(self.data['Fried Chicken']))
        ])
        y = np.array(self.data['Fried Chicken'])

        model = LinearRegression()
        model.fit(X, y)
        pred = model.predict(X)

        spread = y - pred
        z_score = (spread[-1] - np.mean(spread[-20:])) / np.std(spread[-20:])

        print(
            f"[Fried Chicken Model] fried ≈ {model.coef_[0]:.4f} × spices + {model.coef_[1]:.4f} × raw + {model.intercept_:.4f}")
        print(f"[Z-Score] Spread z-score: {z_score:.4f}")

        threshold = 1.0
        if z_score > threshold:
            desiredPositions["Fried Chicken"] = -int(positionLimits["Fried Chicken"] * min(1.0, z_score / 3))
        elif z_score < -threshold:
            desiredPositions["Fried Chicken"] = int(positionLimits["Fried Chicken"] * min(1.0, abs(z_score) / 3))
        else:
            desiredPositions["Fried Chicken"] = 0
