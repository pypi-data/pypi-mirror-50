#!/usr/bin/env python3

def rayArea(A:str, B:str):
    '''Creates the Ray area between two objects A and B. The objects have to be in WKT format.'''
    import shapely.wkt, shapely.geometry
    from shapely.ops import polygonize


    def getallpoints(O):
        '''Function for getting all the points of a geometry, regardless if it is multi or single geometry'''
        otype = O.type
        if otype == 'MultiPolygon':
            points = [x for p in O for x in list(shapely.geometry.MultiPoint(p.exterior.coords))]
        if otype == 'Polygon':
            points = list(shapley.geometry.MultiPoint(O.exterior.coords))
        if otype == 'MultiLineString':
            points = [x for p in O for x in list(shapely.geometry.MultiPoint(p.coords))]
        if otype == 'LineString':
            points = list(shapely.geometry.MultiPoint(O.coords))
        if otype == 'MultiPoint':
            points = list(O)
        if otype == 'Point':
            points = [O]
        points = set([(p.x,p.y) for p in points])
        points = [shapely.geometry.Point(p) for p in points]
        return points

    def extendLine(p1, p2, scale=10):
        'Creates a line extrapoled in p1->p2 direction'
        # add a check for line geometry here later on
        a = p1
        b = shapely.geometry.Point(p1.x+scale*(p2.x-p1.x), p1.y+scale*(p2.y-p1.y))
        extended_linestring = shapely.geometry.LineString([(a.x, a.y), (b.x, b.y)])
        return extended_linestring

    A = shapely.wkt.loads(A)
    B = shapely.wkt.loads(B)

    # 1. Make a convex hull of the two objects
    geomcol = shapely.geometry.GeometryCollection([A, B])
    chullAB = geomcol.convex_hull

    # 2. Difference of the chull and the original objects
    chull_diff = chullAB.difference(geomcol)

    # forcing chull_diff to multipolygon
    chull_diff = shapely.geometry.MultiPolygon(chull_diff)

    # 3. Keep only the parts that are touching both original objects. If the chull is a multipolygon, this will remove any polygons which are touching only one of the objects A and B
    new_chull_diff = []

    for geom in chull_diff:
        if geom.intersects(A) and geom.intersects(B):
            new_chull_diff.append(geom)
    
    chull_diff = shapely.geometry.MultiPolygon(new_chull_diff)

    rayArea_A = chull_diff.intersection(A)
    rayArea_B = chull_diff.intersection(B)

    points_A = getallpoints(rayArea_A)
    points_B = getallpoints(rayArea_B)

    mline = []
    for p1 in points_A:
        for p2 in points_B:
            line = shapely.geometry.LineString([p1, p2])
            if line.touches(A) and line.touches(B):
                mline.append(line)
    mline = shapely.geometry.MultiLineString(mline)

    unreached_points = []
    polygon1 = []
    for pol in chull_diff:
        polygon_points = []
        for point in shapely.geometry.MultiPoint(pol.boundary.coords):
            if mline.intersects(point):
                polygon_points.append(point)
            else:
                unreached_points.append(point)
        single_polygon = shapely.geometry.Polygon([(p.x, p.y) for p in polygon_points])
        polygon1.append(single_polygon)
    polygon1 = shapely.geometry.MultiPolygon(polygon1)
    unreached_points = shapely.geometry.MultiPoint(unreached_points)

    polygons_remaining = chull_diff.difference(polygon1)
    if polygons_remaining.type != 'MultiPolygon':
        polygons_remaining = shapely.geometry.MultiPolygon([polygons_remaining])

    areas_to_add = []
    for polygon_remaining in polygons_remaining:
        area_to_add = []
        for line in mline:
            if line.intersects(polygon_remaining):
                p1, p2 = shapely.geometry.MultiPoint(line.coords)
                if p1.intersects(polygon_remaining):
                    # if the first point of the line (which is always defined with 2 points) is touching the remaining area, extend the line in the direction p2->p1
                    extended_line = extendLine(p2, p1)
                else:
                    # otherwise, extend the line in the direction p1->p2
                    extended_line = extendLine(p1, p2)
                if extended_line.crosses(polygon_remaining):
                    # combine the boundary of the remaining polygon and the line splitting it in 2
                    combined_lines = extended_line.union(polygon_remaining.boundary)

                    # polygonize these combined lines in order to create the version of the remaining polygon that is split in 2 by the extended line
                    polygon_remaining_split = polygonize(combined_lines)

                    for pol in polygon_remaining_split:
                        if pol.disjoint(unreached_points):
                            area_to_add = area_to_add.append(pol)
        areas_to_add.append(shapely.geometry.MultiPolygon(area_to_add))
    areas_to_add = shapely.geometry.MultiPolygon(areas_to_add)

    final_ray_area = polygon1.union(areas_to_add)

    if final_ray_area.type != 'MultiPolygon':
        final_ray_area = shapely.geometry.MultiPolygon([final_ray_area])

    # Now I have to calculate the extreme rays
    # Finding the extreme rays between the final ray area and objects A and B
    # Each polygon in a multipolygon ray_area will be considered separately
    ray_area_with_extreme_rays = []
    for geom in final_ray_area:
        extreme_rays = []
        # Scenario 1. extreme rays that are found by taking the Ra boundary and differencing it from A and B
        extreme_rays_1 = (geom.boundary.difference(A)).difference(B)
        if extreme_rays_1.type == 'MultiLineString':
            for ggeom in extreme_rays_1:
                if ggeom.intersects(A) and ggeom.intersects(B):
                    extreme_rays.append(ggeom.wkt)
        elif extreme_rays_1.intersects(A) and extreme_rays_1.intersects(B):
            extreme_rays.append(extreme_rays_1.wkt)
        # Scenario 2. extreme rays (points) where A, B and Ra all meet each other
        extreme_rays_2 = geom.intersection(A).intersection(B)
        if extreme_rays_2.type == 'MultiLineString':
            for ggeom in extreme_rays_2:
                if not ggeom.is_empty:
                    extreme_rays.append(ggeom.wkt)
        elif not extreme_rays_2.is_empty:
            extreme_rays.append(extreme_rays_2.wkt)
        # Add the part of the ray area together with the related extreme rays to the result
        ray_area_with_extreme_rays.append((geom.wkt, extreme_rays))

    return ray_area_with_extreme_rays


