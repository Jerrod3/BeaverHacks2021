from functions import *


class User:
    """A class that initializes a user for the game"""

    def __init__(self):
        self._residence_size = int(input("How many people live in your home? "))
        self._num_vehicles = int(input("How many vehicles in your houehold? "))
        self._cars_list = []
        self._utilities_dict = {}
        self._recycling_choices = []
        self._footprint = 0

    def get_car_info(self):
        """
        Creates a list of cars in the household where each car is a dictionary
        :return: nothing
        """
        for i in range(self._num_vehicles):
            # gather car info to be appended later
            mpg = int(input(f"What is the mpg of car {i + 1}? "))
            annual_miles = int(input(f"How many miles do you drive car {i + 1} per year? (Avg is 11,000) "))
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

    def get_utility_info(self):
        """
        Creates a single dictionary storing the user's utility usage
        :return: nothing
        """
        # gather utility info to store in dictionary
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

    def get_recycling_info(self):
        """Calculates recycling reductions"""
        # the list of potentially recycled items
        recyclable_items = ['metal cans', 'plastic', 'glass', 'paper', 'magazines']
        # go through list and ask if the user recycles said item, and append to value list accordingly
        for item in recyclable_items:
            response = input(f"Do you recycle {item}? ")
            if item not in positive_responses():
                self._recycling_choices.append(89 * self._residence_size)
            else:
                if item == 'metal cans':
                    self._recycling_choices.append(89 * self._residence_size)
                elif item == 'plastic':
                    self._recycling_choices.append(36 * self._residence_size)
                elif item == 'glass':
                    self._recycling_choices.append(25 * self._residence_size)
                elif item == 'paper':
                    self._recycling_choices.append(113 * self._residence_size)
                elif item == 'magazines':
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

    def proactive_choices(self):

        """Actions the user can take to reduce their footprint after being shown
        what the footprints total amount is. Each input reduces the original footprint"""

        # if we go with the graph idea, this method won't be needed


def main():
    """the main function for creating the user"""
    # create the user object
    user = User()
    user.get_car_info()
    user.get_utility_info()
    user.get_recycling_info()
    total_footprint = user.calculate_footprint()
    print(f"Your current carbon footprint per year is {total_footprint} lbs.")
    #Possibly add in a statement that tells that the above print statement is the max footprint
    #without carbon abatement practices?
    print("Here are some actions you can take to reduce your footprint")



main()
