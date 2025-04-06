import numpy as np
from typing import List
import math
# Custom trading Algorithm
class Algorithm():

    ########################################################
    # NO EDITS REQUIRED TO THESE FUNCTIONS
    ########################################################
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

        # RARE WATCH INITIALISATIONS
        self.last_rare_watch_exit = 0
    # Helper function to fetch the current price of an instrument
    def get_current_price(self, instrument):
        # return most recent price
        return self.data[instrument][-1]
    ########################################################

    def get_uq_dollar_positions(self) -> int:
        instrument_name: str = "UQ Dollar"

        if self.data[instrument_name][-2] > self.data[instrument_name][-1]:
            return self.positionLimits[instrument_name]
        else:
            return -self.positionLimits[instrument_name]

    def get_dawg_food_positions(self) -> int:
        instrument_name: str = "Dawg Food"

        if self.data[instrument_name][-2] > self.data[instrument_name][-1]:
            return self.positionLimits[instrument_name]
        else:
            return -self.positionLimits[instrument_name]

    def get_fintech_token_positions(self) -> int:
        instrument_name: str = "Fintech Token"

        if self.data[instrument_name][-2] > self.data[instrument_name][-1]:
            return self.positionLimits[instrument_name]
        else:
            return -self.positionLimits[instrument_name]

    def get_fried_chicken_positions(self) -> int:
        instrument_name: str = "Fried Chicken"

        if self.data[instrument_name][-2] > self.data[instrument_name][-1]:
            return self.positionLimits[instrument_name]
        else:
            return -self.positionLimits[instrument_name]

    def get_raw_chicken_positions(self) -> int:
        instrument_name: str = "Raw Chicken"

        if self.data[instrument_name][-2] > self.data[instrument_name][-1]:
            return self.positionLimits[instrument_name]
        else:
            return -self.positionLimits[instrument_name]

    def get_secret_spices_positions(self) -> int:
        instrument_name: str = "Secret Spices"

        if self.data[instrument_name][-2] > self.data[instrument_name][-1]:
            return self.positionLimits[instrument_name]
        else:
            return -self.positionLimits[instrument_name]

    def get_goober_eats_positions(self) -> int:
        instrument_name: str = "Goober Eats"

        if self.data[instrument_name][-2] > self.data[instrument_name][-1]:
            return self.positionLimits[instrument_name]
        else:
            return -self.positionLimits[instrument_name]


    def get_quack_positions(self) -> int:
        instrument_name: str = "Quantum Universal Algorithmic Currency Koin"

        if self.data[instrument_name][-2] > self.data[instrument_name][-1]:
            return self.positionLimits[instrument_name]
        else:
            return -self.positionLimits[instrument_name]

    def get_purple_elixir_positions(self) -> int:
        instrument_name: str = "Purple Elixir"

        if self.data[instrument_name][-2] > self.data[instrument_name][-1]:
            return self.positionLimits[instrument_name]
        else:
            return -self.positionLimits[instrument_name]

    # Gets rolling mean of an instrument over the last 20 days
    def get_rolling_mean(self, instrument_name: str) -> float:
        sum: float = 0

        start_day: int
        num_days: int

        if self.day < 19:
            start_day = 0
            num_days = self.day + 1
        else:
            start_day = self.day - 20
            num_days = 20

        end_day: int = self.day

        for day in range(start_day, end_day + 1):
            sum += self.data[instrument_name][day]

        return sum / num_days

    def get_rolling_standard_deviation(self, instrument_name: str) -> float:
        rolling_mean: float = self.get_rolling_mean(instrument_name)
        start_day: int
        num_days: int

        if self.day < 19:
            start_day = 0
            num_days = self.day + 1
        else:
            start_day = self.day -20
            num_days = 20

        end_day: int = self.day

        sum: float = 0

        for day in range(start_day, end_day + 1):
            current_price: float = self.data[instrument_name][day]
            sum += math.pow(current_price - rolling_mean, 2)

        return math.sqrt((1/num_days) * sum)



    # Gets Z score of an instrument over the last 20 days
    def get_z_score(self, instrument_name: str) -> float:

        current_price: float = self.get_current_price(instrument_name)
        rolling_mean: float = self.get_rolling_mean(instrument_name)
        rolling_standard_deviation: float = self.get_rolling_standard_deviation(instrument_name)

        return (current_price - rolling_mean) / rolling_standard_deviation


    def get_rare_watch_positions(self) -> int:
        instrument_name: str = "Rare Watch"

        current_price: float = self.get_current_price(instrument_name)
        z_score: float = self.get_z_score(instrument_name)
        rolling_std: float = self.get_rolling_standard_deviation(instrument_name)
        position_limit: int = self.positionLimits[instrument_name]
        current_position: int = self.positions[instrument_name]

        # --- Risk Control Flags ---
        max_drawdown = 3 * rolling_std
        max_volatility = 5.0  # Adjust threshold as needed
        cooldown_period = 5
        adaptive_positioning = True

        # --- Volatility Filter: Avoid trading in high-vol zones ---
        if rolling_std > max_volatility:
            return current_position  # stay flat or hold

        # --- Spike Guard: Stop-loss if unrealized PnL is deeply negative ---
        if current_position != 0:
            entry_price = self.get_current_price(instrument_name)
            unrealized_pnl = (current_price - entry_price) * current_position
            if unrealized_pnl < -max_drawdown:
                self.last_rare_watch_exit = self.day
                return 0  # exit immediately

        # --- Cooldown: Wait a few days after closing a position ---
        if self.day - self.last_rare_watch_exit < cooldown_period:
            return current_position

        # --- Entry / Exit Logic ---
        if z_score > 1:
            size = position_limit
            if adaptive_positioning:
                size = int(position_limit / (1 + z_score ** 2))
            return size

        elif z_score < -1:
            size = -position_limit
            if adaptive_positioning:
                size = int(-position_limit / (1 + z_score ** 2))
            return size

        elif -0.5 < z_score < 0.5:
            self.last_rare_watch_exit = self.day
            return 0  # Exit when near the mean

        else:
            return current_position


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
        trade_instruments = ["UQ Dollar"]
        
        # Display the prices of instruments I want to trade
        for ins in trade_instruments:
            print(f"{ins}: ${self.get_current_price(ins)}")
        
        # Start trading from Day 2 onwards. Buy if it goes down, sell if it goes up.
        if self.day >= 2:
            # desiredPositions["UQ Dollar"] = self.get_uq_dollar_positions()
            # desiredPositions["Dawg Food"] = self.get_dawg_food_positions()
            # desiredPositions["Fintech Token"] = self.get_fintech_token_positions()
            # desiredPositions["Fried Chicken"] = self.get_fried_chicken_positions()
            # desiredPositions["Raw Chicken"] = self.get_raw_chicken_positions()
            # desiredPositions["Secret Spices"] = self.get_secret_spices_positions()
            # desiredPositions["Goober Eats"] = self.get_goober_eats_positions()
            # desiredPositions["Quantum Universal Algorithmic Currency Koin"] = self.get_quack_positions()
            # desiredPositions["Purple Elixir"] = self.get_purple_elixir_positions()
            desiredPositions["Rare Watch"] = self.get_rare_watch_positions()

        # Display the end of trading day
        print("Ending Algorithm for Day:", self.day, "\n")
        

        #######################################################################
        # Return the desired positions
        return desiredPositions
