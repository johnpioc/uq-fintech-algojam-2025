import numpy as np

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

    def get_rare_watch_positions(self) -> int:
        instrument_name: str = "Rare Watch"

        if self.data[instrument_name][-2] > self.data[instrument_name][-1]:
            return self.positionLimits[instrument_name]
        else:
            return -self.positionLimits[instrument_name]

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

            for ins in trade_instruments:
                # if price has gone down buy
                if self.data[ins][-2] > self.data[ins][-1]:
                    desiredPositions[ins] = positionLimits[ins]
                else:
                    desiredPositions[ins] = -positionLimits[ins]
        # Display the end of trading day
        print("Ending Algorithm for Day:", self.day, "\n")
        

        #######################################################################
        # Return the desired positions
        return desiredPositions
