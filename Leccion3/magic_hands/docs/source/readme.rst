¿Qué es Magic Hands?
====================

Magic Hands es una aplicación basada en visión por computador que permite al usuario
tocar notas musicales utilizando sus dedos.

Usando la aplicación
---------------------

Una vez la aplicación está en ejecución nos colocamos delante de la gfuente de video
de tal manera que sea capaz de capturar ambas manos por completo.

Si lo hemos hecho bien, cada dedo de nuestras manos tendrá asignada una nota musical.

Si juntamos un dedo con una nota asignada junto con el pulgar, reproduciremos el sonido
de dicha nota.

Display options:
~~~~~~~~~~~~~~~~

**Show FPS:** Muestra los frames por segundo en la parte superior izquierda de la pantalla.

**Show hand model:** Dibuja el modelo de mano sobre las manos detectadas, uniendo los marcadores
por lineas rectas simulando un esqueleto.

**Show notes:** Muestra por pantalla las notas asignadas a cada dedo.

**Show played notes:** Fncionalidad aún no soportada.

Sound options:
~~~~~~~~~~~~~~~~

**Mute sound output:** Permite mutear la aplicación, si esta opción está habilitada las notas
musicales que toquemos no se escucharán.

**Volume:** Ajusta el volumen del reproductor.

Advanced sound options
~~~~~~~~~~~~~~~~~~~~~~~

**Note duration:** Duración en segundos de las notas.

**Delay between notes:** Si dejamos una nota pulsada, este parámetro indicará cada cuantos segundos
detectaremos la siguiente nota, permite controlar el comportamiento de la detección para que el sonido
no se solapen las notas.


Ejecutando la aplicación
==========================

Requerimientos
---------------
    - Cámara web o alguna otra fuente de video (video stream)


Instrucciones
--------------
1. En la carpeta raiz ejecutar el siguiente comando:

>>> pip install -r .\magic_hands\requirements.txt

2. A continuación asegurate de tener la cámara web conectada a tu ordenador.

3. Por útimo, también desde la carpeta raiz ejecuta el siguiente comando:

>>> pip install -r .\magic_hands\main.pyw