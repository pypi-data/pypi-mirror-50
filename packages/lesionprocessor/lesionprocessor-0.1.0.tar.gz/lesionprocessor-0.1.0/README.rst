################
Lesion Processor
################

Lesion Processor crops, labels, and/or isolates lesions in a given image
or a set of images.

.. image:: https://raw.githubusercontent.com/marsbound/lesion-processor-static/master/docs/lp_overview.png
    :width: 100%
    :align: center
    :alt: lp_overview

************
Installation
************

.. code:: sh

    pip install lesionprocessor

*****
Usage
*****

.. code-block:: python

    import lesionprocessor as lp

    img_path = 'data/raw/lesion1.jpg'
    crop_dir = 'data/cropped'
    label_dir = 'data/labeled'
    isolate_dir = 'data/isolated'
    unprocessed_dir = 'data/unprocessed' # optional, will default to 'unprocessed' directory

    # Crop
    lp.crop(img_path, crop_dir, unprocessed_dir) # option 1
    lp.process(img_path, unprocessed_dir, crop_dir=crop_dir) # option 2

    # Label
    lp.label(img_path, label_dir, unprocessed_dir) # option 1
    lp.process(img_path, unprocessed_dir, label_dir=label_dir) # option 2

    # Isolate
    lp.isolate(img_path, isolate_dir, unprocessed_dir) # option 1
    lp.process(img_path, unprocessed_dir, isolate_dir=isolate_dir) # option 2

    # Crop + label + isolate (partiton into given out directories)
    lp.process(img_path, unprocessed_dir, crop_dir=crop_dir, label_dir=label_dir, isolate_dir=isolate_dir)

************
How It Works
************
.. image:: https://raw.githubusercontent.com/marsbound/lesion-processor-static/master/docs/lp_detail.png
    :width: 100%
    :align: center
    :alt: lp_overview

**************
Sample Results
**************
Using the crop technique for standardization:

.. image:: https://raw.githubusercontent.com/marsbound/lesion-processor-static/master/docs/results.png
    :width: 100%
    :align: center
    :alt: lp_overview

*******************
Additional Features
*******************

* Concurrently process multiple images
* Adjustable crop padding size
* Adjustable label color
* Adjustable label line thickness
* Adjustable number of contours to target
* Adjustable size of kernels for morphological transformations
* In Progress
    * Additional thresholding methods
    * Adjustable padding for isolation process

*******
License
*******

`Apache License 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`__
