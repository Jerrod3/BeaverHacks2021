from functions import *
import matplotlib.pyplot as plt


class User:
    """A class that initializes a user for the game"""

    def __init__(self):
        self.age = int(input("How old are you? "))
        self._residence_size = int(input("How many people live in your home? "))
        self._num_vehicles = int(input("How many vehicles in your houehold? "))
        self._cars_list = []
        self._utilities_dict = {}
        self._recycling_choices = []
        self.footprint = 0

    def get_car_info(self):
        """
        Creates a list of cars in the household where each car is a dictionary
        :return: nothing
        """
        for i in range(self._num_vehicles):
            # gather car info to be appended later
            mpg = int(input(f"What is the mpg of car {i + 1}? "))
            annual_miles = int(input(f"How many miles do you drive car {i + 1} each year? (Avg is 11,000) "))
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

        self.footprint = cumulative_footprint
        return int(cumulative_footprint)

    def proactive_choices(self):

        """Actions the user can take to reduce their footprint after being shown
        what the footprints total amount is. Each input reduces the original footprint"""

        # if we go with the graph idea, this method won't be needed


def average_american():
    """
    :return: a list of the cumulative carbon footprint of the average american, in tons
    """
    average_list = [16*2000]
    for i in range(72):
        average_list.append(average_list[i] + 16*2000)

    return average_list


def nuke_planet(user, footprint_values):
    """
    creates a list of yearly cumulative co2 footprint where pre-current_age values = the user, and post current
    age = terrible choices
    :param user: the user object previously used
    :return: yearly footprint list
    """

    # average yearly additional emissions for ten more cars
    ten_cars = ((11398 / 21.6) * 19.6) * 10

    nuke_list = []

    for i in range(len(footprint_values)):
        if i < user.age - 18:
            nuke_list.append(footprint_values[i])
        else:
            nuke_list.append(int(nuke_list[i-1]) + user.footprint + ten_cars)

    return nuke_list


# def goody_two_shoes(user, footprint_values):
#     """Trendline where the user does literally everything they can to CO2 emissions(Recycles everything,
#     No vehicle, reduces utilities by half, uses all energy efficient technologies*"""

    # This function doesn't work because I moved it to be outside the class. Feel free to move it back.  I am thinking
    # we can model it after the nuke_planet function though, where it simply modifies a list of values rather than
    # creating a new instance.

    # I am becoming overwhelmed with this.

    # Need to add in electrical mitigations found in the excel sheet
    # cumulative_footprint = self._residence_size * 692 - self._residence_size * 290
    # cumulative_footprint += (self._utilities_dict["natural gas"] / 2) / 10.68 * (119.58 * 12)
    # cumulative_footprint += (self._utilities_dict["electricity"] / 2) / .1188 * (.92 * 12)
    # cumulative_footprint += (self._utilities_dict["oil"] / 2) / 4.02 * (22.61 * 12)
    # cumulative_footprint += (self._utilities_dict["propane"] / 2) / 2.47 * (12.43 * 12)
    #
    # self._footprint = cumulative_footprint
    #
    # return int(cumulative_footprint)



def graph(footprint_values, nuke_list):
    """use plotly to graph the user"""
    input_values = list(range(18, 91))

    average_american_list = average_american()

    fig, ax = plt.subplots()
    ax.plot(input_values, footprint_values, input_values, average_american_list, input_values, nuke_list, linewidth=3)

    # Set chart title and label axes.
    ax.set_title("Lifetime CO2 Emissions", fontsize=24)
    ax.set_xlabel("Age", fontsize=14)
    ax.set_ylabel("CO2 Emissions in tons", fontsize=14)

    # Set size of tick labels
    ax.tick_params(axis='both', labelsize=14)

    plt.show()


def create_user():
    """
    creates a user with the User class
    :returns: the user
    """
    # create the user object
    user = User()
    user.get_car_info()
    user.get_utility_info()
    user.get_recycling_info()
    total_yearly_footprint = user.calculate_footprint()
    print(f"Your current carbon footprint per year is {total_yearly_footprint} lbs.")
    return user


def calculate_lifetime_footprint(user):
    """
    this function calculates a lifetime carbon footprint and stores it as a list with each successive value being the
    running total. Ex. [10,20,30,40,50...]
    :return: the list of totals
    """
    # convert lbs to tons
    footprint_values = [int(user.footprint/2000)]
    for i in range(1, 73):
        footprint_values.append(int(footprint_values[i -1] + user.footprint))
    return footprint_values


def main():
    """the main function for running the program"""
    user = create_user()

    footprint_values = calculate_lifetime_footprint(user)
    nuke_list = nuke_planet(user, footprint_values)

    graph(footprint_values, nuke_list)


main()
