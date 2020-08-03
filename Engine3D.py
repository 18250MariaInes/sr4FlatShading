"""
Maria Ines Vasquez Figueroa
18250
Gráficas
SR3 ObjModel
Main
"""

from gl import Render
from obj import Obj

#valores con los que se inicializan la ventana y viewport

width=1920
height=1080

#creacion de Window

r = Render(width,height)
r.loadModel('./models/objBarrel.obj', (960,300,0), (400,400,400))
r.glFinish('output.bmp')

##IGNORAR DESDE AQUI
##codigo de laboratorios pasados modificado para correcion de funciones
"""
#creacion del viewport
#r.glViewPort(posX, posY, width - width/2 , height - height/2)

#cambio de color con el que se hará el punto con parametros de 0-1 para r, g, b
r.glColor(1,0,0)


#dibujo de estrella verde
r.glColor(0,1,0)
##algoritmo para dibujar linea modificado en base al algoritmo de Bersenham extraido de : https://www.geeksforgeeks.org/bresenhams-line-generation-algorithm/
r.glLine(-1, -1, 0,1)
r.glLine(0, 1,1, -1)
r.glLine(1, -1, -1,0.5)
r.glLine(-1, 0.5, 1,0.5)
r.glLine(1, 0.5, -1,-1)

#asterisco desde el centro rojo
r.glColor(1,0,0)
r.glLine(0, 0, 0,1)
r.glLine(0, 0, 0,-1)
r.glLine(0, 0, 1,1)
r.glLine(0, 0, -1,-1)
r.glLine(0, 0, -1,1)
r.glLine(0, 0, 1,-1)
r.glLine(0, 0, -1,0)
r.glLine(0, 0, 1,0)
r.glLine(0, 0, -0.5,1)
r.glLine(0, 0, 0.5,1)
r.glLine(0, 0, -0.5,-1)
r.glLine(0, 0, 0.5,-1)
r.glLine(0, 0, 1, 0.5)
r.glLine(0, 0, -1, 0.5)
r.glLine(0, 0, 1, -0.5)
r.glLine(0, 0, -1, -0.5)

#con este algoritmo puede dibujar desde cualquier angulo de derecha a izquierda y viceversa
#diagonales azules pero de esquina a esquina, no desde el centro
#comentar para ver todo el asterisco anterior
r.glColor(0,0,1)
r.glLine(-1, -1, 1, 1)
r.glLine(1, -1, -1, 1)
r.glLine(1, 0.5, -1, -0.5)
r.glLine(-1, 0.5, 1, -0.5)


r.glFinish('output.bmp')"""



