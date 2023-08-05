# A I S T H E T I C S

# What?

This repository contains a modified version of the source code [hosted here](https://github.com/idealo/image-quality-assessment).

# Where is the training data?

We did not train the model ourselves, although we could very well do so if necessary using the following datasets.

## AVA dataset

The most interesting dataset I found for this work is called [AVA](https://www.researchgate.net/publication/261336804_AVA_A_large-scale_database_for_aesthetic_visual_analysis) (Aesthetic Visual Analysis). Consists on a dataset of 255530 images, and for each one we have a histogram of scores from 1 to 10 that around 300 amateur photographers gave them (based on aesthetical value).

It is a rather big dataset (~33GB) so you won't find it in this repository.

## ImageNet

This is a huge open dataset of labeled images. There are 1000 different categories. For years, researchers have used this dataset as a ground truth and challenge for their models. Every year there is a contest and every year the winner team's model is a breakthrough in the field of image classification and computer vision.

Most image quality assessment models are based on existing CNN architectures for image classification (the ones that are used are of course the winners of the ImageNet challenge). This is because these networks have been trained to detect many features on images of 1000 different categories, which makes them good at most stuff image related. These models build some layers of neurons on top of the baseline CNN to transform their outputs, and retrain the weights on some of the layers using AVA.

# Model

It is called Neural Image Assessment (NIMA). In their paper, the authors implement the same idea over different baseline networks (VGG16, Inception-v2 and MobileNet).

Here, we use MobileNet as the base model, because it seems to be the best performing one. Details aside, MobileNet changes the classic convolution layers by so called _depthwise separable convolutions_ (or more recently _projection layers_). These are computationally cheaper, making this network suitable for running even in portable devices (hence its name).

On top of MobileNet (replacing its output layer), NIMA is a 10 neuron fully connected layer followed by a softmax activation. The loss function used is squared EMD (earth mover's distance), and the data for retraining is the AVA dataset with histogram inputs. Besides this they do more stuff but we don't care about that right now.

## Shortcomings

Even though this model is probably the best performing in the field of aesthetic assessment, a perfect model for such a subjective topic has not been achieved. Check the [hackdays readme](https://gitlab.com/tutti-ch/hackdays-2019/aisthetics/blob/master/README.md#shortcomings) for more information.