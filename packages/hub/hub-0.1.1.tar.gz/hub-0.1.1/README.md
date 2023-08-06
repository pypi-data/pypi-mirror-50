# Hub Array - Scalable Cloud Numpy Array

Hub Arrays are very large arrays stored on the cloud storage (such as S3) and accessed over internet as if local numpy arrays.
```python
> import hub
> imagenet = hub.load(name='imagenet')
> imagenet.shape
(1034908, 469, 387, 3)
```

## Usage
1. Install 
```sh
pip3 install hub
```

Then provide AWS credentials and name of your project.
```sh
hub configure
```
It will create a bucket to store the data 

2. Create an array
```python
mnist = hub.array((50000, 28, 28, 1), name="username/mnist:v1", dtype='float32')
mnist[0, :] = np.ones((28,28,1))
```

3. Load an array from another machine
```python
mnist = hub.load(name='username/mnist:v1')
print(mnist[0,0,0,0])
```

## Motivation
Most of the time Data Scientists/ML researchers work on data management and preprocessing instead of doing modeling. Deep Learning often requires to work with large datasets. Those datasets can grow up to terabyte or even petabyte size. It is hard to manage data, version control and track. It is time consuming to download the data and link with the training or inference code. There is no easy way to access a chunk of it and possibly visualize. Wouldn’t it be more convenient to have large datasets represented as single arrays and have access from any machine at scale?

Read more in our blogpost [Scalable Cloud Numpy Array: Read and Write from Anywhere](https://medium.com/@SnarkAI/scalable-cloud-numpy-array-read-and-write-from-anywhere-fd5486ad1c96)

## Features
* **Data Management**: Storing large datasets with version control
* **Collaboration**: Multiple data scientists working on the same data in sync
* **Distribute**: Accessing from multiple machines at the same time
* **Machine Learning**: Native integration with Numpy, Dask, PyTorch or TensorFlow.
* **Scale**: Create as big arrays as you want
* **Visualization**: Visualize the data without trouble

## Use Cases
* **Areal images**: Satellite and drone imagery
* **Medical Images**: Volumetric images such as MRI or Xray
* **Self-Driving Cars**: Radar, 3D LIDAR, Point Cloud, Semantic Segmentation, Video Objects
* **Retail**: Self-checkout datasets
* **Media**: Images, Video, Audio storage

### Acknolowdgement
Acknowledgment: This technology was inspired from our experience at Princeton University at SeungLab and would like to thank William Silversmith @SeungLab and his awesome project [cloud-volume](https://github.com/seung-lab/cloud-volume).
