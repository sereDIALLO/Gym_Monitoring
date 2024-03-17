import cv2 as cv
from picamera2 import Picamera2
import numpy as np
import tkinter as tk
import mediapipe as mp
from tkinter import messagebox
import sys
import max30100


# -----------------------Definition des fonctions --------------------------------

# Detection de pose
def detectionPose(img, pose, display = True):
    img_out = img.copy()
    imgRGB = cv.cvtColor(img_out, cv.COLOR_BGR2RGB)
    
    #Recupérer height, width sur l'image d'entrée
    height, width,_ = img.shape
    # Effectuer la détection de pose
    resultat = pose.process(imgRGB)
    landmarks = []
    # verifier si des landmarks sont détectés
    if resultat.pose_landmarks:
        #Dessiner les pose landmarks sur l'image de sortie
        
        mp_drawing.draw_landmarks(image = img_out, landmark_list = resultat.pose_landmarks, connections = mp_pose.POSE_CONNECTIONS)
        for landmark in resultat.pose_landmarks.landmark:
            # ajouter les landmark dans la list
            landmarks.append((int(landmark.x * width), int(landmark.y*height), int(landmark.z * width)))
    # Verifiez si l'image d'entrée et l'image de sortie sont spécifiées pour etre affichées.
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

    
# calcul des angles

def calculAngle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Definition de la main de preference
def set_main_pref(main):
    global main_pref
    global main_pref_selected
    main_pref = main
    main_pref_selected = False
    fenetre.destroy()  # Ferme la fenetre de dialogue apres avoir fait le choix

# Arret du programmer
def on_closing():
    print("programme terminer")
    raise SystemExit()
# renitialisation du programme
def reset_training():
    counter = 0
    stage = None
    main_pref = None
    main_pref_selected = False
    # fermer la fenetre de calories si elle est ouvertes
    try :
            
        fenetre_calories.destroy()
    except tk.TclError:
        pass
    # Reafficher la fenetre de choix
    fenetre.deiconify()
# Recuperation de la frequence cardique
def update_pulse_label(max30, detected_pulse, pulse_label, last_value):
    max30.read_sensor()
    nb = int(max30.ir / 100)
    if max30.ir != max30.buffer_ir:
        if nb > 0:
            pulse_label.config(text="Pulse : {}".format(nb))
            detected_pulse.set(True)
            last_value = nb
            
    if not detected_pulse.get():
        fenetre_calories.after(2000, update_pulse_label, max30, detected_pulse, pulse_label, last_value)  # Appeler cette fonction apres 2 secondes
    return last_value

# Estimation du nombre de calories brulees.
def calories_brule(pouls, MET):
    # MET : L'equivalent metabolique (Metabolic Equivalent of Task)
    temps_seconde = int( (temps_fin - temps_debut) /cv.getTickFrequency() )
    #print(f"temps en seconde : {temps_seconde}")
    # Convertir le temps en heure
    temps_heure = (temps_seconde/3600)
    # Calculer le nombre de calories brulees
    poids = 70
    calories = (MET * poids * temps_heure * 0.01 * pouls* 0.05* counter)
    # Afficher les calories brulées dans une etiquette
    label_calories_affichage.config(text = "Calories brulées : {}".format(round(calories, 2)))



# Definir la main de preference
main_pref = "gauche"

# fenetre principale
fenetre = tk.Tk()
fenetre.title("choix de l'option") 
fenetre.geometry("500x400")

# Création des boutons d'interface
bouton_gauche = tk.Button(fenetre, text="Bras gauche", command=lambda: set_main_pref("gauche"))
bouton_droit = tk.Button(fenetre, text="Bras droite", command=lambda: set_main_pref("droit"))
bouton_deuxmains =  tk.Button(fenetre, text = "Deux bras", command =lambda: set_main_pref("deuxbras"))
bouton_annuler = tk.Button(fenetre, text = "Quitter", command=lambda: set_main_pref(None))

# Pour rendre les boutons visibles sur l'interface
bouton_gauche.pack()
bouton_droit.pack()
bouton_deuxmains.pack()
bouton_annuler.pack()

# Afficher la fenetre
fenetre.mainloop()

#verifier si l'utilisateur a  selectionner une option
if main_pref is None:
    print("Programme arreter")
    sys.exit()
    
