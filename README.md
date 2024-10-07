# 3d_shape

We created a library of 3D-printed objects for visuo-haptic experiments (See [vh_objects](https://github.com/williamsnider/vh_objects)). It is designed to systematically cover a wide range of complex shapes by parameterizing feature dimensions (e.g., curvature, medial-axis structure, relative position and angles of bumps).

<img src="examples/shape_example.gif" width="800"> 


To understand how our library relates to the objects we see and touch in the real world, this repository implements deep learning models trained on real-world images and 3D data. These models are used to process our visuo-haptic shapes, with the goals of evaluating classification results and extracting latent features.


## Residual Neural Network (ResNet)

ResNet is a deep convolutional neural network architecture that introduced the concept of residual learning to address the problem of vanishing gradients in deep networks. We use the ResNet50 model, which consists of 49 convolutional layers and 1 fully connected layer. This model has been trained on the ImageNet dataset, containing over 14 million images across 1000 classes.

In our approach, we first render our 3D mesh data into 2D images, then use the pre-trained ResNet50 to obtain classification results of our visuo-haptic objects.


## Dynamic Graph CNN (DGCNN)

DGCNN is a neural network designed to process 3D point clouds by constructing and dynamically updating graphs. Its key innovation is the use of edge convolutions, which allow it to learn geometric relationships between points in 3D space. This model has been trained on the ModelNet40 dataset, which contains around 12,000 CAD models across 40 classes.

In our approach, we first convert 3D mesh models into 3D point cloud formats and then use the pre-trained DGCNN to obtain classification results for our visuo-haptic objects and extract shape features from a hidden layer.


## Reference
1. Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun. Deep Residual Learning for Image Recognition. (2015) https://arxiv.org/abs/1512.03385

2. Yue Wang, Yongbin Sun, Ziwei Liu, Sanjay E. Sarma, Michael M. Bronstein, Justin M. Solomon. Dynamic Graph CNN for Learning on Point Clouds. (2018) https://arxiv.org/abs/1801.07829\
GitHub:\
https://github.com/WangYueFt/dgcnn/tree/master
https://github.com/AnTao97/dgcnn.pytorch


