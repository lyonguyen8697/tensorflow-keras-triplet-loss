from base.base_data_loader import BaseDataLoader
import os
import math
import json
import numpy as np
from utils.image_preprocessing import load_image, resize_image_with_padding


class DataLoader(BaseDataLoader):
    def __init__(self, config):
        super(DataLoader, self).__init__(config)
        self.config = config

        data = json.load(open(config.annotations_file, 'r'))
        self.annotations = data['annotations']
        self.categories = data['categories']
        self.cat2ann = {cat['id']: [] for cat in self.categories}
        for ann in self.annotations:
            cat_id = ann['category_id']
            self.cat2ann[cat_id].append(ann)

        self.category_per_batch = math.ceil(config.batch_size / config.example_per_category)

        self.train_category_ids = [cat['id'] for cat in self.categories if cat['split'] == 'train']
        self.val_category_ids = [cat['id'] for cat in self.categories if cat['split'] == 'val']

    def get_train_data(self):
        pass

    def get_test_data(self):
        pass

    def get_train_steps(self):
        num_of_example = sum(len(anns) for anns in [self.cat2ann[cat_id] for cat_id in self.train_category_ids])
        num_of_steps = math.ceil(num_of_example / self.config.batch_size)

        return num_of_steps

    def get_val_steps(self):
        num_of_example = sum(len(anns) for anns in [self.cat2ann[cat_id] for cat_id in self.val_category_ids])
        num_of_steps = math.ceil(num_of_example / self.config.batch_size)

        return num_of_steps

    def get_train_generator(self):
        category_ids = np.pad(self.train_category_ids, [0, math.ceil(len(self.train_category_ids) / self.category_per_batch) * self.category_per_batch - len(self.train_category_ids)], mode='wrap')

        while True:
            for i in range(0, len(category_ids), self.category_per_batch):
                annotations = []
                start, end = i, i + self.category_per_batch
                for cat_id in category_ids[start:end]:
                    annotations.extend(np.random.choice(self.cat2ann[cat_id], math.ceil(self.config.batch_size / self.category_per_batch), replace=False))

                images = []
                labels = []
                for ann in annotations[:self.config.batch_size]:
                    image = load_image(os.path.join(self.config.image_dir, ann['image_file']))
                    image = resize_image_with_padding(image, self.config.image_size)
                    label = ann['category_id']
                    images.append(image)
                    labels.append(label)

                yield np.array(images), np.array(labels)

            np.random.shuffle(category_ids)

    def get_val_generator(self):
        category_ids = np.pad(self.val_category_ids, [0, math.ceil(len(self.val_category_ids) / self.category_per_batch) * self.category_per_batch - len(self.val_category_ids)], mode='wrap')

        while True:
            for i in range(0, len(category_ids), self.category_per_batch):
                annotations = []
                start, end = i, i + self.category_per_batch
                for cat_id in category_ids[start:end]:
                    annotations.extend(np.random.choice(self.cat2ann[cat_id], math.ceil(self.config.batch_size / self.category_per_batch), replace=False))

                images = []
                labels = []
                for ann in annotations[:self.config.batch_size]:
                    image = load_image(os.path.join(self.config.image_dir, ann['image_file']))
                    image = resize_image_with_padding(image, self.config.image_size)
                    label = ann['category_id']
                    images.append(image)
                    labels.append(label)

                yield np.array(images), np.array(labels)


