# Script to visualize geojson data (a json based file format for representing geographical features)
import matplotlib.pyplot as plt
import json

DATA_PATH = '/Users/mitchrydzynski/Downloads/cb_2018_us_county_500k/cb_2018_us_county_500k.geojson'


def plt_multipolygon(coords):
    for polygon in coords:
        plt_polygon(polygon)


def plt_polygon(coords):
    for ring in coords:
        x_coords = []
        y_coords = []
        for point in ring:
            x_coords.append(point[0])
            y_coords.append(point[1])
        plt.plot(x_coords, y_coords)


if __name__ == '__main__':
    # extract the data from the county of interest
    county_data = []
    with open(DATA_PATH) as f:
        data = json.load(f)
        for county_points in data['features']:
            county_data.append(county_points['geometry'])

    # visualize the data
    plt.figure()
    for county in county_data:
        if county['type'] == 'Polygon':
            plt_polygon(county['coordinates'])
        elif county['type'] == 'MultiPolygon':
            plt_multipolygon(county['coordinates'])
        else:
            print(f'Saw unrecognized data format {county['type']}')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('USA Counties Map')
    plt.show()
