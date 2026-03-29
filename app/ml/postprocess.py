import numpy as np

def postprocess(prediction):
    mask = prediction[0]  # remove batch dim

    # If model outputs probabilities
    mask = (mask > 0.5).astype(np.uint8)

    return mask