# variable counter qui stockera le nombre de fois l'utilisateur soulève l'haltère.
counter = 0
# Suivre l'état de mouvement du bras
stage = None   
#initialisation de mediapipe pose
mp_pose = mp.solutions.pose
#initialisation de mediapipe drawing
mp_drawing = mp.solutions.drawing_utils
# Mise en place de la fonction de pose
pose_video = mp_pose.Pose(static_image_mode = False, min_detection_confidence = 0.5, model_complexity = 1)
# pour lancer le flux video avec picamera2
picam = Picamera2()
picam.configure(picam.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam.start()

# Enregistrer le temps au debut de la lecture du flux video
temps_debut = cv.getTickCount()
# Boucle principale
while True:
    frame = picam.capture_array()
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    #ret, frame = cap.read()
   
    frame, landmarks = detectionPose(frame, pose_video, display=False)
    
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

        # Calculer l'angle du bras et les repetitions
        #-------------------------------------------------pour le bras gauche------------------------------
        
        if main_pref == "gauche":
            MET = 3
            angle = calculAngle(shoulder_left, elbow_left, wrist_left)
            if angle > 160:
                stage = "down"
            if angle < 30 and stage == "down" and wrist_left[1] < shoulder_left[1] and wrist_left[1] < elbow_left[1] and shoulder_left[1] < elbow_left[1]:
                stage = "up"
                counter +=1
                print(counter)
                #Visualiser angle
                cv.putText(frame, str(elbow_left[1]),
                    tuple(np.multiply(elbow_left, [640,480]).astype(int)),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
                cv.putText(frame, str(shoulder_left[1]), tuple(np.multiply(shoulder_left, [640,480]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, .5,
                                                        (255,255,255))
                cv.putText(frame, str(wrist_left[1]), tuple(np.multiply(wrist_left, [640,480]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                       (255,255,255))
            #print(landmarks)
            #---------------------------------------------------pour le bras droit--------------------------
            
        elif main_pref == "droit":
            MET = 3
            angle = calculAngle(shoulder_right, elbow_right, wrist_right)
            if angle > 160:
                    stage = "down"
            if angle < 30 and stage == "down" and wrist_right[1] < shoulder_right[1] and wrist_right[1] < elbow_right[1] and shoulder_right[1] < elbow_right[1]:
                stage = "up"
                counter +=1
                MET = 3
                print(counter)
                #Visualiser angle
                cv.putText(frame, str(elbow_right[1]),
                    tuple(np.multiply(elbow_right, [640,480]).astype(int)),
                    cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
                cv.putText(frame, str(shoulder_right[1]), tuple(np.multiply(shoulder_right, [640,480]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, .5,
                                                        (255,255,255))
                cv.putText(frame, str(wrist_right[1]), tuple(np.multiply(wrist_right, [640,480]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                               (255,255,255))
            
            #--------------------------------------------------Pour les deux bras----------------------------
            
        elif main_pref == "deuxbras":
            MET = 6
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
                #cv.putText(frame, str(elbow_left[1]),
                    tuple(np.multiply(elbow_left, [640,480]).astype(int)),
                   # cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
                #cv.putText(frame, str(shoulder_left[1]), tuple(np.multiply(shoulder_left, [640,480]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, .5,
                                                       # (255,255,255))
                #cv.putText(frame, str(wrist_left[1]), tuple(np.multiply(wrist_left, [640,480]).astype(int)), cv.FONT_HERSHEY_SIMPLEX, 0.5,
                      # (255,255,255))
        else:
            MET = 0
            pass
        #setup box
        cv.rectangle(frame, (0,0), (225, 73), (23,23,245), -1)
        cv.putText(frame, 'REPS', (15,12),
                       cv.FONT_HERSHEY_SIMPLEX, .5, (0,0,0), 1, cv.LINE_AA)
        cv.putText(frame , str(counter), (10,60),
                    cv.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2, cv.LINE_AA)

        cv.putText(frame, 'STAGE', (75,12),
                    cv.FONT_HERSHEY_SIMPLEX, .5, (0,0,0), 1, cv.LINE_AA)
        cv.putText(frame , stage, (70,60),
                       cv.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2, cv.LINE_AA)
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        cv.imshow("mediapipe", frame)

        quitte = cv.waitKey(1)
        if quitte == 27 or quitte == ord('q'):
            break
# Enregistrer le temps a la fin de la lecture video
temps_fin = cv.getTickCount()
# Interface pour l'estimation des calories burlees.
fenetre_calories = tk.Tk()
fenetre_calories.title("Estimation des calories brulees")
fenetre_calories.geometry("330x200")
fenetre_calories.configure(bg="#DCDCDC")

detected_pulse = tk.BooleanVar()

last_pouls = 0
# Initialiser le capteur MAX30100
max30 = max30100.MAX30100()
max30.enable_spo2()

# Variable de controle pour detecter le pouls
detected_pulse = tk.BooleanVar()
detected_pulse.set(False)

label_instructions = tk.Label(fenetre_calories, text = "Placez votre doigt sur le capteur.")
pulse_label = tk.Label(fenetre_calories, text = "Pulse : ")
label_calories_affichage = tk.Label(fenetre_calories, text="")
pouls = update_pulse_label(max30, detected_pulse, pulse_label, last_pouls)
bouton_valider = tk.Button(fenetre_calories, text = " OK", command = lambda pouls = pouls , MET = MET: calories_brule(pouls, MET))

#print(pouls)
# pour rendre les labels et boutons visible dans l'interface
label_instructions.pack()
pulse_label.pack(pady=10)
bouton_valider.pack()
label_calories_affichage.pack()



# Fermer toutes les fenetres

cv.destroyAllWindows()
fenetre_calories.mainloop()
