import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
import os
from tqdm import tqdm

atri_dir = 'attribute_resized/'
mask_dir = 'segmentation_resized/'
output_dir = 'semantic_map/'

file_name_arr = [] # [ISIC_00000, ISIC_000001, ISIC_000003, ...]
for file in glob.glob(atri_dir+'*.png'):
	temp = file.split('/')[-1].split('_')
	file_name = temp[0]+'_'+temp[1]
	if file_name not in file_name_arr:
	    file_name_arr.append(file_name)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for family in tqdm(file_name_arr):
	# Create a zero filled base image
	for i, file in enumerate(glob.glob(atri_dir+family+'*.png')):
		# Read the image
		read_image = misc.imread(file, flatten=True)
		border_color = read_image[0,0]
		read_image[read_image == border_color] = 0
		read_image[read_image > 0] = 255
		read_image = np.int8(read_image/255)

		if i == 0:
			mask = misc.imread(mask_dir+family+'_segmentation.png', flatten=True)
			base_image = np.ones(read_image.shape, dtype=int) # Healthy Skin is 1
			border_mask_color = mask[0,0]
			base_image[mask == border_mask_color] = 0
			mask[mask == border_mask_color] = 0
			mask[mask > 0] = 255
			mask = np.int8(mask/255)
			base_image += mask # Common Lesion is 2

		type_file = file.split('/')[-1].split('_')[3]

		if type_file == 'pigment': # 3
			base_image += read_image
			if base_image[base_image > 3].any():
				base_image[base_image > 3] = 3
		elif type_file == 'negative': # 4
			base_image += read_image*2
			if base_image[base_image > 4].any():
				base_image[base_image > 4] = 4
		elif type_file.startswith('streaks'): # 5
			base_image += read_image*3
			if base_image[base_image > 5].any():
				base_image[base_image > 5] = 5
		elif type_file == 'milia': # 6
			base_image += read_image*4
			if base_image[base_image > 6].any():
				base_image[base_image > 6] = 6
		elif type_file.startswith('globules'): #7
			base_image += read_image*5
			if base_image[base_image > 7].any():
				base_image[base_image > 7] = 7
		else:
			print('ERROR: Invalid File Found!!!!')
	misc.toimage(base_image, cmin=0, cmax=255).save(output_dir+family+'_semantic.png')
