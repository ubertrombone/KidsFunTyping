from pathlib import Path
import pyttsx3


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
    `voices[24] on Linux systems is Finnish```
    '''
    engine.setProperty('voice', voices[9].id)
    for line in text:
        engine.say(line)
    engine.runAndWait()


if __name__ == "__main__":
    run()
