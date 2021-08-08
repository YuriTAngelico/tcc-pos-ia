from django.core.files.base import File
from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from PIL import Image
from django.core.files.base import ContentFile

#custom imports
import cv2
import os
import imutils
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

#app imports
from .forms import *
from .models import *

class EmployeeClass(View):

    def get(self, request):

        data = {}
        data['employees'] = Employee.objects.all()
        data['employee_form'] = EmployeeForm()
        data['photo_form'] = PhotoForm()

        return render(request, 'employee.html', data)

    def post(self, request):

        print("[INFO] Adding employee.")

        form = EmployeeForm(request.POST, request.FILES)       

        try:
            form.save()
            messages.success(request, f"Employee {request.POST['first_name']} {request.POST['last_name']} succesfully created!", extra_tags="employee")
            
            ############### importando pacotes necessários ##################
            # load our serialized face detector from disk
            model = AIFaceDetector.objects.filter(caffee_model=True).last()
            proto = AIFaceDetector.objects.filter(caffee_model=False).last()
            print(model, proto)
            protoPath =  str(proto.face_detection_model)
            modelPath =  str(model.face_detection_model)
            detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

            # load our serialized face embedding model from disk
            embedder_path = AIEmbedder.objects.last()
            print("[INFO] loading face recognizer...")
            embedder = cv2.dnn.readNetFromTorch(str(embedder_path.embedder))

            # initialize our lists of extracted facial embeddings and
            # corresponding people names
            knownEmbeddings = []
            knownNames = []

            # initialize the total number of faces processed
            total = 0
            ############### importando pacotes necessários ##################

            ########### coleta o video da request e cria e exporta os frames para fotos ##########
            employee = Employee.objects.all().last()
            source  = cv2.VideoCapture(str(employee.video))
            success,image = source.read()
            count = 0
            
            while count < 30:

                try:
                    success,image = source.read()
                    path = os.path.dirname(os.path.realpath(__file__)) + f"\\temp\\{employee.first_name}{employee.last_name}-{count}.jpg"
                    cv2.imwrite(path, image)

                    with open(os.path.dirname(os.path.realpath(__file__)) + f"\\temp\\{employee.first_name}{employee.last_name}-{count}.jpg", 'rb') as f:
                        data = f.read()

                    new_face_photo = EmployeeFacePhoto()
                    new_face_photo.employee = Employee.objects.get(id=employee.id)
                    new_face_photo.photo.save(f"{employee.first_name}{employee.last_name}-{count}.jpg", ContentFile(data))
                    new_face_photo.save()

                    os.remove(os.path.dirname(os.path.realpath(__file__)) + f"\\temp\\{employee.first_name}{employee.last_name}-{count}.jpg")

                except:
                    pass

                count += 1
                ########## coleta o video da request e cria e exporta os frames para fotos ##########

                ############ extração de embedings e escrever o pickle #############
                employee_photo = EmployeeFacePhoto.objects.all().last()
                name = employee_photo.employee.first_name + " " + employee_photo.employee.last_name

                # load the image, resize it to have a width of 600 pixels (while
                # maintaining the aspect ratio), and then grab the image
                # dimensions
                image = cv2.imread(str(employee_photo.photo))
                image = imutils.resize(image, width=600)
                (h, w) = image.shape[:2]

                # construct a blob from the image
                imageBlob = cv2.dnn.blobFromImage(
                    cv2.resize(image, (300, 300)), 1.0, (300, 300),
                    (104.0, 177.0, 123.0), swapRB=False, crop=False)

                # apply OpenCV's deep learning-based face detector to localize
                # faces in the input image
                detector.setInput(imageBlob)
                detections = detector.forward()

                # ensure at least one face was found
                if len(detections) > 0:

                    # we're making the assumption that each image has only ONE
                    # face, so find the bounding box with the largest probability
                    i = np.argmax(detections[0, 0, :, 2])
                    confidence = detections[0, 0, i, 2]

                    # ensure that the detection with the largest probability also
                    # means our minimum probability test (thus helping filter out
                    # weak detections)
                    if confidence > 0.6:
                            
                        # compute the (x, y)-coordinates of the bounding box for
                        # the face
                        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                        (startX, startY, endX, endY) = box.astype("int")

                        # extract the face ROI and grab the ROI dimensions
                        face = image[startY:endY, startX:endX]
                        (fH, fW) = face.shape[:2]

                        # ensure the face width and height are sufficiently large
                        if fW < 20 or fH < 20:
                            continue

                        # construct a blob for the face ROI, then pass the blob
                        # through our face embedding model to obtain the 128-d
                        # quantification of the face
                        faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
                            (96, 96), (0, 0, 0), swapRB=True, crop=False)
                        embedder.setInput(faceBlob)
                        vec = embedder.forward()

                        # add the name of the person + corresponding face
                        # embedding to their respective lists
                        knownNames.append(name)
                        knownEmbeddings.append(vec.flatten())
                        total += 1

            # dump the facial embeddings + names to disk
            print("[INFO] serializing {} encodings...".format(total))
            data = {"embeddings": knownEmbeddings, "names": knownNames}
            f = open(os.path.dirname(os.path.realpath(__file__)) + '\\output\\embeddings.pickle', "wb")
            f.write(pickle.dumps(data))
            f.close()
            ############ extração de embedings e escrever o pickle #############

            ################### treinamento do modelo ####################
            # load the face embeddings
            print("[INFO] loading face embeddings...")
            data = pickle.loads(open(os.path.dirname(os.path.realpath(__file__)) + '\\output\\embeddings.pickle', "rb").read())

            # encode the labels
            print("[INFO] encoding labels...")
            le = LabelEncoder()
            labels = le.fit_transform(data["names"])

            # train the model used to accept the 128-d embeddings of the face and
            # then produce the actual face recognition
            print("[INFO] training model...")
            recognizer = SVC(C=1.0, kernel="linear", probability=True)
            recognizer.fit(data["embeddings"], labels)

            # write the actual face recognition model to disk
            f = open(os.path.dirname(os.path.realpath(__file__)) + '\\output\\recognizer.pickle', "wb")
            f.write(pickle.dumps(recognizer))
            f.close()
            # write the label encoder to disk
            f = open(os.path.dirname(os.path.realpath(__file__)) + '\\output\\le.pickle', "wb")
            f.write(pickle.dumps(le))
            f.close()
            ################### treinamento do modelo ####################    
            
            return redirect('employee')

        except Exception as e:
            messages.error(request, f"Error! --> {e}", extra_tags="employee")
            form = EmployeeForm()
            return redirect('employee')

    def delete(request, id):

        try:
            employee_photos = EmployeeFacePhoto.objects.filter(employee__id=id)
            for photo in employee_photos:
                os.remove(str(photo.photo))
        
        except:
            pass

        employee = Employee.objects.get(id=id)
        os.remove(str(employee.video))
        employee.delete()

        return redirect('employee')



class Photo(View):

    def post(self, request):

        print("[INFO] Adding employee photo.")

        print(request.POST)
        print(request.FILES)

        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, f"Photo succesfully added!", extra_tags="employee")
            return redirect('employee')

        else:
            messages.error(request, f"Error on adding, invalid form!", extra_tags="employee")
            return redirect('employee')

class Test(View):

    def get(self, request):
        pass