import utilities


def get_feb():
    dist = utilities.get_points_distance(1, 2)
    print('feb dist is {0}'.format(dist))


def get_fhd():
    dist = utilities.get_points_distance(1, 3)
    print('fhd dist is {0}'.format(dist))


def get_fmld():
    dist = utilities.get_points_distance(1, 4)
    print('fmld dist is {0}'.format(dist))


def get_measurement():
    print('Start measuring femur...')
    get_feb()
    get_fhd()
    get_fmld()
