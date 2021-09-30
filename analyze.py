import cv2
import numpy as np
from argparse import Namespace


# Global parameters
jpeg_extensions = ['jpeg', 'jpg', 'jpe', 'jfif', 'jif', '.jpeg', '.jpg', '.jpe', '.jfif', '.jif', 'JPEG', 'JPG', 'JPE', 'JFIF', 'JIF', '.JPEG', '.JPG', '.JPE', '.JFIF', '.JIF']
png_extensions = ['png', '.png', 'PNG', '.PNG']


# PREPROCESSING

# RGB to YCbCr conversion & luminance channel extraction
def luminance(img):
    # Convert image
    img_y = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    y, _, _ = cv2.split(img_y)

    return y


# Median filter residual
def mfr(img, size):
    # Ref.: https://www.researchgate.net/figure/Median-filter-residual_fig1_341836414

    median = cv2.medianBlur(img, size)
    residual = img - median

    return residual


# Adjust image size (uses padding; for square window partitioning)
def adjust_size(img, win_size, stride):
    # Check image size and add padding if needed
    img_h, img_w = get_image_size(img)

    if img_h % stride != 0 or img_h % win_size != 0:
        img = cv2.copyMakeBorder(img, 0, stride - img_h % stride, 0, 0, cv2.BORDER_REPLICATE)

    if img_w % stride != 0 or img_w % win_size != 0:
        img = cv2.copyMakeBorder(img, 0, 0, 0, stride - img_w % stride, cv2.BORDER_REPLICATE)

    return img


# Calculate overlapping windows of given size (extracted with given stride; non-overlapping if stride is zero)
# and return their average block
# along with their starting coordinates and ID in order to map them to each pixel (for postprocessing)
def get_average_window_blocks(img, win_size, stride, block_size):
    # Adjust image size
    img = adjust_size(img, win_size, stride)
    img_h, img_w = get_image_size(img)

    # Calculate starting coordinates for each window (top left pixel)
    x = []
    y = []

    for i in range(0, img_w - win_size + 1, stride):
        x.append(i)

    for j in range(0, img_h - win_size + 1, stride):
        y.append(j)

    # Variable initialization
    window_id = 0  # Simple index to keep track of the current window
    blocks = np.zeros((len(x)*len(y), block_size, block_size))  # Final array of blocks (there is one block per window)
    blocks_map = np.zeros((len(x)*len(y), 3), dtype=np.int)  # Each row of blocks_map contains the coordinates of the top left pixel of the window (columns 0 and 1) and its ID (column 2)

    # Window average and mapping
    for i in y:
        for j in x:
            # Get current window blocks
            current_window_blocks = get_non_overlapping_blocks(img[i:i + win_size, j:j + win_size], block_size)

            # Calculate average block for the current window
            sum_block = np.sum(current_window_blocks, axis=0)
            blocks[window_id] = sum_block / len(current_window_blocks)

            # Update blocks map
            blocks_map[window_id, 0] = j
            blocks_map[window_id, 1] = i
            blocks_map[window_id, 2] = window_id

            # Update ID
            window_id += 1

    return blocks, blocks_map


# Non-overlapping blocks of given size
def get_non_overlapping_blocks(window, block_size):
    # Calculate starting coordinates for each window (top left pixel)
    x = []
    y = []

    for i in range(0, window.shape[0] - block_size, block_size):
        x.append(i)
        y.append(i)

    # Variable initialization
    window_id = 0
    blocks = np.zeros((len(x)*len(y), block_size, block_size))

    # Calculate blocks
    for i in y:
        for j in x:
            blocks[window_id] = window[i:i + block_size, j:j + block_size]
            window_id += 1

    return blocks


# EM ALGORITHM


# Expectation step
def expectation(blocks, c, prob_r_b_in_c1, first_iteration=False):

    # Compute correlation r
    r = np.zeros(blocks.shape[0])
    for i in range(blocks.shape[0]):
        r[i] = np.corrcoef(blocks[i].flatten(), c.flatten())[0, 1]

    # Initialize probabilities
    prob_b_in_c1 = np.ones(blocks.shape[0]) * 0.5
    prob_b_in_c2 = np.ones(blocks.shape[0]) * 0.5

    if first_iteration:  # The first iteration uses arbitrary probabilities
        prob_r_b_in_c1 = np.ones(blocks.shape[0]) * prob_r_b_in_c1
        prob_r_b_in_c2 = 1 - prob_r_b_in_c1
    else:  # Successive iterations are estimated by the correlation r
        prob_r_b_in_c1 = abs(r)
        prob_r_b_in_c2 = 1 - prob_r_b_in_c1

    # Calculate conditional probability of each block b of belonging to c1 given the correlation r
    num = prob_r_b_in_c1 * prob_b_in_c1
    den = prob_r_b_in_c1 * prob_b_in_c1 + prob_r_b_in_c2 * prob_b_in_c2

    prob_b_in_c1_r = num / den

    return prob_b_in_c1_r


