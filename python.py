import replicate
from environs import Env
import openai
from chronological import read_prompt, cleaned_completion, main

env = Env()
env.read_env()

# model = replicate.models.get("prompthero/openjourney")
# version = model.versions.get("9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb")
# output = version.predict(prompt="mdjrny-v4 style a highly detailed matte painting of a man on a hill watching a rocket launch in the distance by studio ghibli, makoto shinkai, by artgerm, by wlop, by greg rutkowski, volumetric lighting, octane render, 4 k resolution, trending on artstation, masterpiece")
print (replicate.predictions.list()[-1].output[0])

# openai.api_key = env("OPEN_API_TOKEN")

# configuration = {
#   "model": "text-davinci-002",
#   "prompt": "Story about Taco Science",
#   "temperature": 0.7,
#   "max_tokens": 256,
#   "top_p": 1,
#   "frequency_penalty": 0,
#   "presence_penalty": 0
# }

# response = openai.Completion.create(
#   model = configuration["model"],
#   prompt= configuration["prompt"],
#   temperature = configuration["temperature"],
#   max_tokens = configuration["max_tokens"],
#   top_p = configuration["top_p"],
#   frequency_penalty = configuration["frequency_penalty"],
#   presence_penalty = configuration["presence_penalty"]
# )

# # response.choices[0].text
# print(response.choices[0].text)