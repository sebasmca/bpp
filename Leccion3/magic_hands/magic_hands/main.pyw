from utils import detectorDeManos as ddm
from utils import reproducirNota as rn
import cv2
import time
import tkinter as tk
from tkinter import messagebox, StringVar
from PIL import Image, ImageTk


# Ventana o raiz (root)
raiz = tk.Tk()
# Titulo
raiz.title("Aplicación GUI en Tkinter - Master Python 4 EIP")
raiz.geometry("1040x510")

###########################################################################
# Defino un label donde embeberé el imput de video que capturo de la webcam
handler_video = tk.Label(raiz, bg="black")
handler_video.place(x=385, y=15)

############################################################################
# configuro la captura de video. La entrada tendrá ancho y alto fijos porque
# variarlo puede afectar notablemente a la performance de la aplicación,
# sobre la parte de deteccion de manos con intervalos de confianza altos
wCam, hCam = 640, 480
cam = cv2.VideoCapture(0)
cam.set(3, wCam)
cam.set(4, hCam)

############################################################################
# Iniciamos el detector de manos con un nivel alto de confianza de deteccion
detector = ddm.detectorDeManos(confianzaDeteccion=0.8)

# ##########################################################################
# Variables para controlar lo que dibujaré en la imagen entre otras cosas
display_hand_skel = False
display_notes_identifiers = True
display_fps = False
display_played_notes = False
player_volume = 0.3
mute_output = False
note_duration = 0.4
note_detections_delay = 0.5

# ##########################################################################
# Inicialización del reproductor para tocar la nota detectada
player = rn.reproducirNota()
player.initPlayer(player_volume)

# Variables auxiliares para calcular el frame-rate
cTime = 0
pTime = 0

