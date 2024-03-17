# GYM-MONITORING
![Logo Grafikart.fr](https://learnopencv.com/wp-content/uploads/2022/12/squats_landmarks_used_in_application_ai_fitness_trainer.png)
## Introduction
### Contexte:
Dans le contexte croissant de l'innovation technologique, les systèmes de vision par ordinateur ont gagné en popularité dans divers domaines de la réalité augmentée à la surveillance médicale. Ces systèmes permettent d'extraire des informations précieuses à partir d'images et de vidéos, ouvrant la voie à de nombreuses applications potentielles.

### Objectif:
L'objectif de ce projet est de développer un système de suivi de position en temps réel sur une **Raspberry pi 4**, utilisant une **camera v2.1** et un **capteur de frequence cardique MAX30100**, tout en réalisant une estimation du nombre de calories brûlées par la personne pratiquant une activité physique. Pour atteindre cet objectif, j'ai utilisé la bibliothèque MediaPipe développée par Google Research. Cette bibliothèque offre des fonctionnalités avancées pour la détection de pose, ce qui me permet de suivre les mouvements du corps en temps réel à partir d'une vidéo. J'ai également intégré un calculateur d'estimation des calories brûlées basé sur le nombre de mouvements détectés et le rythme cardiaque estimé.

Le système fonctionne en capturant la vidéo en temps réel à l'aide de la **camera v2.1**, puis en utilisant mon algorithme de détection de pose pour identifier les points clés du corps, tels que les épaules, les coudes et les poignets. À partir de ces points, l'angle formé par les segments du bras est calculé pour déterminer si un mouvement spécifique, comme le soulèvement d'un haltère, est effectué. En fonction de la préférence de l'utilisateur (bras gauche, bras droit ou les deux), le système suit le mouvement approprié et compte le nombre de répétitions.

En parallèle, un capteur de fréquence cardiaque **MAX30100** est utilisé pour estimer le rythme cardiaque de l'utilisateur en plaçant son doigt sur le capteur. Cette mesure est ensuite utilisée pour ajuster le calcul des calories brûlées en fonction de l'intensité de l'activité physique.

Dans les jours à venir, je prévois de partager une vidéo explicative du projet, mettant en lumière son fonctionnement et ses détails.

Merci à bientôt.
