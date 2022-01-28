import musicalbeeps
import time


class reproducirNota:
    """
    ReproducirNotas. Es una clase que nos permite reproducir los siete sonidos de la escala musical diatónica (Do, Re,
    Mi, Fa, Sol, La, Si) de una forma sencilla. Esta clase se basa en la librería
    `musicalbeeps <https://pypi.org/project/musicalbeeps/>`_ que nos permite crear un reproductor Player() el cual nos
    permite reproducir un sonido indicándole la nota y su duración.

    Atributos:
    ==========

    ==================  =============  =================  =============================================================
    Atributos           Condición      Valor por defecto  Comentario
    ==================  =============  =================  =============================================================
    volume              opcional       0.3                Nivel de sonido del reproductor Player(). Rango 0.0 - 1.0
    mute_output         opcional       True               Permite silenciar el reproductor para que no imprima por
                                                          consola las notas que vamos reproduciendo.
    ==================  =============  =================  =============================================================

    Métodos:
    ========

    ==============  ========================  ============  =======================================================
    Métodos         Parámetros                Condición     Comentario
    ==============  ========================  ============  =======================================================
    initPlayer      volume                    opcional      Inicializa el reproductor
    play            lista_notas               requerido     Reproduce las notas musicales que le pasamos por lista
                    note_duration             requerido
                    note_delay                requerido
                    mute_output               requerido
    ==============  ========================  ============  =======================================================

    ejemplos:
    ===========
    >>> import reproducirNota as rn
    >>> player = rn.reproducirNota()
    >>> player.initPlayer(player_volume = 0.5)
    >>> player.play(listaNotas = ["Si", "La"], note_duration = 1, note_detections_delay = 1.2, mute_output = False )
    """

    def __init__(self, volume=0.3, mute_output=True):
        self.volume = volume
        self.mute_output = mute_output
        self.ultima_nota = None
        self.cTime = 0
        self.pTime = 0

    def initPlayer(self, volume=None):
        """
        Metodo para inicializar el reproductor. Al inicializar el reproductor se asigna también su nivel de volumen.

        Inputs:
        * self.volume: volumen del reproductor que se setea al crear un objeto de la clase reproducirNota().
        Valores posibles: de 0 a 1.

        * volume (opcional): opcionalmente sobrescribe el valor de self.volume al inicializar el reproductor.

        Output:
            Inicializa el reproductor para poder reproducir sonidos

        """
        if volume is None:
            self.player = musicalbeeps.Player(self.volume, self.mute_output)
        else:
            self.volume = volume
            self.player = musicalbeeps.Player(volume, self.mute_output)

    def play(self, lista_notas, note_duration, note_delay, mute_output):
        """
        Metodo para reproducir las notas musicales. Le pasamos una lista de notas y las irá reproduciendo de acuerdo
        a la duración y retraso de detección de la nota siguiente que hayamos elegido.

        Inputs:

            listaNotas: volumen del reproductor. Valores posibles: de 0 a 1
            note_duration: duración de la nota musical en segundos. Valores recomendados de 0.5 a 1.5
            note_delay: retardo para reproducir la siguiente nota musical.
            mute_output: permite silenciar el reproductor.

        Output:
            Reproduce el sonido de una nota musical

        """
        # Internacionalizo las notas ya que la librería para reproducir
        # las notas sólo las reproduce de esa manera
        notas_anglo = {"Do": "C", "Re": "D", "Mi": "E", "Fa": "F",
                       "Sol": "G", "La": "A", "Si": "B"}
        self.cTime = time.time()
        for nota in lista_notas:
            if notas_anglo[nota] != self.ultima_nota or (self.cTime - self.pTime) >= note_delay:
                if not mute_output:
                    self.player.play_note(notas_anglo[nota], note_duration)
                self.ultima_nota = notas_anglo[nota]
                self.pTime = self.cTime