def show_frames():
    global cTime
    global pTime

    # Leemos una imagen de la cámara
    try:
        success, img = cam.read()
        assert success == True
    except AssertionError:
        messagebox.showinfo("Error", "Video input not detected. The progam will terminate")
    # #######################################################################
    # Lógica principal encargada de detectar las manos, la posicion  y los
    # landmarks para poder detectar la nota que estamos tocando.
    # Primero se detectan cuantas manos hay en la escena y posteriormente
    # se detecta la nota tocada con cada mano.
    img_result = detector.detectarManos(img, display_hand_skel)
    # Primera mano
    lmList1 = detector.detectarPosicion(img, 0)
    notas = detector.detectarNotas(lmList1, 0)
    player.play(notas, note_duration, note_detections_delay, mute_output)
    detector.pintarNotas(img, lmList1, 0, display_notes_identifiers)
    # Segunda mano
    lmList2 = detector.detectarPosicion(img, 1)
    notas = detector.detectarNotas(lmList2, 1)
    player.play(notas, note_duration, note_detections_delay, mute_output)
    detector.pintarNotas(img, lmList2, 1, display_notes_identifiers)

    # #######################################################################
    # Calculo el framerate para mostrarlo en la imagen de forma opcional
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    if display_fps:
        cv2.putText(img, f"FPS: {str(int(fps))}", (10, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    # #######################################################################
    # Represento la imagen en el label (handler_video).
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_aux = Image.fromarray(imgRGB)
    imgtk = ImageTk.PhotoImage(image=img_aux)
    handler_video.imgtk = imgtk
    handler_video.configure(image=imgtk)
    # Para crear un loop de video actualizo el label (handler) cada segundo:
    handler_video.after(1, show_frames)

# ############################################################################
# Elementos GUI
def toggle_fps():
    global display_fps
    if tgl_display1.config('relief')[-1] == 'sunken':
        tgl_display1.config(relief="raised")
        display_fps = False
    else:
        tgl_display1.config(relief="sunken")
        display_fps = True

def toggle_skel():
    global display_hand_skel
    if tgl_display2.config('relief')[-1] == 'sunken':
        tgl_display2.config(relief="raised")
        display_hand_skel = False
    else:
        tgl_display2.config(relief="sunken")
        display_hand_skel = True

def toggle_notes():
    global display_notes_identifiers
    if tgl_display3.config('relief')[-1] == 'sunken':
        tgl_display3.config(relief="raised")
        display_notes_identifiers = False
    else:
        tgl_display3.config(relief="sunken")
        display_notes_identifiers = True

'''TODO: No me ha dado tiempo de implementar la funcionalidad de pintar las notas
ya tocadas en un buffer en la parte inferior de la pantalla, por lo que este
callback no tiene efecto y por ello el botón de la UI se muestra inactivo (rojo)'''

def toggle_played_notes():
    global display_played_notes
    if tgl_display4.config('relief')[-1] == 'sunken':
        tgl_display4.config(relief="raised")
        display_played_notes = False
    else:
        tgl_display4.config(relief="sunken")
        display_played_notes = True

def help1():
    messagebox.showinfo(
        message='''Shows the frames per seconds on the top-left corner of the video. Ideally above 25 FPS for a good experience''',
        title="Show FPS")

def help2():
    messagebox.showinfo(
        message='''Shows the hand model in real time. Disable to improve the processing time per frame''',
        title="Show hand model")

def help3():
    messagebox.showinfo(message='''Shows the music note assigned to each finger''',
                        title="Show notes")

def help4():
    messagebox.showinfo(message='''On-screen buffer displaying last played notes''',
                        title="Show displayed notes")

muted = tk.IntVar()

def check_changed():
    global mute_output
    global player
    if muted.get() == 1:
        mute_output = True
    if muted.get() == 0:
        mute_output = False

def change_vol(default):
    global player_volume
    global player
    player_volume = vol.get()
    player.initPlayer(player_volume)

sb1_def = StringVar(raiz)
sb1_def.set("0.4")
sb2_def = StringVar(raiz)
sb2_def.set("0.5")

def get():
    global note_duration
    global note_detections_delay
    note_duration = float(spinbox1.get())
    note_detections_delay = float(spinbox2.get())

lbl_optionGrp1 = tk.Label(raiz, text="Display options").place(x=15, y=15)
tgl_display1 = tk.Button(raiz, text="Show FPS", relief="raised", width=15, height=2, command=toggle_fps)
tgl_display1.place(x=30, y=45)
btn_help1 = tk.Button(raiz, text="?", bg="cyan", command=help1).place(x=150, y=52)
tgl_display2 = tk.Button(raiz, text="Show hand model", relief="raised", width=15, height=2, command=toggle_skel)
tgl_display2.place(x=200, y=45)
btn_help2 = tk.Button(raiz, text="?", bg="cyan", command=help2).place(x=320, y=52)
tgl_display3 = tk.Button(raiz, text="Show notes", relief="sunken", width=15, height=2, command=toggle_notes)
tgl_display3.place(x=30, y=90)
btn_help3 = tk.Button(raiz, text="?", bg="cyan", command=help3).place(x=150, y=97)
tgl_display4 = tk.Button(raiz, text="Show played notes", bg="red", fg="white", relief="raised", width=15, height=2,
                         state=tk.DISABLED, command=toggle_played_notes)
tgl_display4.place(x=200, y=90)
btn_help4 = tk.Button(raiz, text="?", bg="cyan", command=help4).place(x=320, y=97)
lbl_optionGrp2 = tk.Label(raiz, text="Sound options").place(x=15, y=147)
checkbox1 = tk.Checkbutton(raiz, text='Mute sound output', command=check_changed, variable=muted, onvalue='1',
                           offvalue="0")
checkbox1.place(x=30, y=177)
vol = tk.Scale(raiz, label="Volume", troughcolor="purple", activebackground="green", from_=0.1, to=1.0,
               orient=tk.HORIZONTAL, resolution=.1, command=change_vol)
vol.place(x=30, y=207)
vol.set(0.3)
lbl_optionGrp3 = tk.Label(raiz, text="Advanced options").place(x=15, y=267)
lbl_spin1 = tk.Label(raiz, text="Note duration").place(x=30, y=297)
spinbox1 = tk.Spinbox(raiz, from_=0.1, to=2.0, increment=0.1, textvariable=sb1_def, width=4, command=get)
spinbox1.place(x=150, y=297)
lbl_spin2 = tk.Label(raiz, text="Delay between notes").place(x=30, y=337)
spinbox2 = tk.Spinbox(raiz, from_=0.1, to=2.0, increment=0.1, textvariable=sb2_def, width=4, command=get)
spinbox2.place(x=150, y=337)
exit_button = tk.Button(raiz, text="Exit", width=15, command=raiz.destroy)
exit_button.place(x=30, y=400)
##############################################################################
##############################################################################
messagebox.showinfo(message='''Para esta lección he implementado una especie de mini-juego en el cual podemos hacer sonar una nota musical al juntar cualquiera de nuestros dedos con el pulgar
de tu mano correspondiente. ¡Utiliza tus dos manos para jugar!\n
He escogido el campo de computer vision porque tengo algo de experiencia académica en la materia y además, desde hace ya un tiempo que quería probar la librería de google "mediapipe" de Google
proporciona detección de manos, cuerpo, descriptores faciales y mallas faciales.\n
También heutilizado la conocida librería OpenCV para obtener el input de la cámara y hacer algunas transformaciones.\n
Por último, se pueden customizar algunos elementos del juego utilizando widgets de tkinter.''',
                    title="¡Bienvenido!")
show_frames()
# algo que se coloca al final
raiz.mainloop()

