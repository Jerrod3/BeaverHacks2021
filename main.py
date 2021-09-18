from functions import *
import copy


class User:
    """A class that initializes a user for the game"""

    def __init__(self):
        while True:
            try:
                self._residence_size = int(input("How many people live in your home? "))
            except:
                print("Please enter a valid amount of residents")
                continue
            try:
                self._num_vehicles = int(input("How many vehicles in your household? "))
            except:
                print("Please enter a valid quantity of vehicles")
                continue
            try:
                self._current_age = int(input("How old are you currently? Minimum age is 18"))
                if self._current_age < 18:
                    print("Please enter a viable age")
                    continue
            except:
                print("Please enter a viable age")
                continue
            break
        self._cars_list = []
        self._utilities_dict = {}
        self._recycling_choices = []
        self._lifetime_CO2 = None
        self._footprint = 0

    def get_car_info(self):
        """
        Creates a list of cars in the household where each car is a dictionary
        :return: nothing
        """
        for i in range(self._num_vehicles):
            # gather car info to be appended later
            while True:
                try:
                    mpg = float(input(f"What is the mpg of car {i + 1}? "))
                    annual_miles = float(input(f"How many miles do you drive car {i + 1} each year? (Avg is 11,000) "))
                    maintenance_answer = input("Do you perform regular maintenance on this vehicle? ")
                    if maintenance_answer in positive_responses():
                        maintenance = True
                    else:
                        maintenance = False

                    # create a dictionary for each car
                    car_dict = {
                        "mpg": maintenance_factor(mpg, maintenance),
                        "annual_miles": annual_miles,
                        "maintenance": maintenance,  # this entry in the dictionary can probably be deleted
                        "lbs_CO2": (annual_miles / mpg) * 19.6,
                    }

                    # append each car to the car list
                    self._cars_list.append(car_dict)

                    break
                except:
                    print("Please enter both a correct amount of miles and mpg")
                    continue
    def get_utility_info(self):
        """
        Creates a single dictionary storing the user's utility usage
        :return: nothing
        """
        # gather utility info to store in dictionary
        while True:
            try:
                natural_gas = int(input("How much do you spend on natural gas each month? $"))
                electricity = int(input("How much do you spend on electricity each month? $"))
                oil = int(input("How much do you spend on oil fuel each month? $"))
                propane = int(input("How much do you spend on propane each month? $"))

                self._utilities_dict = {
                    "natural gas": natural_gas,
                    "electricity": electricity,
                    "oil": oil,
                    "propane": propane,
                }
            except:
                print("Please enter a valid $ amount")
                continue
            break

    def get_recycling_info(self):
        """Calculates recycling reductions"""
        # the list of potentially recycled items
        recyclable_items = ['metal cans', 'plastic', 'glass', 'paper', 'magazines']
        # go through list and ask if the user recycles said item, and append to value list accordingly
        for item in recyclable_items:
            response = input(f"Do you recycle {item}? ")
            if item == 'metal cans' and response in positive_responses():
                self._recycling_choices.append(89 * self._residence_size)
            elif item == 'plastic' and response in positive_responses():
                self._recycling_choices.append(36 * self._residence_size)
            elif item == 'glass' and response in positive_responses():
                self._recycling_choices.append(25 * self._residence_size)
            elif item == 'paper' and response in positive_responses():
                self._recycling_choices.append(113 * self._residence_size)
            elif item == 'magazines' and response in positive_responses():
                self._recycling_choices.append(27 * self._residence_size)

    def calculate_footprint(self):
        """
        calculates the user's carbon footprint
        return: total footprint an integer
        """
        # base value from residence size, subtract recycling values
        cumulative_footprint = self._residence_size * 692 - (sum(self._recycling_choices))
        for car in self._cars_list:
            if car["maintenance"]:
                cumulative_footprint += car.get("lbs_CO2") * .96
            else:
                cumulative_footprint += car.get("lbs_CO2") * 1.04
        cumulative_footprint += self._utilities_dict["natural gas"] / 10.68 * (119.58 * 12)
        cumulative_footprint += self._utilities_dict["electricity"] / .1188 * (.92 * 12)
        cumulative_footprint += self._utilities_dict["oil"] / 4.02 * (22.61 * 12)
        cumulative_footprint += self._utilities_dict["propane"] / 2.47 * (12.43 * 12)

        self._footprint = cumulative_footprint

        return int(cumulative_footprint)

    def current_lifetime_footprint(self):

        """Creates a simple list of accumulated C02 use over the current lifespan of the user. The base for the
        rest of the lines in the graph up to a given point, the users age"""

        # Adding in the basic list for the 45 degree "life so far" line
        life_lst = []
        cumulative_CO2 = 0
        #Used with a minimum age of 18, since metrics go off of household emissions
        for year in range(18, self._current_age):
            cumulative_CO2 += self._footprint
            life_lst.append(cumulative_CO2)

        self._lifetime_CO2 = life_lst

        return sum(life_lst)

    def extrapolate_trend(self):

        """Extrapolating the accumulated C02 over a given set of years, to age 90"""

        life_lst = []
        #Start with the highest accumulated amount from the user input list
        cumulative_CO2 = self._lifetime_CO2[-1]
        for year in range(self._current_age, 90):
            cumulative_CO2 += self._footprint
            life_lst.append(cumulative_CO2)

        self._lifetime_CO2 += life_lst
        return self._lifetime_CO2

    def nuke_the_earth(self):

        """Trendline where the user fails to do anything at all, has 3 extra kids,
         utility bills are double the amount, and mpg's are half of the users amount, and they
         drive twice the distance annually"""

        cumulative_footprint = (self._residence_size + 3) * 692
        for car in self._cars_list:
            # There is an error here, car.get should be retrieving the key value, but it returns none.
            print(car.get("annual miles"))
            cumulative_footprint += (car.get("annual miles") * 2) / (car.get("mpg")/2) * 19.6 * 1.04
        cumulative_footprint += (self._utilities_dict["natural gas"]*2) / 10.68 * (119.58 * 12)
        cumulative_footprint += (self._utilities_dict["electricity"]*2) / .1188 * (.92 * 12)
        cumulative_footprint += (self._utilities_dict["oil"]*2) / 4.02 * (22.61 * 12)
        cumulative_footprint += (self._utilities_dict["propane"]*2) / 2.47 * (12.43 * 12)

        self._footprint = cumulative_footprint

        return int(cumulative_footprint)

    def goody_two_shoes(self):

        """Trendline where the user does literally everything they can to CO2 emissions(Recycles everything,
        No vehicle, reduces utilities by half, uses all energy efficient technologies*"""

        # Need to add in electrical mitigations found in the excel sheet
        cumulative_footprint = self._residence_size * 692 - self._residence_size * 290
        cumulative_footprint += (self._utilities_dict["natural gas"]/2) / 10.68 * (119.58 * 12)
        cumulative_footprint += (self._utilities_dict["electricity"]/2) / .1188 * (.92 * 12)
        cumulative_footprint += (self._utilities_dict["oil"]/2) / 4.02 * (22.61 * 12)
        cumulative_footprint += (self._utilities_dict["propane"]/2) / 2.47 * (12.43 * 12)

        self._footprint = cumulative_footprint

        return int(cumulative_footprint)



def main():
    """the main function for creating the user"""
    # create the user object
    user = User()
    user.get_car_info()
    user.get_utility_info()
    user.get_recycling_info()
    print(f"Your households current carbon footprint per year is {user.calculate_footprint()} lbs.")
    print(f"Your overall lifetime household carbon footprint is {user.current_lifetime_footprint()} lbs.")
    # The deep copy function creates an instance of a class object that is identical to the object that is in the
    # parameter field. I figure we can use this to get copies of the user object's inputs, then modify them through
    # the functions afterwards. For example, for each line on the graph,
    # we can modify the "calculate footprint" function to alter the users carbon footprint/year (ie the nuke func)
    # Then, for every instance, we pass it through the extrapolate trend function afterwards
    # to project CO2 emissions up to age 90. Test it out below to see what I mean!
    nuke_user = copy.deepcopy(user)
    goody = copy.deepcopy(user)
    nuke_user.nuke_the_earth()
    goody.goody_two_shoes()
    print(user.current_lifetime_footprint())
    print(goody.extrapolate_trend())
    print(user.extrapolate_trend())
    print(nuke_user.extrapolate_trend())
main()
