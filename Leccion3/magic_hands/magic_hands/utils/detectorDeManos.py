import cv2
import mediapipe as mp
import time
import math



class detectorDeManos():
    """
    detectorDeManos. Es la clase encargada de detecar los gestos de la mano para asignarle una nota musical a cada dedo
    y luego detectar los gestos de la mano para decidir qué notas estamos intentando tocar.

    Esta clase está basada en la librería `MediaPipe (Hands) <https://google.github.io/mediapipe/solutions/hands.html>`_ de
    Google. MediaPipe es una solución de tracking de dedos de alta fidelidad que utiliza machine learning (ML) para inferir
    21 marcadores (landmarks) 3D de una mano a partir de solamente un frame.

    De este modelo de mano de 21 puntos, tienen especial relevancia en este proyecto los puntos 4 8, 12, 16 y 20 que
    corresponden a la punta de cada dedo (de pulgar a meñique)

    Para el tratamiento de imagenes (frames) se utiliza la conocida librería `OpenCV-Python
    <https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html>`_.


    ==================  =========================== ==================================================================
    Atributos           Valor por defecto           Comentarios
    ==================  =========================== ==================================================================
    modo_estatico       False                       False = tratamos los frames de entrada como streams de video
    num_manos           2                           Indica el numero de manos que se intentará detectar en cada frame
    confianzaDeteccion  0.5                         Umbral de confianza de detección de las manos.
                                                    Si el valor de deteccion es superior al definido en
                                                    confianzaDeteccion, entonces nos evitamos seguir detectando la
                                                    mano y solo hacemos tracking, para disminuir la carga de procesado
    confianzaTracking   0.5                         Umbral de confianza del seguimiento de los dedos
    mpHands             mp.solutions.hands          Modelo de mano
    mpDraw              mp.solutions.drawing_utils  Permite dibujar marcadores y otros elementos del modelo de manos
    hands               mpHands.Hands()             Detector de manos
    ==================  =========================== ==================================================================


    =================  ========================  =====================================================================
    Métodos            Parámetros                Comentario
    =================  ========================  =====================================================================
    detectarManos      img                       Intenta detectar las manos en una escena a partir de un frame (img).
                       draw                      Si draw==True, el método devuelve la imagen con los marcadores
                                                 pintados sobre las manos detectadas y unidos por líneas rectas.
                                                 Al ejecutar este método se guardan internamente los marcadores de los
                                                 dedos
    detectarPosicion   img                       Luego de ejecutar detectarManos(), detectarPosicion() devuelve para
                       mano                      la mano indicada por parámetro, una lista de marcadores con la
                                                 siguiente información: id de marcador, cordenada x, coordenada y.
    detectarNotas      lmList                    Mide el módulo (distancia) entre el índice de la mano indicada (mano)
                       mano                      y los dedos restantes (4 dedos si es la primera mano, 3 si es la
                                                 segunda, ya que trabajamos sólo con  notas musicales) utilizando la
                                                 lista de marcadores que pasamos por parámetro (lmList), para decidir
                                                 qué nota se está tocando (cada dedo excepto el pulgar representa una
                                                 nota mayor)
    pintarNotas        img                       Sirve para mostrar por pantalla al usuario las notas asignadas
                       lmList                    a cada dedo de cada mano
                       mano
                       draw
    =================  ========================  =====================================================================

    Ejemplos:
    ===========
    >>> import detectorDeManos as ddm
    >>> detector = ddm.detectorDeManos(confianzaDeteccion=0.8)           # Inicializa detector
    >>> img_result = detector.detectarManos(img, draw=True)              # Detectamos manos en la escena
    >>> # Primera mano
    >>> lmList1 = detector.detectarPosicion(img, 0)                      # Lista de marcadores primera mano
    >>> notas = detector.detectarNotas(lmList1, 0)                       # Evaluamos el gesto de la mano
    >>> detector.pintarNotas(img, lmList1, 0, display_notes_identifiers) # Printamos notas sobre los dedos de la mano 1
    >>> # Segunda mano
    >>> lmList2 = detector.detectarPosicion(img, 1)                      # Repetimos para la segunda mano si la hubiese
    >>> notas = detector.detectarNotas(lmList2, 1)
    >>> detector.pintarNotas(img, lmList2, 1, display_notes_identifiers)

    """
    def __init__(self, modo_estatico=False, num_manos=2,
                 confianzaDeteccion=0.5, confianzaTracking=0.5):
        self.modo_estatico = modo_estatico
        self.num_manos = num_manos
        self.confianzaDeteccion = confianzaDeteccion
        self.confianzaTracking = confianzaTracking
        # Inicializo el detector de manos
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.modo_estatico,
                                        max_num_hands=self.num_manos,
                                        min_detection_confidence=self.confianzaDeteccion,
                                        min_tracking_confidence=self.confianzaTracking)
        # Sirve para jugar con el modelo de mano y pintar las landmarks o
        # trazar líneas entre ellas
        self.mpDraw = mp.solutions.drawing_utils

    def detectarManos(self, img, draw=False):
        """
        Detecta las manos en la escena a partir de un frame. Si la opción draw es igual a True devolverá una imagen
        con los marcadores de los dedos dibujados encima de la mano. Esta función guarda internamente los marcadores

        :param img: Frame de la escena donde detectaremos la mano
        :param draw: Si es True dibuja el modelo de mano sobre la escena
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLandmarks,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def detectarPosicion(self, img, mano=0):
        """
        Devuelve una lista de marcadores con sus respectivos IDs asi como sus coordenadas x e y.

        :param img: imagen de la escena que contiene los marcadores, de la cual se extraen las dimensiones
        :param mano: Mano activa (0 o 1)
        :return: lmList (listado de landmarks o marcadores para la mano indicada con sus respectivas cordenadas x e y)
        """
        lmList = []
        if self.results.multi_hand_landmarks:
            try:
                manoActiva = self.results.multi_hand_landmarks[mano]
                for id, landmark in enumerate(manoActiva.landmark):
                    heigth, width, channel = img.shape
                    cx, cy = int(landmark.x*width), int(landmark.y*heigth)
                    lmList.append([id, cx, cy])
            except IndexError:
                # He quitado los prints para intentar ganar FPSs.....
                # print("Error de índice."+"Probablemente no hay una segunda mano en la escena")"
                pass
        return lmList

    def pintarNotas(self, img,  lmList, mano=0, draw=False):
        """

        :param img: Frame de la escena donde pintaremos las notas
        :param lmList: Lista de marcadores devueltos por detectarPosicion()
        :param mano: Mano activa (0 o 1)
        :param draw: Si es True dibuja las notas sobre cada dedo en la escena
        """
        notasMano1 = ["Do", "Re", "Mi", "Fa"]
        notasMano2 = ["Sol", "La", "Si"]
        for landmark in lmList:
            if mano == 0:
                if draw and landmark[0] % 4 == 0 and landmark[0] > 4:
                    cv2.circle(img, (landmark[1], landmark[2]), 5,
                               (255, 0, 255), cv2.FILLED)
                    cv2.putText(img, notasMano1[(int(landmark[0]/5))-1],
                                (landmark[1], landmark[2]),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            if mano == 1:
                if draw and landmark[0] % 4 == 0 and landmark[0] > 4 and landmark[0] < 20:
                    cv2.circle(img, (landmark[1], landmark[2]), 5,
                               (255, 0, 255), cv2.FILLED)
                    cv2.putText(img, notasMano2[(int(landmark[0]/4))-2],
                                (landmark[1], landmark[2]),
                                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    def detectarNotas(self, lmList, mano=0):
        """
        Calcula la distancia entre el pulgar (que funciona como actuador) y algun otro dedo de la mano que tenga una
        nota musical asignada. Si esta distancia es menor de cierto rango confirmamos la detección del gesto de una nota
        determinada.

        :param lmList: Lista de marcadores devueltos por detectarPosicion()
        :param mano: Mano activa (0 o 1)
        :return: Lista de notas detectadas
        """
        notas = []
        notasMano1 = ["Do", "Re", "Mi", "Fa"]
        notasMano2 = ["Sol", "La", "Si"]

        for landmark in lmList:
            if landmark[0] == 4:
                x1, y1 = landmark[1], landmark[2]
            try:
                if mano == 0:
                    if landmark[0] % 4 == 0 and landmark[0] > 4:
                        x2, y2 = landmark[1], landmark[2]
                        length = math.hypot(x2 - x1, y2 - y1)
                        if length < 30:
                            notas.append(notasMano1[(int(landmark[0]/5))-1])
                if mano == 1:
                    if landmark[0] % 4 == 0 and landmark[0] > 4 and landmark[0] < 20:
                        x2, y2 = landmark[1], landmark[2]
                        length = math.hypot(x2 - x1, y2 - y1)
                        if length < 30:
                            notas.append(notasMano2[(int(landmark[0]/4))-2])
            except IndexError:
                # print(f"Error de índice. No se detecta el pulgar (x1, x2)")
                pass
        return notas
