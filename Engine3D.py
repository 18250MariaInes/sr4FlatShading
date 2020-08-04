"""
Maria Ines Vasquez Figueroa
18250
Gráficas
SR4 Flat Shading
Main
"""

from gl import Render
from obj import Obj

#valores con los que se inicializan la ventana y viewport

width=1920
height=1080

#creacion de Window

r = Render(width,height)
#r.loadModel('./models/face.obj', (960,300,0), (15,15,15))
r.loadModel('./models/objBarrel.obj', (960,300,0), (400,400,400))
#r.loadModel('./models/model.obj', (960,300,0), (400,400,400))

r.glFinish('output.bmp')
r.glZBuffer('zbuffer.bmp')





