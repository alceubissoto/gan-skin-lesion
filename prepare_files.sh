#!/bin/bash

while getopts a:s:i: option
do
	case "${option}"
		in
		a) ATTRI_DIR=${OPTARG};;
		s) SEG_DIR=${OPTARG};;
		i) IMAGE_DIR=${OPTARG};;
	esac
done

echo "Attribute directory: $ATTRI_DIR"
echo "Segmentation directory: $SEG_DIR"
echo "Image directory $IMAGE_DIR"

mkdir attribute_resized
cd attribute_resized
find ../"$ATTRI_DIR" -name '*.png' -exec sh -c 'echo "{}"; convert "{}" -resize 1024x512\> -size 1024x512 xc:red +swap -gravity center -composite `basename "{}" .png`.png' \;
cd ..

mkdir segmentation_resized
cd segmentation_resized
find ../"$SEG_DIR" -name '*.png' -exec sh -c 'echo "{}"; convert "{}" -resize 1024x512\> -size 1024x512 xc:red +swap -gravity center -composite `basename "{}" .png`.png' \;
cd ..

mkdir image_resized
cd image_resized
find ../"$IMAGE_DIR" -name '*.jpg' -exec sh -c 'echo "{}"; convert "{}" -resize 1024x512\> -size 1024x512 xc:black +swap -gravity center -composite `basename "{}" .jpg`.png' \;
cd ..

python assemble_data.py
rm -r attribute_resized
rm -r segmentation_resized


mkdir images_512p
cd images_512p
find ../"$IMAGE_DIR" -name '*jpg' -exec sh -c 'echo "{}"; convert "{}" -resize 1024x512\> `basename "{}" .jpg`.png' \;
cd ..

mkdir attribute_512p
cd attribute_512p
find ../"$ATTRI_DIR" -name '*.png' -exec sh -c 'echo "{}"; convert "{}" -resize 1024x512 `basename "{}" .png`.png' \;
cd ..

mkdir seg_512p
cd seg_512p
find ../"$SEG_DIR" -name '*.png' -exec sh -c 'echo "{}"; convert "{}" -resize 1024x512 `basename "{}" .png`.png' \;
cd ..

python instance_map.py
mkdir instance_map
cd instance_map
find ../instance_map_no_border -name '*.png' -exec sh -c 'echo "{}"; convert "{}" -resize 1024x512\> -size 1024x512 xc:black +swap -gravity center -composite `basename "{}" .png`.png' \;
cd ..

rm -r instance_map_no_border
rm -r seg_512p
rm -r attribute_512p
rm -r images_512p

git clone https://github.com/NVIDIA/pix2pixHD.git
cd pix2pixHD
git reset --hard 1c46896fc8b131d36811bbaae357ee6e150d9ea1

mkdir -p datasets/skin
mv ../instance_map datasets/skin/
mv ../semantic_map datasets/skin/

mkdir -p datasets/skin/test_label
mkdir -p datasets/skin/test_inst
mkdir -p datasets/skin/test_img
mv datasets/skin/instance_map datasets/skin/train_inst
mv datasets/skin/semantic_map datasets/skin/train_label
mv ../image_resized datasets/skin/
mv datasets/skin/image_resized datasets/skin/train_img

cd ..
python select_train_test.py
cd pix2pixHD
