import cv2 as cv
import numpy as np
import tkinter as tk
import mediapipe as mp
from tkinter import messagebox
import sys


# -----------------------Définition des fonctions --------------------------------
#function detection pos
def detectionPose(img, pose, display = True):
    img_out = img.copy()
    imgRGB = cv.cvtColor(img_out, cv.COLOR_BGR2RGB)
    #Retrieve the height and width of the input image
    height, width,_ = img.shape
    # perfom pose detection
    resultat = pose.process(imgRGB)
    landmarks = []
    # verify if any landmarks are detected
    if resultat.pose_landmarks:
        #draw pose landmarks on the output image
        
        mp_drawing.draw_landmarks(image = img_out, landmark_list = resultat.pose_landmarks, connections = mp_pose.POSE_CONNECTIONS)
        for landmark in resultat.pose_landmarks.landmark:
            #append landmark into the list
            landmarks.append((landmark.x, landmark.y, landmark.z))
    #check if the original input image and the result image are specified to be displayed
    if display:
        plt.figure(figsize = (22,22))
        plt.subplot(121)
        plt.imshow(img)
        plt.title("Input image")
        plt.subplot(122)
        plt.imshow(img_out)
        plt.title("Output image")
    else:
        return img_out, landmarks

    
# fonction calcul de l'angle

def calculAngle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Fonction pour définir la main de préférence
def set_main_pref(main):
    global main_pref
    global main_pref_selected
    main_pref = main
    main_pref_selected = False
    fenetre.destroy()  # Ferme la fenêtre de dialogue après avoir fait le choix

# Fonction de fermeture
def on_closing():
    print("programme terminé")
    raise SystemExit()



# Définir la main de préférence
main_pref = "gauche"

# Interface graphique
fenetre = tk.Tk()
fenetre.title("choix de l'option") 
fenetre.geometry("500x400")

#fenetre.protocol("WM_DELETE_WINDOW", on_closing)

bouton_gauche = tk.Button(fenetre, text="Main gauche", command=lambda: set_main_pref("gauche"))
bouton_droit = tk.Button(fenetre, text="Main droite", command=lambda: set_main_pref("droite"))
bouton_deuxmains =  tk.Button(fenetre, text = "Deux Mains", command =lambda: set_main_pref("deuxmains"))
bouton_annuler = tk.Button(fenetre, text = "Annuler", command=lambda: set_main_pref(None))


    

# Ajouter les boutons à la fenêtre
bouton_gauche.pack()
bouton_droit.pack()
bouton_deuxmains.pack()
bouton_annuler.pack()


# Afficher la fenêtre
fenetre.mainloop()

#verifier si l'utilisateur à selectionner une option
if main_pref is None:
    print("Programme arreter")
    sys.exit()
    


counter = 0
stage = None   
#initializing mediapipe pose
mp_pose = mp.solutions.pose
#initializing mediapipe drawing
mp_drawing = mp.solutions.drawing_utils
#setting up the pose function

pose_video = mp_pose.Pose(static_image_mode = False, min_detection_confidence = 0.5, model_complexity = 1)

