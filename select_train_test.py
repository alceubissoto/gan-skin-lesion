import glob
import numpy as np
import shutil

lesion_arr = []
np.random.seed(0)

for lesion in glob.glob('pix2pixHD/datasets/skin/train_label/*.png'):
        print(lesion)
        case = lesion.split('/')[-1].split('_')[1]
        print(case)
        lesion_arr.append(case)

# Randomly select 150 samples to compose our test dataset.
test = np.random.choice(lesion_arr, 250, replace=False)
# Move the selected files to the correspondent test directory.
for case in test:
        shutil.move('pix2pixHD/datasets/skin/train_label/ISIC_'+case+'_semantic.png', 'pix2pixHD/datasets/skin/test_label/')
        shutil.move('pix2pixHD/datasets/skin/train_inst/ISIC_'+case+'_instance.png', 'pix2pixHD/datasets/skin/test_inst/')
        shutil.move('pix2pixHD/datasets/skin/train_img/ISIC_'+case+'.png', 'pix2pixHD/datasets/skin/test_img/')