def draw_ray_area(A,B):
    '''Calculate the ray area and extreme rays between two geometries A and B, and draw them with matplotlib.'''
    from osgeo import ogr
    from json import loads
    from descartes import PolygonPatch

    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    rcParams['figure.autolayout'] = True
    rcParams['figure.dpi'] = 300

    light_gray = '#d3d3d3'

    res = rayArea(A,B)

    fig = plt.figure(1)
    ax = fig.add_subplot(111)

    A = ogr.CreateGeometryFromWkt(A)
    B = ogr.CreateGeometryFromWkt(B)

    patch_A = PolygonPatch(loads(A.ExportToJson()), fc='gray')
    patch_B = PolygonPatch(loads(B.ExportToJson()), fc='gray')
    patches_ray_area = [PolygonPatch(loads(ogr.CreateGeometryFromWkt(item[0]).ExportToJson()), fc=light_gray) for item in res]

    ax.add_patch(patch_A)
    ax.add_patch(patch_B)
    for patch in patches_ray_area:
        ax.add_patch(patch)

    for item in res:
        for wkt in item[1]:
            geom = ogr.CreateGeometryFromWkt(wkt)
            x, y = zip(*[p for p in geom.GetPoints()])
            if len(x) > 1:
                ax.plot(x,y, color='red', zorder=10)
            else:
                ax.scatter(x,y, color='red', zorder=10)

    ax.axis('off')
    ax.autoscale_view()
    plt.show()



