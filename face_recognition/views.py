from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

#custom imports
import cv2
import os
import imutils
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import json
from json import JSONEncoder
import numpy

#app imports
from .forms import *
from .models import *

class EmployeeClass(View):

    def get(self, request):

        data = {}
        data['employees'] = Employee.objects.all()
        data['employee_form'] = EmployeeForm()
        data['photo_form'] = PhotoForm()
        data['test_image_form'] = TestImageForm()

        return render(request, 'employee.html', data)


    def employees_registered(request):
        data = {}
        data['employees'] = Employee.objects.all()

        return render(request, 'employees_registered.html', data)


    def post(self, request):

        print("[INFO] Adding employee.")

        form = EmployeeForm(request.POST, request.FILES)

        # try:
        form.save()
        messages.success(request, f"Employee {request.POST['first_name']} {request.POST['last_name']} succesfully created!", extra_tags="employee")

        ############### importando pacotes necessários ##################
        # load our serialized face detector from disk
        model = AIFaceDetector.objects.filter(caffee_model=True).last()
        proto = AIFaceDetector.objects.filter(caffee_model=False).last()
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
        print("[INFO] loading employee video...")
        employee = Employee.objects.all().last()
        source  = cv2.VideoCapture(str(employee.video))
        success,image = source.read()
        count = 0

        print("[INFO] starting embeddings extraction...")

        while count < 200:

            try:
                #pega um frame do video e salva como imagem em uma pasta temporaria
                success,image = source.read()
                path = os.path.dirname(os.path.realpath(__file__)) + f"\\temp\\{employee.first_name}{employee.last_name}-{count}.jpg"
                cv2.imwrite(path, image)

                #abre a foto salva e usa os dados lidos para salvar dentro do model de FacePhoto
                with open(os.path.dirname(os.path.realpath(__file__)) + f"\\temp\\{employee.first_name}{employee.last_name}-{count}.jpg", 'rb') as f:
                    data = f.read()

                new_face_photo = EmployeeFacePhoto()
                new_face_photo.employee = Employee.objects.get(id=employee.id)
                new_face_photo.photo.save(f"{employee.first_name}{employee.last_name}-{count}.jpg", ContentFile(data))
                new_face_photo.save()

                os.remove(os.path.dirname(os.path.realpath(__file__)) + f"\\temp\\{employee.first_name}{employee.last_name}-{count}.jpg")

            except Exception as e:
                print(f"Houve um erro aqui --> {e}")

            count += 1
            ########## coleta o video da request e cria e exporta os frames para fotos ##########

            ############ extração de embedings e escrever o pickle #############
            employee_photo = EmployeeFacePhoto.objects.all().last()
            name = employee_photo.employee.first_name + " " + employee_photo.employee.last_name

            print(f"[INFO] Processing photo {count}")

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
        data = {"embeddings": json.dumps(knownEmbeddings, cls=NumpyArrayEncoder), "names": knownNames}

        #salvando em banco os embeddings para potseriormente escrever em um arquivo pickle
        new_employee_embedding = EmployeeEmbedding(
            employee=employee,
            embedding_data=data
        )
        new_employee_embedding.save()
        ############ extração de embedings e escrever o pickle #############

        #verifica se há mais do que um funcionario cadastrado
        if len(Employee.objects.all()) > 1:

            #coleta todos os embeddings de funcionarios
            employees_embeddings = EmployeeEmbedding.objects.all()

            #concatena todos os embeddings
            z = {}
            z['names'] = []
            z['embeddings'] = []
            for eb in employees_embeddings:
                z['names'] += eb.embedding_data['names']
                z['embeddings'] += json.loads(eb.embedding_data['embeddings'])


            #como o arquivo pickle não pode ter appending então teremos
            # que gravar em banco os embeddings como JSON e quando necessário
            #extrair e gerar um pickle
            f = open(os.path.dirname(os.path.realpath(__file__)) + '\\output\\embeddings.pickle', "wb")
            f.write(pickle.dumps(z))
            f.close()

            print("TRAINING MODEL....")

            ################### treinamento do modelo ####################
            # load the face embeddings
            print("[INFO] loading face embeddings...")
            file_pickle = open(os.path.dirname(os.path.realpath(__file__)) + '\\output\\embeddings.pickle', "rb").read()
            data = pickle.loads(file_pickle)
            # print(data)

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
            print("[INFO] Success...")
            ################### treinamento do modelo ####################

        return redirect('employee')

        # except Exception as e:
        #     messages.error(request, f"Error! --> {e}", extra_tags="employee")
        #     form = EmployeeForm()
        #     return redirect('employee')


    def delete(request, id):

        try:
            employee_photos = EmployeeFacePhoto.objects.filter(employee__id=id)
            for photo in employee_photos:
                os.remove(str(photo.photo))

        except:
            pass
        
        try:
            employee = Employee.objects.get(id=id)
            os.remove(str(employee.video))
            employee.delete()

        except Exception as e:
            messages.error(request, f"Employee already deleted! --> {e}", extra_tags="employees_registered")

        messages.success(request, f"Employee deleted!", extra_tags="employees_registered")

        return redirect('employees_registered')


