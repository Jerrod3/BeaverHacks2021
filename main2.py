from functions import positive_responses

class User:
    """A class that initializes a user for the game"""

    def __init__(self):
        self._residence_size = int(input("How many people live in your home? "))
        self._num_vehicles = int(input("How many vehicles in your houehold? "))
        self._cars_list = []
        self._utilities_dict = {}

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
                "mpg": mpg,
                "annual_miles": annual_miles,
                "maintenance": maintenance,
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

    def calculate_footprint(self):
        """
        calculates the user's carbon footprint
        return: total footprint an integer
        """
        cumulative_footprint = self._residence_size * 692
        for car in self._cars_list:
            # Add some logic to handle maintenance. Currently maintenance doesn't come into play at all
            cumulative_footprint += car.get("lbs_CO2")
        cumulative_footprint += self._utilities_dict["natural gas"] / 10.68 * (119.58 * 12)
        cumulative_footprint += self._utilities_dict["electricity"] / .1188 * (.92 * 12)
        cumulative_footprint += self._utilities_dict["oil"] / 4.02 * (22.61 * 12)
        cumulative_footprint += self._utilities_dict["propane"] / 2.47 * (12.43 * 12)

        return int(cumulative_footprint)


def main():
    """the main function for creating the user"""
    # create the user object
    user = User()
    user.get_car_info()
    user.get_utility_info()
    total_footprint = user.calculate_footprint()
    print(f"Your current carbon footprint per year is {total_footprint} lbs.")


main()


