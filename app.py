from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import time
import replicate
import openai
import random
from environs import Env

env = Env()
env.read_env()

openai.api_key = env("OPEN_API_TOKEN")
openAI_configuration = {
  "model": "text-davinci-003",
  "prompt": "Story about Taco Science",
  "temperature": 0.7,
  "max_tokens": 512,
  "top_p": 1,
  "frequency_penalty": 0.5,
  "presence_penalty": 1.5 
}

app = Flask(__name__)
socketio = SocketIO(app)

passage = ""
passageList = []
passagePrompt = ""
title = ""
imagePrompt = ""
imageUrls = []

@app.route('/')
def hello():
    return render_template("home.html", data="Null")

@socketio.on('generateContent')
def generateContent(input):
    time.sleep(1)
    global passagePrompt 
    global openAI_configuration
    global passage

    passagePrompt = input["data"]
    if passage != "":
        openAI_configuration["prompt"] =  passage + " Continue the story with a story arc: " + passagePrompt
    else:
        openAI_configuration["prompt"] =  "Write a complete story, with a problem and solution about: " + passagePrompt

    response = openai.Completion.create(
        model = openAI_configuration["model"],
        prompt = openAI_configuration["prompt"],
        temperature = openAI_configuration["temperature"],
        max_tokens = openAI_configuration["max_tokens"],
        top_p = openAI_configuration["top_p"],
        frequency_penalty = openAI_configuration["frequency_penalty"],
        presence_penalty = openAI_configuration["presence_penalty"]
    )

    if (response["choices"][0].text) == "":
        passageList.append("The End.")
    else:
        if (passage == ""):
            passageList.append(response["choices"][0].text)
        else:
            passageList.append(passagePrompt + response["choices"][0].text)

    passage = passage + "\n" + passageList[-1] + "\n"

    response = openai.Completion.create(
        model = openAI_configuration["model"],
        prompt = "summarize the essay into one sentence: " + passageList[-1],
        temperature = openAI_configuration["temperature"],
        max_tokens = openAI_configuration["max_tokens"],
        top_p = openAI_configuration["top_p"],
        frequency_penalty = openAI_configuration["frequency_penalty"],
        presence_penalty = openAI_configuration["presence_penalty"]
    )

    imagePrompt = "mdjrny-v4 style" + response["choices"][0].text

    model = replicate.models.get("prompthero/openjourney")
    # model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb")
    # version = model.versions.get("6359a0cab3ca6e4d3320c33d79096161208e9024d174b2311e5a21b6c7e1131c")
    version.predict(prompt=imagePrompt)

    imageUrls.append(replicate.predictions.list()[0].output[0])

    emit('processing-finished', {"prompt": passagePrompt, "content": passageList[-1], "image": replicate.predictions.list()[0].output[0]})

@socketio.on('endContent')
def endContent(input):
    time.sleep(1)
    global passagePrompt 
    global openAI_configuration
    global passage

    response = openai.Completion.create(
        model = openAI_configuration["model"],
        prompt = "Generate a title for the following story:" + passage,
        temperature = openAI_configuration["temperature"],
        max_tokens = openAI_configuration["max_tokens"],
        top_p = openAI_configuration["top_p"],
        frequency_penalty = openAI_configuration["frequency_penalty"],
        presence_penalty = openAI_configuration["presence_penalty"]
    )
    image_styles_list = ["Stained glass", "Blackboard", "Crayon", "Calligraphy", "Graphite", "Noir line art", "Cinematic", "ZBrush", "Airbrush", "Caricature", "Origami", "Blueprint", "Drypoint", "Minimalist", "Tarot card", "Chalk", "Psychedelic", "Labor poster", "Ancient greece", "8 Bit", "Marble", "Neon", "Kaleidoscope", "Gold", "Splatter", "Wet paint", "Pop art", "Monochrome", "Line drawing", "Cyberpunk", "Ghibli", "Oil painting", "Sketch", "Spray paint", "Cubism", "Cyanotype", "Drawing", "Pixar", "Manga"]
    image_style = random.choice(image_styles_list)

    imagePrompt = "landscape, " + image_style + " styled, intricate, highly detailed, smooth, sharp focus, 8k" + response["choices"][0].text
    
    model = replicate.models.get("prompthero/openjourney")
    # model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb")
    # version = model.versions.get("6359a0cab3ca6e4d3320c33d79096161208e9024d174b2311e5a21b6c7e1131c")
    version.predict(prompt=imagePrompt)

    emit('end-finished', {"title": response["choices"][0].text, "image": replicate.predictions.list()[0].output[0]})
    pass

if __name__ == "__main__":
    # app.run(debug=True)
    socketio.run(app)
    