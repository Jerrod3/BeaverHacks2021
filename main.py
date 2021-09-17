
class User:

    """A class that initializes the game"""

    def __init__(self, cumulative_footprint):

        self._cumulative_footprint = cumulative_footprint

    def get_current_footprint(self):

        """method to show current carbon footprint"""

        return "Your current carbon footprint in lbs per year is:",   self._cumulative_footprint


def main():

    """The main function"""
    player = User(0)

    print("Welcome to footprint calculator!")

    residence_size = int(input("How many people live in your home?"))
    base_waste = residence_size * 692
    player._cumulative_footprint = player._cumulative_footprint + base_waste

    # Calculate pounds per year of C02 via car exhaust:

    car_quant = int(input("How many vehicles in your household?"))
    if car_quant >= 1:
        car_lst = []
        for cars in range(1 ,car_quant + 1):
            mpg = float(input("What is the mpg of car " + str(cars) + "?"))
            miles_per_year = float(input("How many miles do you drive car " + str(cars) + " per week?"))
            regular_maintenance = input("Do you perform regular maintenance on this vehicle?")
            if regular_maintenance == "yes" or "Yes":
                regular_maintenance == True
            else:
                regular_maintenance == False
            # Could throw try and excepts in here for invalid inputs (or all of the inputs, really)
            car_i = [mpg ,miles_per_year ,regular_maintenance]
            car_lst.append(car_i)
        for cars in car_lst:
            lbs_carbon = (cars[1] * 52) / cars[0] * 19.64 * 1.01
            if cars[2] == False:
                lbs_carbon = lbs_carbon * 1.04
            player._cumulative_footprint = player._cumulative_footprint + lbs_carbon

    # Calculate CO2 cost per lb of household C02 usage

    natural_gas = (int(input("How much natural gas, in $, does your house use per month?")))/10.68 * (119.58 * 12)
    player._cumulative_footprint = player._cumulative_footprint + natural_gas


    electric = (int(input("How much, in $ per month, is your electrical bill?")))/.1188 * (.92 * 12)
    player._cumulative_footprint = player._cumulative_footprint + electric
    #Need to incorporate green power usage here - formula is not specific on how that apllies,
    #Unless it is applied in the reduction section further on down

    fuel_oil = (int(input("How much, in $ per month, is your fuel oil bill?")))/4.02 * (22.61*12)
    player._cumulative_footprint = player._cumulative_footprint + fuel_oil

    propane = (int(input("How much, in $ per month, is your propane?"))) / 2.47 * (12.43 * 12)
    player._cumulative_footprint = player._cumulative_footprint + propane

    print("The base amount of your carbon waste is", player.get_current_footprint())
main()
