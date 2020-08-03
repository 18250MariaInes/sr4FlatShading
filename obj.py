"""
Maria Ines Vasquez Figueroa
18250
Gráficas
SR3 ObjModel
Carga OBJ
"""
#Carga de archivo OBJ

class Obj(object):
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.lines=file.read().splitlines()
        #clasificaciones de datos dentro de archivo OBJ
        self.vertices=[]
        self.normals=[]
        self.texcoords=[]
        self.faces=[]

        self.read()
        #print(self.vertices)
        """for face in self.faces:
            print(face)"""
        #print("-----------------------------------------------------------------------")

    def read(self):#funcion para leer lineas de archivo OBJ y asi clasificarlo
        for line in self.lines:
            #print(line.split(' ',1))
            if line: #clasificacion de lineas en txt entre vertices, normales, textcoords y cara de modelo 3D
                prefix,value=line.split(' ',1)
                if prefix == 'v': # vertices
                    self.vertices.append(list(map(float,value.split(' '))))
                elif prefix == 'vn': #normales
                    self.normals.append(list(map(float,value.split(' '))))
                elif prefix == 'vt': #textcoords
                    self.texcoords.append(list(map(float,value.split(' '))))
                elif prefix == 'f': #faces XX/YY/ZZ
                    self.faces.append([list(map(int,vert.split('/'))) for vert in value.split(' ')])




        