cap = cv.VideoCapture(0)
# Enregistrer le temps au debut de la lecture du flux video
# Boucle principale
while cap.isOpened():
    # Capture vidéo (remplacer avec votre code)
    ret, frame = cap.read()

    if ret:
        # Détecter les points clés (remplacer avec votre code)
        #frame, landmarks = detectionPose(frame, pose_video, display=False)

        try:
            #landmarks for left arm
            frame, landmarks = detectionPose(frame, pose_video, display=False)
            shoulder_left = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][0], landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value][1]]
            elbow_left = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value][0], landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value][1]]
            wrist_left = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value][0], landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value][1]]
            # landmarks for the right arm
            shoulder_right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][0], landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value][1]]
            elbow_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value][0], landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value][1]]
            wrist_right = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value][0], landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value][1]]

        except Exception as e:
            #print(f"Une erreur s'est produite : {e}")
            continue
        else:

            # Calculer l'angle du bras et les répétitions
            #-------------------------------------------------pour la main gauche------------------------------
            if main_pref == "gauche":
                angle = calculAngle(shoulder_left, elbow_left, wrist_left)
                if angle > 160:
                    stage = "down"
                if angle < 30 and stage == "down" and wrist_left[1] < shoulder_left[1] and wrist_left[1] < elbow_left[1] and shoulder_left[1] < elbow_left[1]:
                    stage = "up"
                    counter +=1
                    print(counter)
                    #Visualize angle
                    #cv.putText(frame, str(elbow_left[1]),
                       #tuple(np.multiply(elbow_left, [640,480]).astype(int)),
                       #cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
                    #cv.putText(frame, str(shoulder_left[1]), tuple(np.multiply(shoulder_left, [640,480]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, .5,
                    #                                   (255,255,255))
                    #cv.putText(frame, str(angle), tuple(np.multiply(shoulder_left, [640,480]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2)
            #print(landmarks)
            #---------------------------------------------------pour la main droite--------------------------
            elif main_pref == "droit":
                angle_droit = calculAngle(shoulder_right, elbow_right, wrist_right)
                # visualiser l'angle
                cv.putText(frame, str(angle_droit), tuple(np.multiply(elbow_right, [640,480]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2 )
                if angle_droit > 160:
                    stage = "down"
                if angle_droit < 30 and stage == "down" and wrist_right[1] < shoulder_right[1] and wrist_right[1] < elbow_right[1] and shoulder_right[1] < elbow_right[1]:
                    stage = "up"
                    counter +=1
                    print(counter)
                    #Visualize angle
                    
                    #cv.putText(frame, str(shoulder_right[1]), tuple(np.multiply(shoulder_right, [640,480]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, .5,
                    #                                    (255,255,255))
                    #cv.putText(frame, str(wrist_right[1]), tuple(np.multiply(wrist_right, [640,480]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                      #         (255,255,255))
            #--------------------------------------------------Pour les deux mains----------------------------
            
            elif main_pref == "deuxmains":
                angle_left = calculAngle(shoulder_left, elbow_left, wrist_left)
                angle_right = calculAngle(shoulder_right, elbow_right, wrist_right)
                    
                if angle_left > 160:
                    if angle_right > 160:
                        stage = "down"
                if angle_left < 30 and stage == "down" and wrist_left[1] < shoulder_left[1] and wrist_left[1] < elbow_left[1] and shoulder_left[1] < elbow_left[1]:
                    if angle_right < 30 and stage == "down" and wrist_right[1] < shoulder_right[1] and wrist_right[1] < elbow_right[1] and shoulder_right[1] < elbow_right[1]:
                        stage = "up"
                        counter +=1
                        print(counter)
                        #Visualize angle
                        #cv.putText(frame, str(elbow_left[1]),tuple(np.multiply(elbow_left, [640,480]).astype(int)),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255),2)
                        #cv.putText(frame, str(shoulder_left[1]), tuple(np.multiply(shoulder_left, [640,480]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, .5,(255,255,255),2)
                        #cv.putText(frame, str(wrist_left[1]), tuple(np.multiply(wrist_left, [640,480]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2)
            else:
                pass
            #setup box
            cv.rectangle(frame, (0,0), (225, 73), (245,23,23), -1)
            cv.putText(frame, 'REPS', (15,12),
                       cv.FONT_HERSHEY_SIMPLEX, .5, (0,0,0), 1, cv.LINE_AA)
            cv.putText(frame , str(counter), (10,60),
                       cv.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2, cv.LINE_AA)

            cv.putText(frame, 'STAGE', (75,12),
                       cv.FONT_HERSHEY_SIMPLEX, .5, (0,0,0), 1, cv.LINE_AA)
            cv.putText(frame , stage, (70,60),
                       cv.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2, cv.LINE_AA)
            cv.imshow("mediapipe", frame)

            quitte = cv.waitKey(1)
            if quitte == 27 or quitte == ord('q'):
                break
    else:
        break
temps_fin = cv.getTickCount()
# Fermer la fenêtre

cap.release()
cv.destroyAllWindows()

