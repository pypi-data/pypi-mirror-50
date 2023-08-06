# tutti-aisthetics-tf Python package

## What?

This repository contains a modified version of the source code [hosted here](https://github.com/idealo/image-quality-assessment).

It is actually adapted from the package `tutti-aisthetics`. The weights file with _.hdf5_ format included in that package is transformed here to ProtocolBuffers format. This allows us to import it directly to Tensorflow and not depend on Keras. This makes the package smaller and more suited for deploying the model for pure inference.

This package contains a single class: `Nima`, that reads a model file (for NIMA) in `.pb` format, and can then score images provided either a local path or an S3 path (that starts with _s3://_).

## Model

It is called Neural Image Assessment (NIMA). In their paper, the authors implement the same idea over different baseline networks (VGG16, Inception-v2 and MobileNet).

Here, we use MobileNet as the base model, because it seems to be the best performing one. Details aside, MobileNet changes the classic convolution layers by so called _depthwise separable convolutions_ (or more recently _projection layers_). These are computationally cheaper, making this network suitable for running even in portable devices (hence its name).

On top of MobileNet (replacing its output layer), NIMA is a 10 neuron fully connected layer followed by a softmax activation. The loss function used is squared EMD (earth mover's distance), and the data for retraining is the AVA dataset with histogram inputs. Besides this they do more stuff but we don't care about that right now.

### Shortcomings

Even though this model is probably the best performing in the field of aesthetic assessment, a perfect model for such a subjective topic has not been achieved. Check the [hackdays readme](https://gitlab.com/tutti-ch/hackdays-2019/aisthetics/blob/master/README.md#shortcomings) for more information.