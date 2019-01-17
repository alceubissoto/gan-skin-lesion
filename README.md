# gan-skin-lesion
### Code to reproduce the results for the paper "Skin Lesion Sythesis with Generative Adversarial Networks" in ISIC Skin Image Analysis Workshop and Challenge @ MICCAI 2018.
In this repository you will find the code to generate the "Instance" and "Semantic" images. The network used is pix2pixHD, which is referenced below. You can find our PGAN modification in the link [soon] and the classification network used for our tests [here](https://github.com/learningtitans/isic2018-part3).

# Preparing the data and environment
### Configuring the container.
All tests done were using nvidia-docker.
Run this command to configure a container containing tensorflow:

`nvidia-docker run -ti --userns=host --shm-size 8G  -v /home/gan-skin-lesion/:/gan-skin-lesion/ --name ganskinlesion -p 8008:8008 tensorflow/tensorflow:nightly-devel-gpu-py3 /bin/bash`

### Install dependencies needed:
  `apt-get install imagemagick git`
  
  `pip install scikit-image pillow joblib`
  
### Download and extract your data. 
For our work, we used data from the [2018 ISIC Challenge](https://challenge2018.isic-archive.com/participate/) training set.
You need to download and extract:
  The skin lesion images for tasks 1-2. 
  The ground truth segmentation masks from task1.
  The ground truth attributes masks from task2.
  
### Generate semantic and instance maps.
run the script `prepare_files.sh` pointing to the files you've just downloaded. **Example**:

`sh prepare_files.sh -a ISIC2018_Task2_Training_GroundTruth_v3/ -s ISIC2018_Task1_Training_GroundTruth/ -i ISIC2018_Task1-2_Training_Input/`

When the script finishes running (it may take a good while), you should have a folder called pix2pixHD 
(which will be cloned from the [original authors](https://github.com/NVIDIA/pix2pixHD)).
Also, you should see a `pix2pixHD/datasets/skin/` folder containing the data you need to train the model: semantic and instance maps.
The semantic maps are inside the `train_label` folder, and the instance maps are inside the `train_inst` folder. The data is already divided 
in train and test, with 250 out of the total 2594 images for test.

# Running the GAN

### Install dependencies
`pip3 install torch torchvision dominate tqdm scikit-learn`

### Run training
`python3 train.py --name label2skin --dataroot datasets/skin/ --label_nc 8 --gpu_id 0 --batchSize 2 --tf_log --continue_train`

*Look into the `options` folder for more details.*

### Run test
`python3 test.py --name label2skin --dataroot datasets/skin/ --label_nc --gpu_id 0`
