import tensorflow_datasets as tfds
import tensorflow as tf
import os
from PIL import Image

# Create main dataset directory
dataset_dir = './dataset'
os.makedirs(dataset_dir, exist_ok=True)

# Load the dataset
(ds_train, ds_test), ds_info = tfds.load(
    'cats_vs_dogs',
    split=['train[:80%]', 'train[80%:]'],
    shuffle_files=True,
    as_supervised=True,
    with_info=True,
)

# Save images to folders
def save_images(dataset, subset_name):
    subset_dir = os.path.join(dataset_dir, subset_name)
    os.makedirs(subset_dir, exist_ok=True)
    cat_dir = os.path.join(subset_dir, 'cats')
    dog_dir = os.path.join(subset_dir, 'dogs')
    os.makedirs(cat_dir, exist_ok=True)
    os.makedirs(dog_dir, exist_ok=True)

    for i, (image, label) in enumerate(tfds.as_numpy(dataset)):
        class_name = 'cats' if label == 0 else 'dogs'
        image_path = os.path.join(os.path.join(subset_dir, class_name), f'{class_name}_{i}.jpg')
        Image.fromarray(image).save(image_path)

save_images(ds_train, 'train')
save_images(ds_test, 'validation')

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
predictions = Dense(2, activation='softmax')(x)  # Only 2 classes: cats and dogs
model = Model(inputs=base_model.input, outputs=predictions)

# Freeze base model layers
for layer in base_model.layers:
    layer.trainable = False

# Compile the model
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])
datagen = ImageDataGenerator(rescale=1./255)

train_gen = datagen.flow_from_directory(
    './dataset/train',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

val_gen = datagen.flow_from_directory(
    './dataset/validation',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)
model.fit(train_gen, validation_data=val_gen, epochs=5)
model.save("cats_vs_dogs_model.h5")
