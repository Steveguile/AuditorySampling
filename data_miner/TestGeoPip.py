import geopip
import random

# UK borders exist somewhere between -8.2 (longitude) to 60 (latitude)
print(random.uniform(-8.2, 60))


test = geopip.search(lng=-5.172886, lat=58.2289307)


def method():
    # UK borders exist somewhere between -8.5 to 2.2 (latitude) and 49.5 to 60 (longitude)
    Lat = random.uniform(49.5, 60)
    Long = random.uniform(-8.5, 2.2)
    coord = geopip.search(lng=Long, lat=Lat)

    # Lovely bit of recursion
    if coord is None:
        method()
    elif coord["FIPS"] == 'UK':
        print(coord)
        # Return
        print(Lat)
        print(Long)
    else:
        method()


method()