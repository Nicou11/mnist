import os

def get_keras_path():
    f = os.path.abspath(__file__)
    dir_name = os.path.dirname(f)
    model_path = os.path.join(dir_name, f"mnist240924.keras")
    return model_path

