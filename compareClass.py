import wave


class compareClass:
    karaoke_wav: wave.Wave_read
    compared_song: wave.Wave_read

    percentage_mfcc
    percentage_speech

    def __init__(self, karaoke_file: wave.Wave_read, song_file: wave.Wave_read, percentage_mfcc=None,
                 percentage_speech=None):
        self._karaoke_wav = karaoke_file
        self._compared_song = song_file
        self._percentage_mfcc = percentage_mfcc
        self._percentage_speech = percentage_speech

    @property
    def karaoke_wav(self):
        return self._karaoke_wav

    @karaoke_wav.setter
    def karaoke_wav(self, wav: wave.Wave_read):
        self._karaoke_wav = wav

    @property
    def compared_song(self):
        return self._compared_song

    @compared_song.setter
    def compared_song(self, wav):
        self._percentage_mfcc = wav

    @property
    def percentage_mfcc(self):
        return self._percentage_mfcc

    @percentage_mfcc.setter
    def percentage_mfcc(self, percentage):
        self._percentage_mfcc = percentage

    @property
    def percentage_speech(self):
        return self._percentage_speech

    @percentage_speech.setter
    def percentage_speech(self, percentage):
        self._percentage_speech = percentage