# class Photo(View):

#     def post(self, request):

#         print("[INFO] Adding employee photo.")

#         print(request.POST)
#         print(request.FILES)

#         form = PhotoForm(request.POST, request.FILES)

#         if form.is_valid():
#             form.save()
#             messages.success(request, f"Photo succesfully added!", extra_tags="employee")
#             return redirect('employee')

#         else:
#             messages.error(request, f"Error on adding, invalid form!", extra_tags="employee")
#             return redirect('employee')

class Test(View):

    def get(self, request):
        data = {}
        data['test_image_form'] = TestImageForm()
        return render(request, 'test_recognition.html', data)


    def post(self, request):

        form = TestImageForm(request.POST, request.FILES)

        try:
            form.save()
        except:
            pass

        ############### importando pacotes necessários ##################
        # load our serialized face detector from disk
        model = AIFaceDetector.objects.filter(caffee_model=True).last()
        proto = AIFaceDetector.objects.filter(caffee_model=False).last()
        protoPath =  str(proto.face_detection_model)
        modelPath =  str(model.face_detection_model)
        detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

        # load our serialized face embedding model from disk
        embedder_path = AIEmbedder.objects.last()
        print("[INFO] loading face recognizer...")
        embedder = cv2.dnn.readNetFromTorch(str(embedder_path.embedder))

        recognizer = pickle.loads(open(os.path.dirname(os.path.realpath(__file__)) + '\\output\\recognizer.pickle', "rb").read())
        le = pickle.loads(open(os.path.dirname(os.path.realpath(__file__)) + '\\output\\le.pickle', "rb").read())

        if request.method == "POST":

            test_image = TestImage.objects.all().last()

            # load the image, resize it to have a width of 600 pixels (while
            # maintaining the aspect ratio), and then grab the image dimensions
            image = cv2.imread(str(test_image.test_image))
            # print(image)
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

            # loop over the detections
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]
                # filter out weak detections
                if confidence > 0.6:
                    # compute the (x, y)-coordinates of the bounding box for the
                    # face
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    # extract the face ROI
                    face = image[startY:endY, startX:endX]
                    (fH, fW) = face.shape[:2]
                    # ensure the face width and height are sufficiently large
                    if fW < 20 or fH < 20:
                        continue
                    # construct a blob for the face ROI, then pass the blob
                    # through our face embedding model to obtain the 128-d
                    # quantification of the face
                    faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
                        (0, 0, 0), swapRB=True, crop=False)
                    embedder.setInput(faceBlob)
                    vec = embedder.forward()
                    # perform classification to recognize the face
                    preds = recognizer.predict_proba(vec)[0]
                    j = np.argmax(preds)
                    proba = preds[j]
                    name = le.classes_[j]

                    # draw the bounding box of the face along with the associated
                    # probability
                    text = "{}: {:.2f}%".format(name, proba * 100)

                    print(text)

                    data = dict(
                        result=text,
                        show=True,
                        test_image_form = TestImageForm()
                    )

                    return render(request, 'test_recognition.html', data)


    @csrf_exempt
    def ajax_post(request):
        if request.method == "POST":
            print("Eu recebi um POST!!!")

            data_image = request.POST.get('image')
            data_image_parse = json.loads(data_image) # parse JSON.stringify and would be a dictionary
            data_image = list(data_image_parse.values()) # convert to list and would be length of 640 * 480 * 4
            image_from_post = np.array(data_image).reshape(480, 640, 4) # here is your image data and you can save it
            cv2.imwrite("teste.png", image_from_post)

            ########################################################################################################
            ########################################################################################################
            ########################################################################################################
            ########################################################################################################

            ############### importando pacotes necessários ##################
            # load our serialized face detector from disk
            model = AIFaceDetector.objects.filter(caffee_model=True).last()
            proto = AIFaceDetector.objects.filter(caffee_model=False).last()
            protoPath =  str(proto.face_detection_model)
            modelPath =  str(model.face_detection_model)
            detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

            # load our serialized face embedding model from disk
            embedder_path = AIEmbedder.objects.last()
            print("[INFO] loading face recognizer...")
            embedder = cv2.dnn.readNetFromTorch(str(embedder_path.embedder))

            recognizer = pickle.loads(open(os.path.dirname(os.path.realpath(__file__)) + '\\output\\recognizer.pickle', "rb").read())
            le = pickle.loads(open(os.path.dirname(os.path.realpath(__file__)) + '\\output\\le.pickle', "rb").read())


            # load the image, resize it to have a width of 600 pixels (while
            # maintaining the aspect ratio), and then grab the image dimensions
            image = cv2.imread("teste.png")
            print(f"Tipo de imagem lida do disco: {type(image)}, Shape: {image.shape}")
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

            # loop over the detections
            for i in range(0, detections.shape[2]):
                # extract the confidence (i.e., probability) associated with the
                # prediction
                confidence = detections[0, 0, i, 2]
                # filter out weak detections
                if confidence > 0.6:
                    # compute the (x, y)-coordinates of the bounding box for the
                    # face
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    # extract the face ROI
                    face = image[startY:endY, startX:endX]
                    (fH, fW) = face.shape[:2]
                    # ensure the face width and height are sufficiently large
                    if fW < 20 or fH < 20:
                        continue
                    # construct a blob for the face ROI, then pass the blob
                    # through our face embedding model to obtain the 128-d
                    # quantification of the face
                    faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96),
                        (0, 0, 0), swapRB=True, crop=False)
                    embedder.setInput(faceBlob)
                    vec = embedder.forward()
                    # perform classification to recognize the face
                    preds = recognizer.predict_proba(vec)[0]
                    j = np.argmax(preds)
                    proba = preds[j]
                    name = le.classes_[j]

                    # draw the bounding box of the face along with the associated
                    # probability
                    text = "{}: {:.2f}%".format(name, proba * 100)

                    print(text)
                    return JsonResponse({"pessoa": name, "probabilidade": proba}, status=200, safe=False)

            return JsonResponse({"message": "Deu boa..."}, status=200, safe=False)
    

            ########################################################################################################
            ########################################################################################################
            ########################################################################################################
            ########################################################################################################


class NumpyArrayEncoder(JSONEncoder):
    """
    Aux classes for decoding NumPy arrays to Python objects.
    Returns:
        A list or a JSONEnconder object.
    """
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


class AboutProjectClass(View):

    def get(self, request):
        data = {}
        return render(request, 'about_the_project.html', data)