import matplotlib.pyplot as plt

# NOTES / THINGS TO IMPLEMENT
"""
I lost the try/except stuff along the way, so input validation isn't present here :(
If you look at the good default user material, it will hopefully be pretty straightforward how to implement
a bad default user.  It should only require creating one new function for each default user, and formatting it like
the default good user.
We need to figure out how to label the lines on the grpah. I'm sure Plotly has a tool for this.
Move some functions to function.py, though this is just for readability and aesthetics.
Update README
Update this docstring to show a description, date, and us at the authors.
"""

class User:
    """A class that represents a user for the game"""
    def __init__(self, age, residence_size, num_vehicles, cars_list, utilities_dict, recycling_choices):
        self.age = age
        self._residence_size = residence_size
        self._num_vehicles = num_vehicles
        self._cars_list = cars_list
        self._utilities_dict = utilities_dict
        self._recycling_choices = recycling_choices
        self.footprint = self.calculate_footprint()

    def calculate_footprint(self):
        """calculates the user's carbon footprint"""
        footprint = self._residence_size * 692 - sum(self._recycling_choices)
        for car in self._cars_list:
            if car["maintenance"]:
                footprint += car.get("lbs_CO2") * 0.96
            else:
                footprint -= car.get("lbs_CO2") * 0.96
        footprint += self._utilities_dict["natural gas"] / 10.68 * (119.58 * 12)
        footprint += self._utilities_dict["electricity"] / .1188 * (.92 * 12)
        footprint += self._utilities_dict["oil"] / 4.02 * (22.61 * 12)
        footprint += self._utilities_dict["propane"] / 2.47 * (12.43 * 12)

        return int(footprint)


def get_car_info(num_vehicles):
    """
    Creates a list of cars in the household where each car is a dictionary
    :return: nothing
    """
    car_list = []
    for i in range(num_vehicles):
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

        # append each car_dict to the car list
        car_list.append(car_dict)

    return car_list


def get_utility_info():
    """
    Creates a single dictionary storing the user's utility usage
    :return: nothing
    """
    # gather utility info to store in dictionary
    natural_gas = int(input("How much do you spend on natural gas each month? $"))
    electricity = int(input("How much do you spend on electricity each month? $"))
    oil = int(input("How much do you spend on oil fuel each month? $"))
    propane = int(input("How much do you spend on propane each month? $"))

    utilities_dict = {
        "natural gas": natural_gas,
        "electricity": electricity,
        "oil": oil,
        "propane": propane,
    }

    return utilities_dict


def get_recycling_info(residence_size):
    """Calculates recycling reductions"""
    # the list of potentially recycled items
    recyclable_items = ['metal cans', 'plastic', 'glass', 'paper', 'magazines']
    # go through list and ask if the user recycles said item, and append to value list accordingly
    recycling_choices = []
    for item in recyclable_items:
        response = input(f"Do you recycle {item}? ")
        if response not in positive_responses():
            recycling_choices.append(89 * residence_size)
        else:
            if item == 'metal cans':
                recycling_choices.append(89 * residence_size)
            elif item == 'plastic':
                recycling_choices.append(36 * residence_size)
            elif item == 'glass':
                recycling_choices.append(25 * residence_size)
            elif item == 'paper':
                recycling_choices.append(113 * residence_size)
            elif item == 'magazines':
                recycling_choices.append(27 * residence_size)

    return recycling_choices


def get_player_list(yearly_footprint):
    """creates a list of the players cumulative footprint"""
    cumulative_list = [yearly_footprint]
    for i in range(1, 73):
        cumulative_list.append(int(cumulative_list[i-1] + yearly_footprint))
    return cumulative_list


def get_modified_list(yearly_footprint, modified_footprint, age):
    """creates a list of the modified cumulative footprint"""
    # modification_factor = yearly_footprint = modified_footprint
    modified_list = [yearly_footprint]

    for i in range(1, 73):
        if i <= age:
            modified_list.append(modified_list[i-1] + yearly_footprint)
        else:
            modified_list.append(modified_list[i-1] + modified_footprint)

    return modified_list


def average_american():
    """
    :return: a list of the cumulative carbon footprint of the average american, in lbs
    """
    average_list = [16*2000]
    for i in range(72):
        average_list.append(average_list[i] + 16*2000)

    return average_list


def good_user():
    """a default user object who makes green choices"""
    age = 18  # this is arbitrary and won't come into play
    residence_size = 1
    num_vehicles = 0
    car_list = []
    utilities_dict = {
            "natural gas": 0,
            "electricity": 25,
            "oil": 0,
            "propane": 0,
        }
    recycling_choices = [89, 89, 36, 25, 113, 27]

    goody_two_shoes = User(age, residence_size, num_vehicles, car_list, utilities_dict, recycling_choices)

    return goody_two_shoes


def create_user():
    """
    creates a user with the User class
    :return:
    """
    age = int(input("How old are you? "))
    residence_size = int(input("How many people live in your home? "))
    num_vehicles = int(input("How many vehicles in your household? "))
    car_list = get_car_info(num_vehicles)
    utilities_dict = get_utility_info()
    recycling_choices = get_recycling_info(residence_size)

    player = User(age, residence_size, num_vehicles, car_list, utilities_dict, recycling_choices)

    return player


def graph(player_list, good_list):
    """graphs all objects using Plotly"""
    input_values = list(range(18, 91))
    average_american_list = average_american()

    fig, ax = plt.subplots()
    ax.plot(input_values, player_list, input_values, average_american_list, input_values, good_list, linewidth=3)

    # Set chart title and label axes.
    ax.set_title("Lifetime CO2 Emissions", fontsize=24)
    ax.set_xlabel("Age", fontsize=14)
    ax.set_ylabel("CO2 Emissions in lbs", fontsize=14)

    # Set size of tick labels
    ax.tick_params(axis='both', labelsize=14)

    plt.show()


def main():
    """the main function for the program"""
    player = create_user()
    player_list = get_player_list(player.footprint)

    goody_two_shoes = good_user()
    good_list = get_modified_list(player.footprint, goody_two_shoes.footprint, player.age)

    # print(player_list)
    # print(good_list)

    graph(player_list, good_list)


def positive_responses():
    """a list of positive response"""
    return ['yes', 'y', 'Yes', 'Y']


def maintenance_factor(mpg, maintenance_bool):
    """
    :param mpg: fuel efficiency as an int
    :param maintenance_bool: whether regular maintenance is performed
    :return: modified mpg as float
    """
    if maintenance_bool:
        return mpg * 1.04
    else:
        return mpg * 0.96

main()