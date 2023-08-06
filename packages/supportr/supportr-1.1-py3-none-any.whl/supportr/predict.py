from .supportr import Supportr

sr = None

def predict(text):
    global sr
    if sr is None:
        try:
            sr = Supportr()
        except Exception as e:
            print("Failed to initialize Supportr")
            print(e)

    return sr.predict(text)