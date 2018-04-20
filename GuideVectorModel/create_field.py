###        given a matrix of pixel values, this function returns a field of vectors               ###
###  assumes: (1) pixels along correct path have value 1, (2), pixels in open space have value 0  ###
###                     and (3) pixel for obstacles have value -1                                 ###
###                         the example matrix used here is:                                      ###
###                         [[ 0.  0.  0.  0.  0.  0.  0.  0.]                                    ###
###                          [ 0.  1.  1.  1.  1.  1.  1.  0.]                                    ###
###                          [ 0.  1.  0.  0.  0.  0.  0.  1.]                                    ###
###                          [ 0.  1.  0.  0. -1. -1.  0.  1.]                                    ###
###                          [ 0.  1.  0.  0. -1. -1.  0.  1.]                                    ###
###                          [ 0.  1.  0. -1. -1. -1.  0.  1.]                                    ###
###                          [ 1.  0.  0. -1. -1. -1.  0.  1.]                                    ###
###                          [ 1.  0.  0. -1. -1. -1.  0.  0.]]                                   ###


import numpy as np
import matplotlib.pyplot as plt

#### TO DO: 1) improve the theta calculation -- should be a function of the distance to the nearest point on the path
####        2) improve how the tangents are calculated
def create_field(E, theta=.9):
    def get_dist(v1,v2):
        assert len(v1) == len(v2), 'vector lengths not the same, cant calculate norms'
        return [np.linalg.norm(np.array(v1[i]) - np.array(v2[i]),2) for i in range(len(v1))]

    def compute_lattice_map(E):
        map = {}
        n_row = E.shape[0]
        for i in range(E.shape[0]):
            for j in range(E.shape[1]):
                map[(j,n_row-i-1)] = E[i,j]

        return map

    def get_nearest_point_on_path(target_ix, path_ix):
        nearest_point_on_path = {}  # dictionary with key: point, value: nearest point on path

        for ix in target_ix:
            rep_ix = [ix] * len(path_ix)
            d = get_dist(rep_ix, path_ix)
            min_ix = np.argmin(d)
            nearest_point_on_path[ix] = path_ix[min_ix]

        return nearest_point_on_path

    def get_direction_to_path(nearest_point_on_path):
        direction_to_path = {}

        for i in nearest_point_on_path.keys():
            direction_to_path[i] = np.array(list(nearest_point_on_path[i])) - np.array(list(i))
            if np.linalg.norm(direction_to_path[i],2) != 0:
                direction_to_path[i] = (direction_to_path[i]/np.linalg.norm(direction_to_path[i],2)).tolist() #get a unit vector
            else:
                direction_to_path[i] = direction_to_path[i].tolist()

        return direction_to_path

    def careful_sign(x):
        if x == 0.:
            return 1.0
        else:
            return np.sign(x)

    def get_tangent_direction(path_ix):
        tangent_direction = {}
        for ix in path_ix:
            x = ix[0]
            y = ix[1]

            ### get box around (x,y) to calculate average tangent #####
            tp = [(x + i, y + j) for i in range(10) for j in range(10) if j+i != 0]
            tn = [(x - i, y - j) for i in range(10) for j in range(10) if j+i != 0]

            test_points = tp + tn

            ### **** old way of doing it **** ####
            #test_points = [(x-1,y-1), (x-1,y), (x-1, y+1), (x, y-1), (x,y+1), (x+1, y-1), (x+1,y), (x+1,y+1)]

            neighbors = [pt for pt in test_points if pt in path_ix]
            tangents = [(np.array(pt)-np.array(ix))*careful_sign(pt[0]-x) for pt in neighbors]
            tangent_direction[ix] = np.mean(tangents, axis=0)
            if np.linalg.norm(tangent_direction[ix]) != 0:
                tangent_direction[ix] = tangent_direction[ix]/np.linalg.norm(tangent_direction[ix])

        return tangent_direction

    def map_to_matrix(direction, n_row, n_col):
        Xdir = np.zeros((n_row,n_col))
        Ydir = np.zeros((n_row,n_col))

        for point in direction.keys():
            x,y = point[0], point[1]
            xdir,ydir = direction[point][0], direction[point][1]
            Xdir[n_row-y-1, x] = xdir
            Ydir[n_row-y-1, x] = ydir

        return Xdir, Ydir



    ### translate into coordinate system in first quadrant
    map = compute_lattice_map(E)
    n_row = E.shape[0]
    n_col = E.shape[1]
    path_ix = [i for i in map.keys() if map[i] == 1.0]

    nearest_point_on_path = get_nearest_point_on_path(map.keys(), path_ix)
    direction_to_path = get_direction_to_path(nearest_point_on_path)
    tangent_direction = get_tangent_direction(path_ix)

    direction = {}
    for point in map.keys():
        direction[point] = theta*np.array(direction_to_path[point]) + (1-theta)*np.array(tangent_direction[nearest_point_on_path[point]])

    Xdir, Ydir = map_to_matrix(direction, n_row, n_col)

    return Xdir, Ydir


if __name__ == '__main__':
    ### example matrix

    E = np.zeros((20, 20))
    E[0,0:2]=1
    E[1,1:3]=1
    E[2,2:4]=1
    E[3:5,3]=1
    E[6, 0] = 1
    E[7, 0] = 1
    E[1:6, 1] = 1
    E[1:2, 2] = 1
    E[1, 3:7] = 1
    E[2:7, 7] = 1

    E[3:8, 4] = -1
    E[3:8, 5] = -1
    E[5:8, 3] = -1

    Xdir, Ydir = create_field(E)
    X,Y = np.meshgrid(range(E.shape[0]), range(E.shape[1]))

    print('Original Matrix', E)
    #print('X component of vectors', Xdir)
    #print('Y component of vectors', Ydir)

    plt.quiver(X,Y,Xdir,Ydir)
    #plt.imshow(Xdir)
    #plt.colorbar()
    plt.show()
    #plt.imshow(Ydir)

