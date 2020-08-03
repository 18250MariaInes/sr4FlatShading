"""
Maria Ines Vasquez Figueroa
18250
Gráficas
SR3 ObjModel
Funciones
"""
import struct
from obj import Obj
import random
import numpy as np
from collections import namedtuple

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z','w'])

def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # 2 bytes
    return struct.pack('=h',w)

def dword(d):
    # 4 bytes
    return struct.pack('=l',d)

def color(r, g, b):
    #return bytes([b, g, r])
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

def baryCoords(Ax, Bx, Cx, Ay, By, Cy, Px, Py):
    # u es para la A, v es para B, w para C
    try:
        u = ( ((By - Cy)*(Px - Cx) + (Cx - Bx)*(Py - Cy) ) /
              ((By - Cy)*(Ax - Cx) + (Cx - Bx)*(Ay - Cy)) )

        v = ( ((Cy - Ay)*(Px - Cx) + (Ax - Cx)*(Py - Cy) ) /
              ((By - Cy)*(Ax - Cx) + (Cx - Bx)*(Ay - Cy)) )

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w


BLACK = color(0,0,0)
WHITE = color(1,1,1)

class Render(object):
    def __init__(self, width, height): #funncion que actua como el glInit
        #self.glInit(width, height)
        self.curr_color = WHITE
        self.curr_color_bg=BLACK
        self.glCreateWindow(width, height)

    #Inicializa objetos internos
    def glInit(self, width, height):
        #esto se establece ahora en la funcion glCreatWindow
        """self.width = width
        self.height = height"""
        self.curr_color = WHITE
        self.curr_color_bg=BLACK
        self.glCreateWindow(width, height)
        """self.glClearColor(red, green, blue)
        self.glClear()"""

    #inicializa framebuffer
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewPort(0, 0, width, height)

    #define area de dibujo
    def glViewPort(self, x, y, width, height):
        self.vportwidth = width
        self.vportheight = height
        self.vportx = x
        self.vporty = y

    #cambia el color con el que se llena el mapa de bits (fondo)
    def glClearColor(self, red, green, blue):
        nred=int(255*red)
        ngreen=int(255*green)
        nblue=int(255*blue)
        self.curr_color_bg = color(nred, ngreen, nblue)

    #llena el mapa de bits de un solo color predeterminado antes
    def glClear(self):
        self.pixels = [ [ self.curr_color_bg for x in range(self.width)] for y in range(self.height) ]
        #Z - buffer, depthbuffer, buffer de profudidad
        self.zbuffer = [ [ -float('inf') for x in range(self.width)] for y in range(self.height) ]

    
    #dibuja el punto en relación al viewport
    def glVertex(self, x, y):
        nx=int((x+1)*(self.vportwidth/2)+self.vportx)
        ny=int((y+1)*(self.vportheight/2)+self.vporty)
        try:
            self.pixels[ny][nx] = self.curr_color
        except:
            pass
    
    #cambia de color con el que se hará el punto con parametros de 0-1
    def glColor(self, red, green, blue):
        nred=int(255*red)
        ngreen=int(255*green)
        nblue=int(255*blue)
        self.curr_color = color(nred, ngreen, nblue)
    
    def glVertex_coord(self, x,y, color = None):#helper para dibujar puntas en la funcion de glLine, 
    #ahora mejorado para solo dibujar cuando no hay nada abajo ya dibujado, más eficiente
        try:
            if (self.pixels[y][x]!=self.curr_color and self.pixels[y][x]!=color):
                self.pixels[y][x] = color or self.curr_color
            else:
                pass
        except:
            pass


    #escribe el archivo de dibujo
    def glFinish(self, filename):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        #f.write(char('B'))
        #f.write(char('M'))

        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))

        archivo.write(dword(14 + 40 + self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.width))
        archivo.write(dword(self.height))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        # Pixeles, 3 bytes cada uno

        for x in range(self.height):
            for y in range(self.width):
                archivo.write(self.pixels[x][y])


        archivo.close()

    def glLine(self, x0, y0, x1, y1): #algoritmo de clase modificado por mi en base al algoritmo de Bersenham extraido de : https://www.geeksforgeeks.org/bresenhams-line-generation-algorithm/
        x0 = int(( x0 + 1) * (self.vportwidth / 2 ) + self.vportx)
        x1 = int(( x1 + 1) * (self.vportwidth / 2 ) + self.vportx)
        y0 = int(( y0 + 1) * (self.vportheight / 2 ) + self.vporty)
        y1 = int(( y1 + 1) * (self.vportheight / 2 ) + self.vporty)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        inc = dy > dx

        if inc:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        limit = 0.5
    
        #a diferencia del visto en clase, el algoritmo consultado inicializa m como 2 veces el diferencial en y 
        #y offset como la resta entre la pendiente m y 2 veces el diferencial en x
        m=2*(dy)
        offset=m-2*dx
        y = y0
        for x in range(x0, x1 + 1):
            if inc:
                self.glVertex_coord(y, x)
            else:
                self.glVertex_coord(x, y)
            offset += m
            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y-=1
                limit += 1
                #igualmente cuando offset es mayor o igual que el limite 0.5, se le resta 2 veces el diferencial en x
                offset-=2*dx
    
    def glLine_c(self, x0, y0, x1, y1):#algoritmo realizado con Carlos en clase, lo mantengo como comparacion y el resultado es muy similar al desarrollado por mi
        x0 = int(( x0 + 1) * (self.vportwidth / 2 ) + self.vportx)
        x1 = int(( x1 + 1) * (self.vportwidth / 2 ) + self.vportx)
        y0 = int(( y0 + 1) * (self.vportheight / 2 ) + self.vporty)
        y1 = int(( y1 + 1) * (self.vportheight / 2 ) + self.vporty)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        inc = dy > dx

        if inc:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5
        m = dy/dx
        y = y0
        for x in range(x0, x1 + 1):
            if inc:
                self.glVertex_coord(y, x)
            else:
                self.glVertex_coord(x, y)
            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1

    def glLine_coord(self, x0, y0, x1, y1): #window coordinates en base a mi algoritmo realizado, no da problema con division con cero
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        inc = dy > dx

        if inc:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        limit = 0.5
    
        #a diferencia del visto en clase, el algoritmo consultado inicializa m como 2 veces el diferencial en y 
        #y offset como la resta entre la pendiente m y 2 veces el diferencial en x
        
        m=2*dy
    
        y = y0
        
        offset=m-2*dx
        for x in range(x0, x1 + 1):
            if inc:
                self.glVertex_coord(y, x)
            else:
                self.glVertex_coord(x, y)
            offset += m
            if offset >= limit:
                if y0 < y1:
                    y += 1
                else:
                    y-=1
                limit += 1
                #igualmente cuando offset es mayor o igual que el limite 0.5, se le resta 2 veces el diferencial en x
                offset-=2*dx

    #Barycentric Coordinates
    def triangle_bc(self, Ax, Bx, Cx, Ay, By, Cy, Az, Bz, Cz, color = None):
        #bounding box
        minX = min(Ax, Bx, Cx)
        minY = min(Ay, By, Cy)
        maxX = max(Ax, Bx, Cx)
        maxY = max(Ay, By, Cy)

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                u, v, w = baryCoords(Ax, Bx, Cx, Ay, By, Cy, x,y)

                if u >= 0 and v >= 0 and w >= 0:

                    z = Az * u + Bz * v + Cz * w

                    if z > self.zbuffer[y][x]:
                        self.glVertex_coord(x, y, color)
                        self.zbuffer[y][x] = z
    def subtract(self, x0, x1, y0, y1, z0, z1):
        res=[]
        res.append(x0-x1)
        res.append(y0-y1)
        res.append(z0-z1)
        return res
    
    def cross(self, v0, v1):
        res=[]
        res.append(v0[1]*v1[2]-v1[1]*v0[2])
        res.append(-(v0[0]*v1[2]-v1[0]*v0[2]))
        res.append(v0[0]*v1[1]-v1[0]*v0[1])
        return res

    def frobenius(self, norm):
        return((norm[0]**2+norm[1]**2+norm[2]**2)**(1/2))

    def division(self, norm, frobenius):
        if (frobenius==0):
            res=[]
            res.append(float('NaN'))
            res.append(float('NaN'))
            res.append(float('NaN'))
            return res
            #return float('NaN')
        else:
            res=[]
            res.append(norm[0]/ frobenius)
            res.append(norm[1]/ frobenius)
            res.append(norm[2]/ frobenius)
            return res

    def loadModel(self, filename, translate, scale, isWireframe = False): #funcion para crear modelo Obj
        model = Obj(filename)
        lightx=0
        lighty=0
        lightz=1

        light=V3(lightx, lighty, lightz)
        for face in model.faces:
            vertCount = len(face) #conexion entre vertices para crear Wireframe
            if isWireframe:
                for vert in range(vertCount):
                    v0 = model.vertices[ face[vert][0] - 1 ]
                    v1 = model.vertices[ face[(vert + 1) % vertCount][0] - 1]
                    #coordenadas para dibujar linea con escala y traslacion setteado
                    x0 = int(v0[0] * scale[0]  + translate[0])
                    y0 = int(v0[1] * scale[1]  + translate[1])
                    x1 = int(v1[0] * scale[0]  + translate[0])
                    y1 = int(v1[1] * scale[1]  + translate[1])

                    #self.glVertex_coord(x0, y0)
                    
                    self.glLine_coord(x0, y0, x1, y1)
            else:
                v0 = model.vertices[ face[0][0] - 1 ]
                v1 = model.vertices[ face[1][0] - 1 ]
                v2 = model.vertices[ face[2][0] - 1 ]

                x0 = int(v0[0] * scale[0]  + translate[0])
                y0 = int(v0[1] * scale[1]  + translate[1])
                z0 = int(v0[2] * scale[2]  + translate[2])
                x1 = int(v1[0] * scale[0]  + translate[0])
                y1 = int(v1[1] * scale[1]  + translate[1])
                z1 = int(v1[2] * scale[2]  + translate[2])
                x2 = int(v2[0] * scale[0]  + translate[0])
                y2 = int(v2[1] * scale[1]  + translate[1])
                z2 = int(v2[2] * scale[2]  + translate[2])

                ##cambiar esta parte de mi por matematica propia
                v0=V3(x0, y0, z0)
                v1=V3(x1, y1, z1)
                v2=V3(x2, y2, z2)
                """print("------------SUBSTRACT----------------------")
                print(v1)
                print(v0)
                print(np.subtract(v1,v0))
                print(self.subtract(x1, x0, y1, y0, z1, z0))
                print("------------CROSS----------------------")
                print(np.cross(np.subtract(v1,v0), np.subtract(v2,v0)))
                print(self.cross(self.subtract(x1, x0, y1, y0, z1, z0), self.subtract(x2, x0, y2, y0, z2, z0)))"""



                normal = np.cross(np.subtract(v1,v0), np.subtract(v2,v0))
                #print(normal)
                """print("-------------------Frobenius---------------------")
                print(np.linalg.norm(normal)) 
                print(self.frobenius(self.cross(self.subtract(x1, x0, y1, y0, z1, z0), self.subtract(x2, x0, y2, y0, z2, z0))))"""
                print("-----------normal------------")
                print(normal / np.linalg.norm(normal))
                #print((self.cross(self.subtract(x1, x0, y1, y0, z1, z0), self.subtract(x2, x0, y2, y0, z2, z0)))/(self.frobenius(self.cross(self.subtract(x1, x0, y1, y0, z1, z0), self.subtract(x2, x0, y2, y0, z2, z0)))))
                print(self.division(self.cross(self.subtract(x1, x0, y1, y0, z1, z0), self.subtract(x2, x0, y2, y0, z2, z0)),self.frobenius(self.cross(self.subtract(x1, x0, y1, y0, z1, z0), self.subtract(x2, x0, y2, y0, z2, z0))) ))
                normal = normal / np.linalg.norm(normal)
                intensity = np.dot(normal, light)

                if intensity >=0:
                    self.triangle_bc(x0,x1,x2, y0, y1, y2, z0, z1, z2, color(intensity, intensity, intensity))
                
                if vertCount > 3: #asumamos que 4, un cuadrado
                    v3 = model.vertices[ face[3][0] - 1 ]
                    x3 = int(v3[0] * scale[0]  + translate[0])
                    y3 = int(v3[1] * scale[1]  + translate[1])
                    z3 = int(v3[2] * scale[2]  + translate[2])

                    if intensity >=0:
                        self.triangle_bc(x0,x2,x3, y0, y2,y3, z0, z2,z3, color(intensity, intensity, intensity))


           
                
                
                

                











