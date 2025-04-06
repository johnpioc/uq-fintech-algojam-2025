import numpy as np
from sklearn.linear_model import LinearRegression


# Custom trading Algorithm
class Algorithm():
    # FUNCTION TO SETUP ALGORITHM CLASS
    def __init__(self, positions):
        # Initialise data stores:
        # Historical data of all instruments
        self.data = {}
        # Initialise position limits
        self.positionLimits = {}
        # Initialise the current day as 0
        self.day = 0
        # Initialise the current positions
        self.positions = positions
        self.last_prices = {}
        self.pnl_history = {}

    # Helper function to fetch the current price of an instrument
    def get_current_price(self, instrument):
        # return most recent price
        return self.data[instrument][-1]

    ########################################################

    ### HELPER FUNCTIONS ###
    def get_rolling_mean(self, instrument_name: str, window: int = 20) -> float:
        if self.day < window - 1:
            return np.mean(self.data[instrument_name][:self.day + 1])
        return np.mean(self.data[instrument_name][self.day - window + 1:self.day + 1])

    def get_rolling_std(self, instrument_name: str, window: int = 20) -> float:
        if self.day < window - 1:
            return np.std(self.data[instrument_name][:self.day + 1])
        return np.std(self.data[instrument_name][self.day - window + 1:self.day + 1])

    def get_z_score(self, instrument_name: str, window: int = 20) -> float:
        current_price = self.get_current_price(instrument_name)
        rolling_mean = self.get_rolling_mean(instrument_name, window)
        rolling_std = self.get_rolling_std(instrument_name, window)
        return (current_price - rolling_mean) / rolling_std if rolling_std > 0 else 0

    ### GET POSITIONS FUNCTIONS ####

    def get_uq_dollar_positions(self) -> int:
        instrument_name = "UQ Dollar"
        z_score = self.get_z_score(instrument_name, 20)
        if z_score < -1.5:  # Buy when significantly below mean
            return self.positionLimits[instrument_name]
        elif z_score > 1.5:  # Sell when significantly above mean
            return -self.positionLimits[instrument_name]
        return 0

    def get_dawg_food_positions(self) -> int:
        instrument_name: str = "Dawg Food"
        mean_window = 3
        threshold = 0.01

        rolling_mean = np.mean(self.data[instrument_name][-mean_window:])
        current_price = self.get_current_price(instrument_name)

        if current_price < rolling_mean * (1 - threshold):
            return self.positionLimits[instrument_name]
        elif current_price > rolling_mean * (1 + threshold):
            return -self.positionLimits[instrument_name]
        else:
            return 0

    def get_fintech_token_positions(self) -> int:
        instrument_name: str = "Fintech Token"

        mean_window = 5
        threshold = 0.001

        rolling_mean = np.mean(self.data[instrument_name][-mean_window:])
        current_price = self.get_current_price(instrument_name)

        if current_price < rolling_mean * (1 - threshold):
            return self.positionLimits[instrument_name]
        elif current_price > rolling_mean * (1 + threshold):
            return -self.positionLimits[instrument_name]
        else:
            return 0

    def get_fried_chicken_positions(self) -> int:
        if len(self.data['Fried Chicken']) < 20:
            return 0

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

        threshold = 1.0
        if z_score > threshold:
            return -int(self.positionLimits["Fried Chicken"] * min(1.0, z_score / 3))
        elif z_score < -threshold:
            return int(self.positionLimits["Fried Chicken"] * min(1.0, abs(z_score) / 3))
        else:
            return 0

    def get_raw_chicken_positions(self) -> int:
        instrument_name: str = "Raw Chicken"

        if self.data[instrument_name][-2] > self.data[instrument_name][-1]:
            return self.positionLimits[instrument_name]
        else:
            return -self.positionLimits[instrument_name]

    def get_secret_spices_positions(self) -> int:
        instrument_name: str = "Secret Spices"
        mean_window = 3
        threshold = 0.0001

        rolling_mean = np.mean(self.data[instrument_name][-mean_window:])
        current_price = self.get_current_price(instrument_name)

        if current_price < rolling_mean * (1 - threshold):
            return self.positionLimits[instrument_name]
        elif current_price > rolling_mean * (1 + threshold):
            return -self.positionLimits[instrument_name]
        else:
            return 0

    def get_goober_eats_positions(self) -> int:
        instrument_name: str = "Goober Eats"
        mean_window = 30
        threshold = 0.005

        rolling_mean = np.mean(self.data[instrument_name][-mean_window:])
        current_price = self.get_current_price(instrument_name)

        if current_price < rolling_mean * (1 - threshold):
            return self.positionLimits[instrument_name]
        elif current_price > rolling_mean * (1 + threshold):
            return -self.positionLimits[instrument_name]
        else:
            return 0


    def get_quack_positions(self) -> int:
        instrument_name: str = "Quantum Universal Algorithmic Currency Koin"

        if self.data[instrument_name][-2] > self.data[instrument_name][-1]:
            return self.positionLimits[instrument_name]
        else:
            return -self.positionLimits[instrument_name]

    def get_purple_elixir_positions(self) -> int:
        instrument_name: str = "Purple Elixir"
        mean_window = 5
        threshold = 0.005

        rolling_mean = np.mean(self.data[instrument_name][-mean_window:])
        current_price = self.get_current_price(instrument_name)

        if current_price < rolling_mean * (1 - threshold):
            return self.positionLimits[instrument_name]
        elif current_price > rolling_mean * (1 + threshold):
            return -self.positionLimits[instrument_name]
        else:
            return 0

    def get_rare_watch_positions(self) -> int:
        instrument_name: str = "Rare Watch"

        mean_window = 5
        threshold = 0.001

        rolling_mean = np.mean(self.data[instrument_name][-mean_window:])
        current_price = self.get_current_price(instrument_name)

        if current_price < rolling_mean * (1 - threshold):
            return -self.positionLimits[instrument_name]
        elif current_price > rolling_mean * (1 + threshold):
            return self.positionLimits[instrument_name]
        else:
            return 0

    # RETURN DESIRED POSITIONS IN DICT FORM
    def get_positions(self):
        # Get current position
        currentPositions = self.positions
        # Get position limits
        positionLimits = self.positionLimits

        # Declare a store for desired positions
        desiredPositions = {}

        # Loop through all the instruments you can take positions on.
        for instrument, positionLimit in positionLimits.items():
            # For each instrument initilise desired position to zero
            desiredPositions[instrument] = 0

        # IMPLEMENT CODE HERE TO DECIDE WHAT POSITIONS YOU WANT
        #######################################################################
        # Display the current trading day
        print("Starting Algorithm for Day:", self.day)

        # I only want to trade the UQ Dollar
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

        # Display the prices of instruments I want to trade
        for ins in trade_instruments:
            print(f"{ins}: ${self.get_current_price(ins)}")

        # Start trading from Day 2 onwards. Buy if it goes down, sell if it goes up.
        if self.day < 2: return desiredPositions

        # Get some initial positions
        desiredPositions["UQ Dollar"] = self.get_uq_dollar_positions()
        desiredPositions["Dawg Food"] = self.get_dawg_food_positions()
        desiredPositions["Fintech Token"] = self.get_fintech_token_positions()
        desiredPositions["Fried Chicken"] = self.get_fried_chicken_positions()
        desiredPositions["Raw Chicken"] = self.get_raw_chicken_positions()
        desiredPositions["Secret Spices"] = self.get_secret_spices_positions()
        desiredPositions["Goober Eats"] = self.get_goober_eats_positions()
        desiredPositions["Quantum Universal Algorithmic Currency Koin"] = self.get_quack_positions()
        desiredPositions["Purple Elixir"] = self.get_purple_elixir_positions()
        desiredPositions["Rare Watch"] = self.get_rare_watch_positions()

        # capital optimisation
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
                            if self.data[ins][-2] > self.data[ins][-1]:
                                desiredPositions[ins] = int(additional_value / current_price)
                            else:
                                desiredPositions[ins] = -int(additional_value / current_price)
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

        # Display the end of trading day
        print("Ending Algorithm for Day:", self.day, "\n")
        #######################################################################
        # Return the desired positions
        return desiredPositions
