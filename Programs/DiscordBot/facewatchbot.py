# This example requires the 'members' privileged intents
#!! Lines 20 and 145 require input of firebase key and discord bot auth key respectively. Without these, this will not work.

import shutil
import requests
import discord
from discord.ext import commands
import discord
from dotenv import load_dotenv
import time

#Facial Recognition Imports
import face_recognition
import cv2
import numpy as np
import firebase_admin
from firebase_admin import credentials
from sqlalchemy import false

cred = credentials.Certificate('/path/to/firebase/key')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://faces-c07d3-default-rtdb.firebaseio.com'})

from firebase_admin import db

load_dotenv()

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

class client(discord.Client):
    async def startup(self):
        await self.wait_until_ready()
        await tree.sync()
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
@bot.command()
async def echoimage(ctx):
    try:
        url = ctx.message.attachments[0].url
    except IndexError:
        print('No attachments')
        await ctx.send('No attachments')
    else:
        if url[0:26] == "https://cdn.discordapp.com":
            r = requests.get(url, stream=True)
            filename = str(int(time.time())) + '.png'
            with open(filename, 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
            

            imagefile = str(filename)
            image = cv2.imread(imagefile)
            imcap = face_recognition.load_image_file(imagefile)

            

            Faces = [] #A constant, list of all of the face names
            known_faces = []
            face_locations = []
            face_names = []

            await ctx.send('Please wait... I\'m setting things up right now...')

            ref = db.reference("/")
            data = ref.get() or []

            def name_function():
                for name in data:
                    ref = db.reference("/" + name)
                    codes = ref.get()
                    for discriminator in codes:
                        encoding = []
                        ref = db.reference("/" + name + "/" + str(discriminator))
                        code = ref.get()
                        for number in code:
                            encoding.append(number)
                        known_faces.append(np.array(encoding))
                        Faces.append(name)
            name_function()


            def EncodeFace(input, Encoding):
                # send data to firebase
                if input == "":
                    return
                ref = db.reference("/" + input + "/")
                print(input)
                ref.set({"Encoding": Encoding.tolist()})

                known_faces.append(Encoding)
                Faces.append(input)

            def CompareFaces(tol):
                match = face_recognition.api.compare_faces(known_faces, face_encoding, tolerance=tol)
                name = "Unknown"
                face_distances = face_recognition.api.face_distance(known_faces, face_encoding)
                best_match_index = np.argmin(face_distances)
                if match[best_match_index]:
                    name = Faces[best_match_index]
                return name

            print("Alright, I'm generating the output!")

            #Reads the current video capture, and sets it to RGB format
            faces_found = []

            face_locations = face_recognition.api.face_locations(imcap) 
            face_encodings = face_recognition.api.face_encodings(imcap, face_locations)

            face_names=[]
            for face_encoding in face_encodings:
                name = CompareFaces(0.35)
                print(name)
                if name == "Unknown":
                    name = CompareFaces(0.55)
                    print(name)
                face_names.append(name) #face_names will be the names of the faces currently detected
                faces_found.append(face_encoding)

            for (top, right, bottom, left), name, face_encodings in zip(face_locations, face_names, faces_found):
                boxColor = (0,255,0)
                if name == "Unknown":
                    boxColor = (0,0,255)

                cv2.rectangle(image, (left, top), (right, bottom), (boxColor), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(image, name, (left + 6, bottom + 32), font, 1.0, (0, 255, 0), 1)

            cv2.imwrite('output.png', image)
            e = discord.Embed(title=('Here you go!'),color=0xFF5733)
            output = discord.File("output.png", filename="output.png")
            e.set_image(url="attachment://output.png")
            await ctx.send(file=output, embed=e) 

bot.run('######################################')