
import sys
import cv2, os
import numpy as np
from PIL import Image

def read_images(path):
    """Reads the images in a given folder, resizes images on the fly if size is given.
    Args:
        path: Path to a folder with subfolders representing the subjects (persons).
        model: An integer indicating the model for which the data is to be used. 1 denotes LBP Recogniser.
                2 indicates FisherFaces recogniser.

    Returns:
        A list [X, y, folder_names]

            X: The images, which is a Python list of numpy arrays.
            y: The corresponding labels (the unique number of the subject, person) in a Python list.
            folder_names: The names of the folder, so you can display it in a prediction.
    """
    c = 0
    X = []
    Y = []
    folder_names = []
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    for dirname, dirnames, filenames in os.walk(path):
        for subdirname in dirnames:
            folder_names.append(subdirname)
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                try:
                    image_path = os.path.join(subject_path, filename)
                    # resize to given size (if given)
                    image_pil = Image.open(image_path).convert('L')

                    # Convert the image format into numpy array
                    image = np.array(image_pil, 'uint8')
                    faces = faceCascade.detectMultiScale(image)
                    for (x, y, w, h) in faces:
                        if w < 100 or h < 100:
                            continue
                        img = image[y: y+h, x: x+h]
                        #if model==1:
                        #    img1 = img
                        #else:
                        img1 = cv2.resize(img, (150, 150))
                        X.append(img1)
                        Y.append(c)
                        cv2.imshow("Adding faces to training set...", img1)
                        cv2.waitKey(10)
                except IOError, (errno, strerror):
                    print "I/O error({0}): {1}".format(errno, strerror)
                except:
                    print "Unexpected error:", sys.exc_info()[0]
                    raise
            c = c+1
    return [X,Y,folder_names]

def train_models(path):
    """Creates LBF and Fisherface Recognisers using the OpenCV Libraries.
        Trains them using the dataset present in the given folder.
        Stores the recognisers for future prodictions in present directory.
    Args:
        path: Path to a folder with subfolders representing the subjects (persons).
    """
    recognizer1 = cv2.face.createLBPHFaceRecognizer()
    recognizer2 = cv2.face.createFisherFaceRecognizer()

    [images, labels, subject_names] = read_images(path)
    #[images2, labels2, subject_names2] = read_images(path)

    list_of_labels = list(xrange(max(labels)+1))
    subject_dictionary = dict(zip(list_of_labels, subject_names))

    np.save('subjectlabels.npy', subject_dictionary)

    recognizer1.train(images, np.array(labels))
    recognizer2.train(images, np.array(labels))

    recognizer1.save("LBPFPatternRecogniser")
    recognizer2.save("FisherfacesRecogniser")

    cv2.destroyAllWindows()
