# gan-skin-lesion
### Code to reproduce the results for the [paper](https://arxiv.org/abs/1902.03253) "Skin Lesion Synthesis with Generative Adversarial Networks" in ISIC Skin Image Analysis Workshop and Challenge @ MICCAI 2018.
In this repository you will find the code to generate the "Instance" and "Semantic" images. The network used is pix2pixHD (Wang et al.), which is referenced below. You can find our PGAN modification in the link [here](https://github.com/alceubissoto/cond-pgan) and the classification network used for our tests [here](https://github.com/learningtitans/isic2018-part3).

### Example Synthetic Images
<img src="/../images_examples/image_examples/semantic_ISIC_0000031_synthesized_image.jpg?raw=true" width="425"/> <img src="/../images_examples/image_examples/semantic_ISIC_0015995_synthesized_image.jpg?raw=true" width="425"/>

<img src="/../images_examples/image_examples/semantic_ISIC_0000097_synthesized_image.jpg?raw=true" width="425"/> <img src="/../images_examples/image_examples/semantic_ISIC_0015139_synthesized_image.jpg?raw=true" width="425"/>


# Preparing the data and environment
### Configuring the container.
We used nvidia-docker for all experiments. Run the following command to configure a container:

`nvidia-docker run -ti --userns=host --shm-size 8G  -v /home/gan-skin-lesion/:/gan-skin-lesion/ --name ganskinlesion -p 8008:8008 tensorflow/tensorflow:nightly-devel-gpu-py3 /bin/bash`

### Inside the container, install dependencies:
  `apt-get install imagemagick git`
  
  `pip install scikit-image pillow joblib`
  
### Download and extract your data. 
You need to download the [2018 ISIC Challenge](https://challenge2018.isic-archive.com/participate/) training set. Download images and ground truth for tasks 1 and 2.
  
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
`pip3 install -r requirements.txt`

### Run training
`python3 train.py --name label2skin --dataroot datasets/skin/ --label_nc 8 --gpu_id 0 --batchSize 2 --tf_log --continue_train`

*Check the `pix2pixHD/options` folder for more details.*

### Run test
`python3 test.py --name label2skin --dataroot datasets/skin/ --label_nc --gpu_id 0`

## Citation
If you find this useful for your research, please use the following.

```
  @inproceedings{bissoto2018skin,
	title={Skin Lesion Synthesis with Generative Adversarial Networks},
	author={Bissoto, Alceu and Perez, F\'abio and Valle, Eduardo and Avila, Sandra},
	booktitle={OR 2.0 Context-Aware Operating Theaters, Computer Assisted Robotic Endoscopy, Clinical Image-Based Procedures, and Skin Image Analysis},
        pages={294--302},
        year={2018},
        publisher={Springer}
}

```
