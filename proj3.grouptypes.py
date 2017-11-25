from math import hypot
# Initialising the city of GRIDBOURNE
GRIDBOURNE = []
letter = list(map(chr, range(65, 75)))
number = list(num for num in range(1, 11))
for i in letter:
    row = []
    for j in number:
        row.append('{}{}'.format(i, j))
    GRIDBOURNE.append(row)

def cord_of_restraunts(x, y):
    ''' Takes input x,y coordintaes of users location, finds the coordinates of
   restraunts in neighbourhood returning list float coordinates(HELPER FUNC)'''

    cr_rest_cord = [float((str(abs(x)))[0]), float((str(abs(y)))[0])]
    mr_rest_cord = [float((str(abs(x)))[0] + '.5'),
                    float((str(abs(y)))[0] + '.5')]

    return [cr_rest_cord, mr_rest_cord]

def dist_rest(x, y, a, b):
    ''' Takes user location (a, b) and neighbourhood to be tested:(x, y) and
    finds user distance restraunts returning a list (HELPER FUNC)'''

    # Finding coordinates of the middle and corner restraunts in neighbourhood
    rest_cord = cord_of_restraunts(x, y)

    # Finding user location with origin as CR followed by origin as MR
    relative_xcr = a - rest_cord[0][0]
    relative_ycr = b - rest_cord[0][1]
    relative_xmr = a - rest_cord[1][0]
    relative_ymr = b - rest_cord[1][1]

    # Assuming CR,MR cords as origin to calculate eucl distance using hypot
    dist_cr = hypot(relative_xcr, relative_ycr)
    dist_mr = hypot(relative_xmr, relative_ymr)

    return [dist_cr, dist_mr]

def find_my_neighbourhood(x, y):
    ''' Takes an x and y coordinate as input to find the location of user in
    terms of neighbourhood returning a list'''

    #  Checking row and column user is located in and assigning respectively
    y = str(abs(y))
    x = str(abs(x))
    col = (int(x[0]))
    row = (int(y[0]))

    return GRIDBOURNE[row][col]

def find_all_restaurants_in_neighbourhood(x, y):
    ''' Calls find_my_neighbourhood to check location of user and returns the 2
    restraunts in acsending alphabetical order as a list'''

    nhood = find_my_neighbourhood(x, y)
    nhood_rest = [nhood + 'CR', nhood + 'MR']

    return nhood_rest

def find_closest_restaurant_in_neighbourhood(x, y):
    ''' Takes user location (x, y) as inputs and finds the nearest
    restraunts to the user in their neighbourhood returning a list'''

    # Calling on dist_rest to calculate restraunt distances
    dist_cr = dist_rest(x, y, x, y)[0]
    dist_mr = dist_rest(x, y, x, y)[1]

    # Checking for closest restraunt
    if dist_cr == dist_mr:
        return find_all_restaurants_in_neighbourhood(x, y)
    elif dist_cr < dist_mr:
        return [(find_all_restaurants_in_neighbourhood(x, y))[0]]
    else:
        return [(find_all_restaurants_in_neighbourhood(x, y))[1]]

def find_farthest_restaurant_in_neighbourhood(x, y):
    ''' Takes user location (x, y) as inputs and finds the farthest
    restraunts to the user in their neighbourhood returning a list'''

    # Calling on dist_rest to calculate restraunt distances
    dist_cr = dist_rest(x, y, x, y)[0]
    dist_mr = dist_rest(x, y, x, y)[1]

    # Checking for closest restraunt
    if dist_cr == dist_mr:
        return find_all_restaurants_in_neighbourhood(x, y)
    elif dist_cr > dist_mr:
        return [(find_all_restaurants_in_neighbourhood(x, y))[0]]
    else:
        return [(find_all_restaurants_in_neighbourhood(x, y))[1]]

def find_closest_restaurant(x, y):
    ''' Takes user location (x, y) as inputs and finds the closest restruants
    regardless of neighbourhood returning a list'''

    # List of curr, right, left, up, down and diag_topright neighbourhoods
    near_hoods = [(x, y), (x+1, y), (x-1, y), (x, y+1), (x, y-1), (x+1, y+1)]

    # Scenario 2: location in left most column of GRIDBOURNE
    if x < 1:
        del near_hoods[2]

    # Scenario 2: location in right most column of GRIDBOURNE
    if x >= 9:
        del near_hoods[1]

    # Scenario 3: location in top column of GRIDBOURNE
    if y >= 9:
        del near_hoods[3]

    # Scenario 4: location in bottom column of GRIDBOURNE
    if y < 1:
        del near_hoods[4]

    # Running through list of nearby restraunts to compile list of closest
    nearest_rest = [[(0, 0), 40000, '']]
    for hood in near_hoods:
        dist_to_rest = dist_rest(hood[0], hood[1], x, y)
        if dist_to_rest[0] < nearest_rest[0][1]:
            nearest_rest = [[hood, dist_to_rest[0], 'CR']]
        elif dist_to_rest[0] == nearest_rest[0][1]:
            nearest_rest.append([hood, dist_to_rest[0], 'CR'])
        if dist_to_rest[1] < nearest_rest[0][1]:
            nearest_rest = [[hood, dist_to_rest[1], 'MR']]
        elif dist_to_rest[1] == nearest_rest[0][1]:
            nearest_rest.append([hood, dist_to_rest[1], 'MR'])

    # Formatting to return just neighbourhood and restraunt list
    final_list = []
    for mem in nearest_rest:
        final_list.append('{}{}'.format(find_my_neighbourhood(mem[0][0],
                          mem[0][1]), mem[2]))

    return sorted(list(set(final_list)))

def find_closest_restaurant_on_path(list_of_stops):
    ''' Takes a list of lists with x,y coordinates and returns nearest
    restaurant along that path'''

    final_list = []
    for stop in list_of_stops:
        final_list.append(find_closest_restaurant(stop[0], stop[1]))

    return final_list
