The original work of this project is always belong to the original creator (https://github.com/TropComplique/mtcnn-pytorch). I just make this available on pypi for easy installation. To install this project just type `pip install torch-mtcnn`

# MTCNN

`pytorch` implementation of **inference stage** of face detection algorithm described in  
[Joint Face Detection and Alignment using Multi-task Cascaded Convolutional Networks](https://arxiv.org/abs/1604.02878).

## Example
![example of a face detection](https://github.com/TropComplique/mtcnn-pytorch/blob/master/images/example.png)

## How to use it
Install the package with pip: `pip install torch-mtcnn`
```python
from torch_mtcnn import detect_faces
from PIL import Image

image = Image.open('image.jpg')
bounding_boxes, landmarks = detect_faces(image)
```
For a few more examples available on the original repository (link above).

## Requirements
* pytorch 0.2
* Pillow, numpy

## Credit
This implementation is heavily inspired by:
* [pangyupo/mxnet_mtcnn_face_detection](https://github.com/pangyupo/mxnet_mtcnn_face_detection)  
