from pyttsx3 import init


def speak(string: str):
    engine = init()
    engine.say(string)
    engine.runAndWait()

    return True