def RIM(A:str, B:str, O:str):
    '''Calculates RIM between two objects A and B. The objects have to be in WKT format.'''
    from osgeo import ogr
    import shapely.wkt, shapely.geometry
    import numpy as np

    floating_point_allowance = 0.000

    all_ray_areas = rayArea(A,B)
    A = shapely.wkt.loads(A)
    B = shapely.wkt.loads(B)
    O = shapely.wkt.loads(O)

    ray1 = np.array([[0,0,1],[0,0,1]])
    ray2 = np.array([[0,1,1],[0,0,1]])
    ray3 = np.array([[0,1,1],[0,1,1]])
    ray4 = np.array([[0,1,0],[0,1,0]])
    ray5 = np.array([[1,1,1],[0,0,1]])
    ray6 = np.array([[1,1,1],[0,1,1]])
    ray7 = np.array([[1,0,0],[0,1,0]])
    ray8 = np.array([[0,0,1],[0,1,1]])

    final_result = []
    for ray_area in all_ray_areas:
        Ra = shapely.wkt.loads(ray_area[0])
        # print(Ra.wkt)
        rays = []
        extreme_rays = []

        if O.disjoint(Ra):
            rays.append(ray1)
            # print('ray1')
        
        else:
            intersection = O.intersection(Ra)
            # prepare the placeholder for the difference of ra and o
            diff = []
            # this serves to remove the very very small polygons (result of the floating point error in GDAL topological functions) from the newly created difference of Ra and O
            difference = Ra.difference(O)
            if difference.geom_type == 'MultiPolygon':
                for geom in Ra.difference(O):
                    if geom.area > floating_point_allowance:
                        diff.append(geom)
                diff = shapely.geometry.MultiPolygon(diff)
            else:
                diff = difference
            diff_touches_AB = False
            if difference.geom_type == 'MultiPolygon':
                for geom in diff:
                    if geom.intersects(A) and geom.intersects(B):
                        diff_touches_AB = True
            elif diff.intersects(A) and diff.intersects(B):
                diff_touches_AB = True
            if diff_touches_AB:
                rays.append(ray1)
                # print('ray1')
                if not diff.equals(Ra):
                    rays.append(ray2)
                    # print('ray2')

            if diff_touches_AB and intersection.geom_type != 'Point' and (intersection.intersects(A) or intersection.intersects(B)):
                rays.append(ray3)
                # print('ray3')

            if diff_touches_AB and intersection.intersects(A) and intersection.intersects(B):
                rays.append(ray4)
                # print('ray4') 
            
            if (O.within(Ra) or O.overlaps(Ra)) and (diff.intersects(A) and diff.intersects(B)):
                rays.append(ray5)
                # print('ray5')

            if not diff.equals(Ra) and (diff.intersects(A) or diff.intersects(B)) and (intersection.intersects(A) or intersection.intersects(B)):
                rays.append(ray6)
                # print('ray6')

            if intersection.intersects(A) and intersection.intersects(B):
                rays.append(ray7)
                # print('ray7') 

        shrinked_O = O
        for extreme_ray in ray_area[1]:
            extreme_ray = shapely.wkt.loads(extreme_ray)
            if extreme_ray.disjoint(O):
                extreme_rays.append(ray1)
                # print('extreme ray1')
            elif (extreme_ray.intersects(O.boundary) and extreme_ray.disjoint(O)) and extreme_ray.boundary.disjoint(O):
                extreme_rays.append(ray2)
                # print('extreme ray2')
            elif extreme_ray.geom_type == 'LineString' and (extreme_ray.boundary[0].intersects(O.boundary) ^ extreme_ray.boundary[1].intersects(O.boundary)) and extreme_ray.disjoint(O):
                extreme_rays.append(ray3)
                # print('extreme ray3')
            elif extreme_ray.within(O.boundary):
                extreme_rays.append(ray4)
                # print('extreme ray4')
            elif extreme_ray.geom_type == 'LineString' and extreme_ray.boundary.disjoint(O) and extreme_ray.intersects(O):
                extreme_rays.append(ray5)
                # print('extreme ray5')
            elif extreme_ray.geom_type == 'LineString' and not diff.equals(Ra) and (extreme_ray.boundary[0].intersects(O.boundary) ^ extreme_ray.boundary[1].intersects(O.boundary)):
                extreme_rays.append(ray6)
                # print('extreme ray6')
            elif extreme_ray.within(O):
                extreme_rays.append(ray7)
                # print('extreme ray7')
            elif extreme_ray.touches(O):
                extreme_rays.append(ray8)
                # print('extreme ray8')
        
        RIM_part = sum(rays + extreme_rays)/len(rays + extreme_rays)
        RIM_part2 = sum(extreme_rays)/len(extreme_rays)
        RIM_all = np.concatenate((RIM_part, RIM_part2))
        # normalize all values between 0 and 1 (triangle) to 0.5
        RIM_all[(RIM_all>0) & (RIM_all<1)] = 0.5
        final_result.append(list(RIM_all.flatten()))

        known_rims = {
            '[0.5, 0.5, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0]' : 'RIM 1',
            '[0.5, 0.5, 1.0, 0.0, 0.5, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0]' : 'RIM 2',
            '[0.5, 0.5, 0.5, 0.0, 0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0]' : 'RIM 3',
            '[0.5, 0.5, 1.0, 0.0, 0.0, 1.0, 0.0, 0.5, 1.0, 0.0, 0.0, 1.0]' : 'RIM 4',
            '[0.5, 0.5, 1.0, 0.0, 0.5, 1.0, 0.0, 0.5, 1.0, 0.0, 0.5, 1.0]' : 'RIM 5',
            '[0.5, 0.5, 0.5, 0.0, 0.5, 0.5, 0.0, 0.5, 1.0, 0.0, 0.5, 1.0]' : 'RIM 6',
            '[0.5, 0.5, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0]' : 'RIM 7',
            '[0.5, 0.5, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0]' : 'RIM 8',
            '[0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0]' : 'RIM 9',
            '[0.5, 0.5, 1.0, 0.0, 0.0, 1.0, 0.5, 1.0, 1.0, 0.0, 0.0, 1.0]' : 'RIM 10',
            '[0.5, 1.0, 1.0, 0.0, 1.0, 1.0, 0.5, 1.0, 1.0, 0.0, 1.0, 1.0]' : 'RIM 11',
            '[0.5, 0.5, 0.0, 0.0, 1.0, 0.0, 0.5, 0.5, 1.0, 0.0, 1.0, 1.0]' : 'RIM 12',
            '[1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0]' : 'RIM 13',
            '[1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0]' : 'RIM 14',
            '[1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0]' : 'RIM 15',
            '[0.5, 0.5, 1.0, 0.0, 0.0, 1.0, 0.5, 0.5, 1.0, 0.0, 0.0, 1.0]' : 'RIM 16',
            '[0.5, 0.5, 1.0, 0.0, 0.5, 1.0, 0.5, 0.5, 1.0, 0.0, 0.5, 1.0]' : 'RIM 17',
            '[0.5, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.0, 0.5, 0.0, 0.5, 0.5]' : 'RIM 18',
            '[0.0, 0.5, 1.0, 0.0, 0.0, 1.0, 0.0, 0.5, 1.0, 0.0, 0.0, 1.0]' : 'RIM 19',
            '[0.0, 0.5, 1.0, 0.0, 0.5, 1.0, 0.0, 0.5, 1.0, 0.0, 0.5, 1.0]' : 'RIM 20',
            '[0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.0, 0.5, 0.5]' : 'RIM 21',
            '[0.0, 0.0, 1.0, 0.0, 0.5, 1.0, 0.0, 0.0, 1.0, 0.0, 0.5, 1.0]' : 'RIM 22',
            '[0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0]' : 'RIM 23',
            '[0.5, 0.5, 1.0, 0.0, 0.5, 1.0, 0.5, 0.5, 1.0, 0.0, 0.0, 1.0]' : 'RIM 24',
            '[1.0, 1.0, 1.0, 0.0, 0.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.5, 1.0]' : 'RIM 25',
            '[1.0, 1.0, 1.0, 0.0, 0.5, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0]' : 'RIM 26',
            '[0.5, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.0, 0.5, 1.0]' : 'RIM 27',
            '[0.5, 0.5, 0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.0, 0.0, 1.0]' : 'RIM 28',
        }
        final_result = [known_rims.get(str(rim),rim) for rim in final_result]

        if len(final_result) > 1:
            final_result = [x for x in final_result if x != 'RIM 23']
        if len(final_result) == 1:
            final_result = final_result[0]
    return final_result
