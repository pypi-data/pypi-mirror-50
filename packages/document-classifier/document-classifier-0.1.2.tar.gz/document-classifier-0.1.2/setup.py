# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['document_classifier']

package_data = \
{'': ['*']}

install_requires = \
['keras>=2.2,<3.0',
 'numpy>=1.17,<2.0',
 'pillow>=6.1,<7.0',
 'tensorflow-gpu>=1.14,<2.0']

setup_kwargs = {
    'name': 'document-classifier',
    'version': '0.1.2',
    'description': 'A simple CNN for n-class classification of document images.',
    'long_description': '# basic-document-classifier\nA simple CNN for n-class classification of document images.\n\nIt doesn\'t take colour into account (it transforms to grayscale).\nFor small numbers of classes (2 to 4) this model can achieve > 90% accuracy with as little as 10 to 30 training images per class.\nTraining data can be provided in [any image format supported by *PIL*](https://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html).\n\n## Installation\n\n```pip install document-classifier```\nor\n```poetry add document-classifier```\n\n## Usage\n\n```python\nfrom document_classifier import CNN\n\n# Create a classification model for 3 document classes.\nclassifier = CNN(class_number=3)\n\n# Train the model based on images stored on the file system.\ntraining_metrics = classifier.train(\n    batch_size=8,\n    epochs=40,\n    train_data_path="./train_data",\n    test_data_path="./test_data"\n)\n# "./train_data" and "./test_data" have to contain a subfolder for\n# each document class, e.g. "./train_data/letter" or "./train_data/report".\n\n# View training metrics like the validation accuracy on the test data.\nprint(training_metrics.history["val_acc"])\n\n# Save the trained model to the file system.\nclassifier.save(model_path="./my_model")\n\n# Load the model from the file system.\nclassifier = CNN.load(model_path="./my_model")\n\n# Predict the class of some document image stored in the file system.\nprediction = classifier.predict(image="./my_image.jpg")\n# The image parameter also taks binary image data as a bytes object.\n```\n\nThe prediction result is a 2-tuple containing the document class label as a string and the confidence score as a float.\n\n## Changes\n\n### 0.1.2\n- Give every CNN instance its own isolated tensorflow graph and session\n\n### 0.1.1\n- Fix a bug that occured when using multiple model instances at the same time\n\n## TODO\n\nThe model architecture is fixed for now and geared towards smaller numbers of classes and training images.\nI\'m working on automatic scaling for the CNN.\n',
    'author': 'Silas Bischoff',
    'author_email': 'silas.bischoff@googlemail.com',
    'url': 'https://github.com/sbischoff-ai/basic-document-classifier',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
