import numpy as np
from shapely.geometry import Point, Polygon, LineString


def area_of_slice(slice_data):
    return np.sum(np.array(slice_data, dtype=np.int8))


def area_of_contours(contours):
    total_area = 0

    for contour in contours:
        contour_polygon = Polygon(contour)

        # add points within the contour
        surrounding_points = get_surrounding_points(contour_polygon)
        for point in surrounding_points:
            if contour_polygon.contains(point):
                total_area += 1

        # add points on the perimeter of the contour
        total_area += len(contour)

    return total_area


def get_surrounding_points(polygon):
    minx, miny, maxx, maxy = polygon.bounds
    minx, miny, maxx, maxy = int(minx), int(miny), int(maxx), int(maxy)
    return [Point([x, y]) for x in range(minx, maxx + 1) for y in range(miny, maxy + 1)]
