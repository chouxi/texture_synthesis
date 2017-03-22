'''
# =============================================================================
#      FileName: ef_alg.py
#          Desc: 
#        Author: ZaneQi
#         Email: qizheng1993hit@gmail.com
#      HomePage: https://github.com/chouxi
#       Version: 0.0.1
#    LastChange: 2017-03-21 18:55:58
#       History:
# =============================================================================
'''
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
def gaussian2D(size, sigma = 1, center=None):
    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]

    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]
    return np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / sigma**2)

def get_unfilled_neighbor(visited_mat):
    direction = [(0,1), (0,-1), (-1,0), (1,0)]
    x, y = visited_mat.shape
    unfilled_list = []
    for i in range(x):
        for j in range(y):
            if visited_mat[i][j] == 0:
                for k in range(len(direction)):
                    diff_x = direction[k][0]
                    diff_y = direction[k][1]
                    if i + diff_x >= 0 and i + diff_x < (x - 1) and j+diff_y >= 0 and j + diff_y < (y-1) and visited_mat[i+diff_x][j + diff_y] == 1:
                        unfilled_list.append((i, j))
                        break
    return unfilled_list

def get_neighborwind(image, window_size, pixel):
    x,y = image.shape
    # window_size need to be odd number
    if window_size & 1 == 0:
        window_size += 1
    margin = window_size / 2
    #return image[max(0, pixel[0] - margin):min(x - 1, pixel[0] + margin), max(0, pixel[1]-margin):min(y - 1,pixel[1]+margin)]
    return [max(0, pixel[0] - margin),min(x - 1, pixel[0] + margin), max(0, pixel[1]-margin),min(y - 1,pixel[1]+margin)]
    
def find_matches(template, sample,visited_mat, window_size):
    sigma = 0.3
    valid_mask = visited_mat[template[0]:template[1], template[2]: template[3]]
    #sigma_mat = np.ones((2,2)) *sigma
    #gauss_mask = np.random.multivariate_normal([window_size/2+1,window_size/2+1],sigma_mat, (window_size,window_size))
    gauss_mask = gaussian2D(window_size, sigma)

def grow_image(sample, image, visited_mat, window_size):
    while 1:
        pixel_list = get_unfilled_neighbor(visited_mat)
        if len(pixel_list) == 0:
            break
        for pixel in pixel_list:
            template = get_neighborwind(image, window_size, pixel)
            find_matches(template, sample, visited_mat, window_size)
            visited_mat[pixel[0],pixel[1]] = 1
            break
        break

def do_efros(sample, new_x, new_y, window_size):
    size = sample.shape
    if new_x < size[0] or new_y < size[1]:
        print '[ERROR] new size smaller than sample'
    #init mats
    image = np.zeros((new_x,new_y))
    visited_mat = np.zeros((new_x,new_y))
    # put sample into the image 
    start_x = new_x / 2 - size[0]/2
    start_y = new_y / 2 - size[1]/2
    image[start_x: (start_x + size[0]), start_y:(start_y + size[1])] = sample
    visited_mat[start_x: (start_x + size[0]), start_y:(start_y + size[1])] = 1
    grow_image(sample, image, visited_mat, window_size)
    #io.imshow(image)
    #io.show()

sample = io.imread('./pics/T1.gif')
do_efros(sample, 200, 200, 5)
