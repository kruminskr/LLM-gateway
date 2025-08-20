# model logic here (API calls)

# local ONNX model 
def getDataONNX():
    # call a self hosted API that uses ONNX model
    return {"message": "Success"}

# Cloud API - groq
def getDataGroq():
    # call groq API
    return {"message": "Success"}

# Cloud API - HuggingFace
def getDataHuggingFace():
    # call HuggingFace API
    return {"message": "Success"}