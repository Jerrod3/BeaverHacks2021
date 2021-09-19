from functions import *
import matplotlib.pyplot as plt
from labellines import labelLine, labelLines

# NOTES / THINGS TO IMPLEMENT
"""
I lost the try/except stuff along the way, so input validation isn't present here :(
If you look at the good default user material, it will hopefully be pretty straightforward how to implement
a bad default user.  It should only require creating one new function for each default user, and formatting it like
the default good user.
We need to figure out how to label the lines on the graph. I'm sure Plotly has a tool for this.
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

    def get_residence_size(self):
        """Getter function fo residence size"""
        return self._residence_size

    def calculate_footprint(self):
        """calculates the user's carbon footprint"""
        footprint = self._residence_size * 692 - sum(self._recycling_choices)
        print(footprint)
        for car in self._cars_list:
            if car["maintenance"]:
                footprint += car.get("lbs_CO2") * 0.96
            else:
                footprint += car.get("lbs_CO2") * 1.04
        footprint += self._utilities_dict["natural gas"] / 10.68 * (119.58 * 12)
        footprint += self._utilities_dict["electricity"] / .1188 * (.92 * 12)
        footprint += self._utilities_dict["oil"] / 4.02 * (22.61 * 12)
        footprint += self._utilities_dict["propane"] / 2.47 * (12.43 * 12)

        return int(footprint)


def main():
    """the main function for the program"""
    player = create_user()
    player_list = get_player_list(player.footprint)

    goody_two_shoes = good_user()
    nuke_the_planet = bad_user()
    green_fam = green_two_extra_kids(player.get_residence_size())
    waste_fam = wasteful_two_extra_kids(player.get_residence_size())
    good_list = get_modified_list(player.footprint, goody_two_shoes.footprint, player.age)
    bad_list = get_modified_list(player.footprint, nuke_the_planet.footprint, player.age)
    green_fam_list = get_modified_list(player.footprint, green_fam.footprint, player.age)
    waste_fam_list = get_modified_list(player.footprint, waste_fam.footprint, player.age)
    graph(player_list, good_list, bad_list,green_fam_list,waste_fam_list)


def get_player_list(yearly_footprint):
    """creates a list of the players cumulative footprint"""
    cumulative_list = [yearly_footprint]
    for i in range(1, 73):
        cumulative_list.append(int(cumulative_list[i-1] + yearly_footprint))
    return cumulative_list


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
    recycling_choices = [89, 36, 25, 113, 27]

    goody_two_shoes = User(age, residence_size, num_vehicles, car_list, utilities_dict, recycling_choices)

    return goody_two_shoes


def bad_user():
    """
    a default user object who makes non-green choices
    This user does not recycle, drives two average cars an average of 12,000 miles
    """
    age = 18  # this is arbitrary and won't come into play
    residence_size = 1
    num_vehicles = 3
    car_list = two_bad_cars()
    utilities_dict = {
            "natural gas": 100,
            "electricity": 200,
            "oil": 100,
            "propane": 100,
        }
    recycling_choices = [0, 0, 0, 0, 0, 0]  # does not recycle

    nuke_the_planet = User(age, residence_size, num_vehicles, car_list, utilities_dict, recycling_choices)

    return nuke_the_planet


def green_two_extra_kids(player_res_size):
    """
    Having two additional children (residents of your home) and being very green
    """

    age = 18  # this is arbitrary and won't come into play
    residence_size = player_res_size + 2
    num_vehicles = 1
    car_list = [{
        "mpg": maintenance_factor(36, True),
        "annual_miles": 8000,
        "maintenance": True,  # this entry in the dictionary can probably be deleted
        "lbs_CO2": (8000 / 36) * 19.6,
    }]
    utilities_dict = {
        "natural gas": 40,
        "electricity": 60,
        "oil": 0,
        "propane": 0,
    }
    recycling_choices = [89 * residence_size, 36, 25, 113, 27]

    green_fam = User(age, residence_size, num_vehicles, car_list, utilities_dict, recycling_choices)

    return green_fam


def wasteful_two_extra_kids(player_res_size):
    """
    Having two additional children (residents of your home) and being very wasteful
    """

    age = 18  # this is arbitrary and won't come into play
    residence_size = player_res_size + 2
    print(residence_size)
    num_vehicles = 3
    car_list = two_bad_cars()
    utilities_dict = {
        "natural gas": 200,
        "electricity": 200,
        "oil": 200,
        "propane": 200,
    }
    recycling_choices = [0, 0, 0, 0, 0]

    waste_fam = User(age, residence_size, num_vehicles, car_list, utilities_dict, recycling_choices)

    return waste_fam


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


def graph(player_list, good_list, bad_list,green_fam_list,waste_fam_list):
    """graphs all objects using Plotly"""
    input_values = list(range(18, 91))
    average_american_list = average_american()

    fig, ax = plt.subplots()
    # Create a line on the graph for each plot
    ax.plot(input_values, player_list, linewidth=1, label="You")
    ax.plot(input_values, average_american_list, linewidth=1, label="Avg American")
    ax.plot(input_values, good_list, linewidth=1, label="100% green")
    ax.plot(input_values, bad_list, linewidth=1, label="Bad Actor")
    ax.plot(input_values, green_fam_list, linewidth=1, label= "Green, two more kids")
    ax.plot(input_values, waste_fam_list, linewidth=1, label="Wasteful, two more kids")
    # Use the label lines package to put labels on the lines
    labelLines(plt.gca().get_lines(), fontsize=7)

    # Set chart title and label axes.
    ax.set_title("Lifetime CO2 Emissions", fontsize=24)
    ax.set_xlabel("Age", fontsize=14)
    ax.set_ylabel("CO2 Emissions in lbs", fontsize=14)

    # Set size of tick labels
    ax.tick_params(axis='both', labelsize=14)

    plt.show()


main()
