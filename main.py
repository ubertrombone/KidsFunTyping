from pathlib import Path
import pyttsx3
import sounddevice as sd
import soundfile as sf
from ttsmms import TTS


def run():
    """
    Reads the file "text.txt" stored in the same location as "main.py" and returns only the lines of the file that
    aren't blank.
    """
    text = filter(lambda x: x != "", Path('text.txt').read_text().split('\n'))
    engine = pyttsx3.init()
    '''Sets voice volume (0.0 - 1.0)'''
    engine.setProperty('volume', 1.0)
    '''Sets the voice speech rate (words per minute)'''
    engine.setProperty('rate', 120)
    '''
    (Different OS's use different TTS engines so experiment with the voices to find the one
    best suited to you).
    NB: For MacOS users, changing the voice may throw a `KeyError`. 
    To fix this, update `_toVoice` in `nsss.py` to:
    ```
    @objc.python_method
    def _toVoice(self, attr):
        try:
            lang = attr['VoiceLocaleIdentifier']
            age = attr['VoiceAge']
        except KeyError:
            lang = attr['VoiceLanguage']
            age = None
        return Voice(attr['VoiceIdentifier'], attr['VoiceName'],
                     [lang], attr['VoiceGender'],
                     age)
    ```
    '''
    voices = engine.getProperty('voices')
    '''
    Adjust the index of `voices` to change language/gender/voice depending on OS
    `voices[22] on Linux systems is Finnish```
    '''
    engine.setProperty('voice', voices[22].id)  # voices[6].id)
    for line in text:
        engine.say(line)
    engine.runAndWait()


def mms():
    """
    Download the Meta language model.
    For MacOS/Linux users: curl https://dl.fbaipublicfiles.com/mms/tts/lang_code.tar.gz --output lang_code.tar.gz
    Replace "lang_code" in the url and tar with the language code for your language. E.g., eng for English

    Extract the tar ball.
    For MacOS/Linux users: mkdir -p data && tar -xzf lang_code.tar.gz -C data/
    Replace "lang_code" with the language used above.

    Requires the following libraries: ttsmms, sounddevice
    """
    rawText = list(filter(lambda x: x != "", Path('text.txt').read_text().split('\n')))
    text = " ".join(rawText).lower()
    tts = TTS("data/fin")
    wav = tts.synthesis(text, wav_path="output.wav")
    data, fs = sf.read(wav, dtype='float32')
    sd.play(data, fs)
    status = sd.wait()


if __name__ == "__main__":
    # run()
    mms()
