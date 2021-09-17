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
