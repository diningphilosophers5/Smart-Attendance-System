# Smart Attendance System Using face Recognition

The objective of this project is to process live video-stream of students entering their classroom and generate the list of students attending the class.
The system is coded in Python 2.7 using OpenCv 3.1.0-dev, Tkinter and Numpy libraries.
The file in the directory are:
* attendencesystem.py: This is the main  script of the project.
                    It implements the GUI of the project and calls functions from the modules package developed.

* haarcascade_frontalface_default.xml: This file is taken from the OpenCV library and contains trained configurations of Voila-Jones Algorithm for detecting faces.

* Modules: This directory contains files which have helper functions for better structuring of the code.
    * predict.py: This contains the functions :
                identify_images(path): To recognise faces from an image.
                predict_video(path): To recognise faces from a video.
    * training.py: This contains the functions:
                train_models(path): To train the prediction models with the training set images.
                read_images(path): To fetch the face feature matrix from the subdirectories within a directory.

## Getting Started
### Prerequisites

The system needs Python 2.7 installed along with OpenCV libraries.
The face module of OpenCv is used for implementing Fisherfaces and Local Binary Pattern Histogram. The library is also used to implement Viola-Jones Face detection technique.

### Installing

The steps to install OpenCV with the extra module can be found [here](https://github.com/opencv/opencv_contrib).
The project also requires [Tkinter](https://docs.python.org/2/library/tkinter.html) and [Numpy](http://www.numpy.org/).


## Built With

* [OpenCV](http://docs.opencv.org/3.1.0/) - Implementation of Algorithms
* [Tkinter](https://docs.python.org/2/library/tkinter.html) - GUI Implementation
* [Numpy](http://www.numpy.org/) - Used to manage computaions.

## Authors

* **Ishan Roy**
* **Shivangi Singh**
* **Harshit Rastogi**
* **Kartikeya Mishra**
* **Akash Unni**


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
The following blogs helped in coding up this project:
* http://bytefish.de/blog/videofacerec/
* http://hanzratech.in/2015/02/03/face-recognition-using-opencv.html

Refer the following papers for understanding the algorithms used:
* [Rapid Object Detection Using Boosted Cascade of Simple Features](https://www.cs.cmu.edu/~efros/courses/LBMV07/Papers/viola-cvpr-01.pdf)
* [Eigenfaces vs Fisherfaces: Recognition using Class Specific Linear Projection](http://www.face-rec.org/algorithms/LDA/belhumeur96eigenfaces.pdf)
* [Local Binary Patterns and Its Application to Facial Image Analysis: A Survey](http://liris.cnrs.fr/Documents/Liris-5004.pdf).