# Maximization step
def maximization(blocks, prob_b_in_c1_r):
    # Calculate template c
    num = np.sum(np.array([prob_b_in_c1_r * blocks for (prob_b_in_c1_r, blocks) in zip(prob_b_in_c1_r, blocks)]), axis=0)
    den = np.sum(prob_b_in_c1_r, axis=0)

    c = num / den

    return c


# Expectation-maximization algorithm
def expectation_maximization(blocks, threshold, prob_r_b_in_c1):
    # Initialize logging array for the differences plot
    diff_history = []

    # Random initialize template c
    c = np.random.uniform(0, 1, (8, 8))

    # Initialize difference matrix
    diff = np.ones((8, 8))  # Difference between successive estimates of c is an 8x8 matrix

    # First iteration
    prob_b_in_c1_r = expectation(blocks, c, prob_r_b_in_c1, first_iteration=True)
    c = maximization(blocks, prob_b_in_c1_r)

    # Main EM loop
    while np.all(diff > threshold):  # Iterate E-M steps until difference is lower than threshold
        # Store last iteration's template
        c_prev = np.copy(c)

        # E step
        prob_b_in_c1_r = expectation(blocks, c, prob_r_b_in_c1)

        # M step
        c = maximization(blocks, prob_b_in_c1_r)

        # Calculate difference between successive estimates of c
        diff = abs(c - c_prev)
        diff_history.append(np.average(diff))  # Add the difference matrix' average to the difference log

    return prob_b_in_c1_r, c, diff_history


# POSTPROCESSING

# Get output map
def get_output_map(prob_b_in_c1_r, blocks_map, img_w, img_h, show=False, save=False, img_path=None, win_size=None, stop_threshold=None):

    # Initialize empty map
    output_map = np.empty((img_h, img_w, 2))

    for w in blocks_map:  # For each element in the window list...
        output_map[w[1]:w[1] + win_size, w[0]:w[0] + win_size, 0] += prob_b_in_c1_r[w[2]]
        output_map[w[1]:w[1] + win_size, w[0]:w[0] + win_size, 1] += 1

    for i in range(0, output_map.shape[0]):  # Average
        for j in range(0, output_map.shape[1]):
            output_map[i, j, 0] = output_map[i, j, 0] / output_map[i, j, 1]

    output_map = 1 - output_map[:, :, 0]  # Because the map computed so far actually shows the probability that a pixel has not been modified

    # Replace NaNs with a neutral probability (0.5)
    output_map = np.nan_to_num(output_map, nan=0.5)

    # Thresholding & normalization
    output_map_norm = np.where(output_map > 0.8, 255, 0).astype(np.uint8)  # Pixels with probability of being manipulated lower than 80% are masked

    return output_map_norm


# UTILS

# Load image
def load_image(img_path, raise_io=True):
    # Load image
    img = cv2.imread(img_path)

    # Check image correctness
    if img is not None:
        return img
    elif raise_io:
        raise IOError('Error while loading image: invalid image file or image file path.')
    else:
        return None


# Get image size (regardless of number of channels)
def get_image_size(img):
    if len(img.shape) == 3:
        img_h, img_w, _ = img.shape
    elif len(img.shape) == 2:
        img_h, img_w = img.shape
    else:
        raise RuntimeError('Incorrect input image shape.')

    return img_h, img_w


# Get filename from path
def get_filename(file_path):
    tmp_filename = file_path.split('/')[-1]
    extension = tmp_filename.split('.')[-1]
    tmp_filename = tmp_filename.split('.')[:-1]

    if len(tmp_filename) > 1:
        filename = tmp_filename[0]
        for el in tmp_filename[1:]:
            filename += '.' + el
    else:
        filename = tmp_filename[0]

    return filename, extension


# MAIN

def main(img_path):
    # Arguments
    args = Namespace()
    args.img_path = img_path
    args.win_size = 64
    args.stop_threshold = 1e-3
    args.prob_r_b_in_c1 = 0.3
    args.show = False
    args.save = False
    args.show_roc_plot = False
    args.save_roc_plot = False
    args.show_diff_plot = False
    args.save_diff_plot = False

    # Load image
    img = load_image(args.img_path)

    # RGB to YCbCr conversion & luminance channel extraction
    lum = luminance(img)

    # 3x3 median filter residual
    filtered_lum = mfr(lum, 3)

    # Average blocks from overlapping windows generation
    blocks, blocks_map = get_average_window_blocks(filtered_lum, args.win_size, 8, 8)

    # Expectation-maximization algorithm
    prob_b_in_c1_r, c, diff_history = expectation_maximization(blocks, args.stop_threshold, args.prob_r_b_in_c1)

    # Output map & difference plot
    output_map = get_output_map(prob_b_in_c1_r, blocks_map, img.shape[1], img.shape[0], args.show, args.save, args.img_path, args.win_size, args.stop_threshold)

    return output_map
