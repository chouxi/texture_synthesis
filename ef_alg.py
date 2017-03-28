'''
# =============================================================================
#      FileName: ef_alg.py
#          Desc: 
#        Author: ZaneQi
#         Email: qizheng1993hit@gmail.com
#      HomePage: https://github.com/chouxi
#       Version: 0.0.1
#    LastChange: 2017-03-28 10:56:33
#       History:
# =============================================================================
'''
import numpy as np
from skimage import io, morphology
import matplotlib.pyplot as plt
import random
import time
from scipy import signal

def gaussian2D(shape, sigma = 1, center=None):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

def get_unfilled_neighbor(visited_mat, margin):
    count_mask = np.ones((3,3))
    count_mask[1][1] = 0
    dilation_mat = np.ones((3,3))
    dilation_mask = morphology.dilation(visited_mat, selem=dilation_mat) - visited_mat
    count_dict = {}
    x,y = dilation_mask.shape
    for (i,j),v in np.ndenumerate(dilation_mask):
        if v == 1 and i >= margin and i < x - margin and j >= margin and j < y-margin:
            tmp = visited_mat[i-1:i+2 , j-1:j+2]
            count = int(np.multiply(tmp, count_mask).sum())
            if count_dict.has_key(count):
                count_dict[count].append((i,j))
            else:
                count_dict.setdefault(count, [(i,j)])
    count_list = count_dict.keys()
    count_list.sort(reverse=True)
    unfilled_list = []
    for key in count_list:
        unfilled_list += count_dict[key]
    return unfilled_list

def get_neighborwind(image, window_size, pixel, margin):
    x,y = image.shape
    # return indexs instead of the matrix
    return [pixel[0] - margin, pixel[0]+1 + margin, pixel[1]-margin, pixel[1]+1+margin]
    
def find_matches(template, image, sample,visited_mat, err_threshold,gauss_mask, sample_block_list, coordinate_list):
    valid_mask = visited_mat[template[0]:template[1], template[2]: template[3]]
    template_block = image[template[0]:template[1], template[2]: template[3]]
    # get the gauss_mask, shift it make it same to the shape of valid_mask
    if gauss_mask.shape != valid_mask.shape:
        print "[ERROR] gauss_mask shape " + str(gauss_mask.shape) + " is not equal to the valid_mask shape " + str(valid_mask.shape) +""
    weight_mat = np.multiply(gauss_mask, valid_mask)
    total_weight = weight_mat.sum()
    template_block_list = np.tile(template_block, (len(sample_block_list),1,1))
    SSD = np.sum(np.sum(np.multiply(weight_mat, np.square(template_block_list - sample_block_list)), axis=1), axis=1) / total_weight
    threshold= SSD.min()*(1+err_threshold)
    pixel_list = []
    for error,coor in zip(SSD, coordinate_list):
        if error <= threshold:
            pixel_list.append((coor, error))
    return pixel_list

def grow_image(sample, image, visited_mat, window_size, err_threshold, max_err_threshold, margin):
    # get gauss2D
    sigma = window_size / 6.4
    gauss_mask =gaussian2D((window_size, window_size), sigma)
    # get sample block list
    sample_size = sample.shape
    sample_block_list = []
    # get coorsponding coordinate
    coordinate_list = []
    for x in range(margin, sample_size[0]-margin):
        for y in range(margin, sample_size[1] -margin):
            sample_block_list.append(sample[(x - margin):(x+1 + margin),(y-margin):(y+1+margin)])
            coordinate_list.append((x,y))
    while 1:
        flag = 0
        pixel_list = get_unfilled_neighbor(visited_mat, margin)
        if len(pixel_list) == 0:
            break
        for pixel in pixel_list:
            template = get_neighborwind(image, window_size, pixel, margin)
            #start = time.time()
            matches_list = find_matches(template, image, sample, visited_mat, err_threshold, gauss_mask, np.asarray(sample_block_list), coordinate_list)
            #end = time.time()
            #print end - start
            if matches_list == 1:
                match_pixel = matches_list[0]
            else:
                match_pixel = matches_list[random.randrange(len(matches_list))]
            if match_pixel[1] < max_err_threshold:
                image[pixel[0],pixel[1]] = sample[match_pixel[0]]
                visited_mat[pixel[0],pixel[1]] = 1
                flag = 1
        if flag == 0:
            max_err_threshold *= 1.1
        #io.imshow(image)
        #io.show()

def do_efros(sample, new_x, new_y, window_size):
    # normalize
    sample *= (1.0/sample.max())
    err_threshold = 0.1
    max_err_threshold = 0.3
    # window_size need to be odd number
    if window_size & 1 == 0:
        window_size += 1
    margin = window_size / 2
    sample_x, sample_y = sample.shape
    new_x += margin*2
    new_y += margin*2
    #init mats
    image = np.zeros((new_x,new_y))
    visited_mat = np.zeros((new_x,new_y))
    # put sample into the image 
    start_x = new_x / 2 - 1
    start_y = new_y / 2 - 1
    rand_x = random.randrange(sample_x-3)
    rand_y = random.randrange(sample_y-3)
    image[start_x: (start_x + 3), start_y:(start_y + 3)] = sample[rand_x: rand_x+3, rand_y:rand_y + 3]
    visited_mat[start_x: (start_x + 3), start_y:(start_y + 3)] = 1
    grow_image(sample, image, visited_mat, window_size, err_threshold, max_err_threshold, margin)
    image = image[margin: new_x - margin, margin: new_y - margin] *255
    #io.imshow(image, cmap='gray')
    io.imshow(image)
    io.show()

if __name__ == '__main__':
    sample = io.imread('./pics/T1.gif').astype('float64')
    start = time.time()
    do_efros(sample, 200, 200, 11)
    end = time.time()
    print end - start
