# Import necessary modules
import simulation
import pickle

# This is commented out because we will be using pickle to update Derek's profile object, hence run once
# Initialize Derek's profile
# derek = simulation.Profile()
# derek.set_cash(20)  # Load $20 to Derek's profile

# This was a test, this will submit the order for Apple stock worth $20, run once, else continue to submit order
# derek.submit_order('AAPL', 20)
# with open('derek.pkl', 'wb') as file:  # Open the pickle file to dump Derek's profile
#     pickle.dump(derek, file)  # Dump Derek's profile


# Read Derek's profile
with open('derek.pkl', 'rb') as file:  # Load Derek's profile object
    derek = pickle.load(file)  # Define Derek object as derek

derek.complete_trade()  # Example of complete trade
