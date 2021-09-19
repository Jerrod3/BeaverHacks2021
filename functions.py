"""
All the functions needed for main.py
"""


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
            continue
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


def average_american():
    """
    :return: a list of the cumulative carbon footprint of the average american, in lbs
    """
    average_list = [16]
    for i in range(72):
        average_list.append(average_list[i] + 16)

    return average_list


def get_modified_list(yearly_footprint, modified_footprint, age):
    """creates a list of the modified cumulative footprint"""
    # modification_factor = yearly_footprint = modified_footprint
    modified_list = [yearly_footprint]

    for i in range(1, 73):
        if i <= age - 18:
            modified_list.append(modified_list[i-1] + yearly_footprint)
        else:
            modified_list.append(modified_list[i-1] + modified_footprint)

    return modified_list


def two_bad_cars():
    """returns a list of two bad car dicts"""
    return [
        {
            "mpg": maintenance_factor(21.6, False),
            "annual_miles": 4000,
            "maintenance": False,  # this entry in the dictionary can probably be deleted
            "lbs_CO2": (11000 / 21.6) * 19.6,
        },
        {
            "mpg": maintenance_factor(21.6, False),
            "annual_miles": 4000,
            "maintenance": False,  # this entry in the dictionary can probably be deleted
            "lbs_CO2": (11000 / 21.6) * 19.6,
        },
    ]


def one_good_car():
    """returns a list of a single good car dict"""
    return [
        {
            "mpg": maintenance_factor(50, False),
            "annual_miles": 5000,
            "maintenance": True,  # this entry in the dictionary can probably be deleted
            "lbs_CO2": (11000 / 50) * 19.6,
        }
    ]