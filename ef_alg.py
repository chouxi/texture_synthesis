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
from skimage import io, morphology
import matplotlib.pyplot as plt
import random
import time
from scipy import signal

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
    count_mask = np.ones((3,3))
    count_mask[1][1] = 0
    dilation_mat = np.ones((3,3))
    dilation_mask = morphology.dilation(visited_mat, selem=dilation_mat) - visited_mat
    count_dict = {}
    x,y = dilation_mask.shape
    for (i,j),v in np.ndenumerate(dilation_mask):
        if v == 1:
            tmp = visited_mat[max(0, i-1):min(i+2,x) , max(0, j-1):min(y,j+2)]
            count = int(np.multiply(tmp, count_mask[max(0, 1-i):min(3, 3+min(x-i-2, 0)), max(0, 1-j):min(3, 3+min(y-j-2, 0))]).sum())
            if count_dict.has_key(count):
                count_dict[count].append((i,j))
            else:
                count_dict.setdefault(count, [(i,j)])
    count_list = count_dict.keys()
    count_list.sort()
    unfilled_list = []
    for key in count_list:
        unfilled_list += count_dict[key]
    '''
    # plain brute implementation
    direction = [(0,1), (0,-1), (-1,0), (1,0),(-1,1),(1,1),(-1,-1),(1,-1)]
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
    '''
    return unfilled_list

def get_neighborwind(image, window_size, pixel):
    x,y = image.shape
    margin = window_size / 2
    # return indexs instead of the matrix
    return [max(0, pixel[0] - margin),min(x, pixel[0]+1 + margin), max(0, pixel[1]-margin),min(y,pixel[1]+1+margin)]
    
def find_matches(template, image, sample,visited_mat, window_size, center, err_threshold,gauss_mask):
    valid_mask = visited_mat[template[0]:template[1], template[2]: template[3]]
    template_block = image[template[0]:template[1], template[2]: template[3]]
    margin = window_size / 2
    # get the gauss_mask, shift it make it same to the shape of valid_mask
    gauss_mask = gauss_mask[template[0] - (center[0]-margin):window_size + (template[1] - (center[0] + 1 + margin)), template[2] - (center[1]-margin):window_size + (template[3] - (center[1] + 1 + margin))]
    if gauss_mask.shape != valid_mask.shape:
        print "[ERROR] gauss_mask shape " + str(gauss_mask.shape) + " is not equal to the valid_mask shape " + str(valid_mask.shape) +""
    weight_mat = np.multiply(gauss_mask, valid_mask)
    total_weight = weight_mat.sum()
    sample_size = sample.shape
    SSD = np.zeros((sample_size[0] - 2*margin, sample_size[1]-2*margin))
    for x in range(margin, sample_size[0] - margin):
        for y in range(margin, sample_size[1] - margin):
            sample_block = sample[(x - margin):(x+1 + margin),(y-margin):(y+1+margin)]
            # shift sample_block to the same as template
            sample_block = sample_block[template[0] - (center[0]-margin):window_size + (template[1] - (center[0] + 1 + margin)), template[2] - (center[1]-margin):window_size + (template[3] - (center[1] + 1 + margin))]
            if sample_block.shape != valid_mask.shape:
                print "[ERROR] sample_block shape " + str(sample_block.shape) + " is not equal to the valid_mask shape " + str(valid_mask.shape) +"."
            SSD[x-margin,y-margin] = (np.multiply(weight_mat, np.square(template_block-sample_block)).sum()) / total_weight
    threshold= SSD.min()*(1+err_threshold)
    pixel_list = []
    for x in range(SSD.shape[0]):
        for y in range(SSD.shape[1]):
            if SSD[x,y] <= threshold:
                pixel_list.append((x + margin,y + margin,SSD[x,y]))
    return pixel_list

def grow_image(sample, image, visited_mat, window_size, err_threshold, max_err_threshold):
    # window_size need to be odd number
    if window_size & 1 == 0:
        window_size += 1
    sigma = window_size / 6.4
    gauss_mask =gaussian2D(window_size, sigma)
    while 1:
        flag = 0
        pixel_list = get_unfilled_neighbor(visited_mat)
        if len(pixel_list) == 0:
            break
        for pixel in pixel_list:
            template = get_neighborwind(image, window_size, pixel)
            start = time.time()
            matches_list = find_matches(template,image, sample, visited_mat, window_size, pixel, err_threshold, gauss_mask)
            end = time.time()
            print end - start
            match_pixel = matches_list[random.randrange(len(matches_list))]
            if match_pixel[2] < max_err_threshold:
                image[pixel[0],pixel[1]] = sample[match_pixel[0], match_pixel[1]]
                visited_mat[pixel[0],pixel[1]] = 1
                flag = 1
        if flag == 0:
            max_err_threshold *= 1.1
        #io.imshow(image)
        #io.show()

def do_efros(sample, new_x, new_y, window_size):
    err_threshold = 0.1
    max_err_threshold = 0.3
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
    grow_image(sample, image, visited_mat, window_size, err_threshold, max_err_threshold)
    io.imshow(image, cmap='gray')
    io.show()

if __name__ == '__main__':
    sample = io.imread('./pics/T1.gif')
    do_efros(sample, 200, 200, 5)
