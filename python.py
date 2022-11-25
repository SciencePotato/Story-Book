import replicate
from environs import Env

env = Env()
env.read_env()

# model = replicate.models.get("prompthero/openjourney")
# version = model.versions.get("9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb")
# output = version.predict(prompt="mdjrny-v4 style a highly detailed matte painting of a man on a hill watching a rocket launch in the distance by studio ghibli, makoto shinkai, by artgerm, by wlop, by greg rutkowski, volumetric lighting, octane render, 4 k resolution, trending on artstation, masterpiece")
# print (replicate.predictions.list())

print (env("GITHUB"))