
import cv2, os
import numpy as np
from PIL import Image

def identify_images(path):
    """Loads the already present models of LBP and FisherFaces Recognisers
        Returns the prediction on all the images present in the folder given by path
    Args:
        path: Path to a folder containing images to be tested on.

    Returns:
        A dictionary {image_path : predicted_person}

            image_path: The path of the image for which the prediction is.
            predicted_person: The corresponding labels (the unique number of the subject, person) or name of the person in the image.
    """
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    recognizer1 = cv2.face.createLBPHFaceRecognizer()
    recognizer2 = cv2.face.createFisherFaceRecognizer()

    recognizer1.load("LBPFPatternRecogniser")
    recognizer2.load("FisherfacesRecogniser")

    result = {}
    subjects = np.load('subjectlabels.npy').item()

    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    for image_path in image_paths:
        predict_image_pil = Image.open(image_path).convert('L')
        predict_image = np.array(predict_image_pil, 'uint8')
        faces = faceCascade.detectMultiScale(predict_image)
        for (x, y, w, h) in faces:
            if w < 100 or h < 100:
                continue
            img = predict_image[y: y + h, x: x + w]
            resize_img = cv2.resize(img, (150, 150))
            nbr_predicted1, conf1 = recognizer1.predict(resize_img)
            nbr_predicted2, conf2 = recognizer2.predict(resize_img)
            final_conf = (.8*conf1 + .2*((conf2)/30))
            final_predict = -1
            if nbr_predicted1 == nbr_predicted2:
                if final_conf < 70:
                    final_predict = nbr_predicted1
            else:
                if conf1 < 45:
                    final_predict = nbr_predicted1
                elif conf2 < 500:
                    final_predict = nbr_predicted2
            if final_predict != -1:
                result[image_path] = subjects[final_predict]
                cv2.imshow("Recognizing Face", resize_img)
                cv2.waitKey(10)
    cv2.destroyAllWindows()
    return result

def predict_video(path):
    """Loads the already present models of LBP and FisherFaces Recognisers
        Returns the prediction on all the images present in the folder given by path
    Args:
        path: Path to a folder containing video to be tested on.

    Returns:
        A set containing the names of the predicted persons.

    """
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    recognizer1 = cv2.face.createLBPHFaceRecognizer()
    recognizer2 = cv2.face.createFisherFaceRecognizer()

    recognizer1.load("LBPFPatternRecogniser")
    recognizer2.load("FisherfacesRecogniser")

    result = set()
    subjects = np.load('subjectlabels.npy').item()
    vidcap = cv2.VideoCapture(path)
    time = 0
    success = True
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC, time)
        time += 500
        success, image = vidcap.read()
        if success:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray)
            for (x, y, w, h) in faces:
                if w < 100 or h < 100:
                    continue
                img = gray[y: y + h, x: x + w]
                img_resize = cv2.resize(img,(150,150))
                nbr_predicted1, conf1 = recognizer1.predict(img_resize)
                nbr_predicted2, conf2 = recognizer2.predict(img_resize)
                final_conf = (.8*conf1 + .2*((conf2)/30))
                final_predict = -1
                if nbr_predicted1 == nbr_predicted2:
                    if final_conf < 70:
                        final_predict = nbr_predicted1
                else:
                    if conf1 < 45:
                        final_predict = nbr_predicted1
                    elif conf2 < 500:
                        final_predict = nbr_predicted2
                #print final_predict
                if final_predict != -1:
                    result.add(subjects[final_predict])
                    #cv2.imshow("Recognizing Face", gray[y: y + h, x: x + w])
                    cv2.imshow("Recognizing Face",img_resize)
                    cv2.waitKey(10)
    cv2.destroyAllWindows()
    return result
