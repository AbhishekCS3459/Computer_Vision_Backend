import tensorflow_datasets as tfds
import tensorflow as tf
import os
from PIL import Image

dataset_dir = './dataset'
os.makedirs(dataset_dir, exist_ok=True)

(ds_train, ds_test), ds_info = tfds.load(
    'cats_vs_dogs',
    split=['train[:80%]', 'train[80%:]'],
    shuffle_files=True,
    as_supervised=True,
    with_info=True,
)

def save_images(dataset, subset_name):
    subset_dir = os.path.join(dataset_dir, subset_name)
    os.makedirs(subset_dir, exist_ok=True)
    cat_dir = os.path.join(subset_dir, 'cats')
    dog_dir = os.path.join(subset_dir, 'dogs')
    os.makedirs(cat_dir, exist_ok=True)
    os.makedirs(dog_dir, exist_ok=True)

    for i, (image, label) in enumerate(tfds.as_numpy(dataset)):
        class_name = 'cats' if label == 0 else 'dogs'
        path = os.path.join(subset_dir, class_name, f'{class_name}_{i}.jpg')
        Image.fromarray(image).save(path)

save_images(ds_train, 'train')
save_images(ds_test, 'validation')
