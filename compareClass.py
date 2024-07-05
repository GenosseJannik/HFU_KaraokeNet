import wave

#Class to send all needed information for evaluation in one Session

class compareClass:
    karaoke_wav: str
    compared_song: str

    def __init__(self, karaoke_file: str, song_file: str, percentage_mfcc=None,
                 percentage_speech=None):
        self._karaoke_wav = karaoke_file
        self._compared_song = song_file
        self._percentage_mfcc = percentage_mfcc
        self._percentage_speech = percentage_speech

    @property
    def karaoke_wav(self):
        return self._karaoke_wav

    @karaoke_wav.setter
    def karaoke_wav(self, wav: str):
        self._karaoke_wav = wav

    @property
    def compared_song(self):
        return self._compared_song

    @compared_song.setter
    def compared_song(self, wav):
        self._percentage_mfcc = wav

    @property
    def overall_transposed_semitone_difference(self):
        return self._percentage_mfcc

    @overall_transposed_semitone_difference.setter
    def overall_transposed_semitone_difference(self, difference):
        self._overall_transposed_semitone_difference = difference

    @property
    def transposition(self):
        return self._transposition

    @transposition.setter
    def percentage_mfcc(self, transposition):
        self._transposition = transposition

    @property
    def result_singing_percentage(self):
        return self._result_singing_percentage

    @result_singing_percentage.setter
    def result_singing_percentage(self, percentage):
        self._result_singing_percentage = percentage

    @property
    def percentage_speech(self):
        return self._percentage_speech

    @percentage_speech.setter
    def percentage_speech(self, percentage):
        self._percentage_speech = percentage
