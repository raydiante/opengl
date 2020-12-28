'''
Rayssa Rosa
Trabalho final de Computação grafica

Instruções:
Faça um programa de visualização de objetos 3D usando OpenGL com as eguintes características:
Possobilidade de visualização em wireframe e solid, com modelo de iluminação habilitando luzes, ou flat, transformações geométricas básicas (rotações, translações e mudança de escala), recursos para troca de cores. Desejável que tenha ainda: zoom, marcar como selecionado, desmarcar seleção, agrupar objetos na seleção e desagrupar objetos.
'''

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

w, h = 500,500
wMenu, hMenu = 200,200

VERMELHO=[1,0,0]
AZUL=[0,0,1]
VERDE=[0,1,0]
ROSA=[1,0.0,1]
LARANJA=[1,0.5,0]
AMARELO=[1, 1, 0.0]
BRANCO=[1,1,1]

ZOOM=1
REDISPLAY=True
WIRE=False
SELECIONA=False
CORATUAL=VERMELHO
ROTATE=False
LUZES=True


OBJETOSDESENHO=[]
OBJETOSMENU=[]
OBJETOSSELECIONADOS=[]

  
       

#---------------------------------
#-------------SELEÇAO DE OBJETOS
#---------------------------------
def normalizaCoordenada(x,y,w,h):# Transforma coordanadas baseadas no centro da tela para coordenadas baseadas no canto direito na tela
	xNovo=w/2 + (x*(w/2))
	yNovo=h/2 - (y*(h/2))
	return xNovo,yNovo
def normalizaCoordenada2(x,y,w,h):# Transforma coordanadas baseadas no centro da tela para coordenadas baseadas no canto direito na tela
	xNovo=w/2 + (x*(w/3))
	yNovo=h/2 - (y*(h/3))
	return xNovo,yNovo

def adicionaOBJ(tipo,centroX,centroY,raio,escala,rotx,rotax,roty,rotay,cor,wire):
	global OBJETOSDESENHO
	novoOBJ=[tipo,centroX,centroY,raio,escala,rotx,rotax,roty,rotay,cor,wire]
	OBJETOSDESENHO.append(novoOBJ)

def limpaOBJ():
	global OBJETOSDESENHO,OBJETOSSELECIONADOS
	OBJETOSDESENHO=[]
	OBJETOSSELECIONADOS=[]

#---------------------------------
#-------------CALLBACK
#---------------------------------


def clickMenu(button,state,x, y):
	global WIRE,OBJETOSMENU,OBJETOSSELECIONADOS,OBJETOSDESENHO,VERMELHO,AZUL,VERDE,ROSA,LARANJA,BRANCO,AMARELO
	#print(OBJETOSMENU)
	#button=0 state=0 } click botao esquerdo
	if state == 0:
		#print("Mouse click ", x,' - ', y,' - ',  button,' - ', state)

		for obj in OBJETOSMENU:
			distancia=math.sqrt(((x-obj[0])*(x-obj[0])) + ((y-obj[1])*(y-obj[1])))

			if (distancia<(obj[2]*(wMenu/2))):

				print("Clicou em ",obj[3])

				glMatrixMode(GL_MODELVIEW)
				glPushMatrix()

				if obj[3] == "Teapot":
					adicionaOBJ("Teapot",0,0,0.11,1,False,False,False,False,AMARELO,False)
				if obj[3] == "Sphere":
					adicionaOBJ("Sphere",0,0,0.11,1,False,False,False,False,AMARELO,False)
				if obj[3] == "Cube":
					adicionaOBJ("Cube",0,0,0.11,1,False,False,False,False,AMARELO,False)
				if obj[3] == "Donut":
					adicionaOBJ("Donut",0,0,0.15,1,False,False,False,False,AMARELO,False)

				if obj[3] == "VERMELHO" and len(OBJETOSSELECIONADOS)>0:
					for i in OBJETOSSELECIONADOS:
						OBJETOSDESENHO[i][9]=VERMELHO
				if obj[3] == "AZUL" and len(OBJETOSSELECIONADOS)>0:
					for i in OBJETOSSELECIONADOS:
						OBJETOSDESENHO[i][9]=AZUL
				if obj[3] == "VERDE" and len(OBJETOSSELECIONADOS)>0:
					for i in OBJETOSSELECIONADOS:
						OBJETOSDESENHO[i][9]=VERDE
				if obj[3] == "ROSA" and len(OBJETOSSELECIONADOS)>0:
					for i in OBJETOSSELECIONADOS:
						OBJETOSDESENHO[i][9]=ROSA
				if obj[3] == "AMARELO" and len(OBJETOSSELECIONADOS)>0:
					for i in OBJETOSSELECIONADOS:
						OBJETOSDESENHO[i][9]=AMARELO
				if obj[3] == "LARANJA" and len(OBJETOSSELECIONADOS)>0:
					for i in OBJETOSSELECIONADOS:
						OBJETOSDESENHO[i][9]=LARANJA

				glPopMatrix()
				glFlush()


	#glutPostRedisplay()


def clickDesenha(button,state,x, y):
	global SELECIONA,OBJETOSDESENHO,OBJETOSSELECIONADOS
	#print(OBJETOSDESENHO)
	#button=0 state=0 } click botao esquerdo
	if state == 0:
		#print("Mouse click ", x,' - ', y,' - ',  button,' - ', state)
		#print(OBJETOSDESENHO)

		for idx,obj in enumerate(OBJETOSDESENHO):
			#print(idx,'-',obj[0])
			xobj=obj[1]
			yobj=obj[2]
			xobj,yobj=normalizaCoordenada2(xobj,yobj,w,h)
			distancia=math.sqrt(((x-xobj)*(x-xobj)) + ((y-yobj)*(y-yobj)))
			raio=(obj[3]*(w/2))
			if obj[0] == "Cube":
				raio=raio/2

			#print(xobj,'-',yobj,'-',distancia,'-',raio)

			if (distancia<raio):
				print("Clicou em ",obj[0])
				if SELECIONA == True:
					print("SELECIONOU  ",obj[0], " - ",idx)
					if idx not in OBJETOSSELECIONADOS:
						OBJETOSSELECIONADOS.append(idx)



def keyboard(bkey, x, y):
	global ROTATE,LUZES,WIRE,SELECIONA,OBJETOSSELECIONADOS,OBJETOSDESENHO,ZOOM
	# Convert bytes object to string 
	key = bkey.decode("utf-8")
	#print(key)
	# Allow to quit by pressing 'Esc' or 'q'
	if key == chr(27):
		sys.exit()
	if key == 'q':
		sys.exit()


	if key == 'r' or key == 'R':
		ROTATE=True
	if (key == 'a' or key == 'A') and ROTATE == True :
		for i in OBJETOSSELECIONADOS:
			OBJETOSDESENHO[i][8]-=10
			OBJETOSDESENHO[i][7]=1
	if (key == 'd' or key == 'D') and ROTATE == True :
		for i in OBJETOSSELECIONADOS:
			OBJETOSDESENHO[i][8]+=10
			OBJETOSDESENHO[i][7]=1
	if (key == 'w' or key == 'W') and ROTATE == True :
		for i in OBJETOSSELECIONADOS:
			OBJETOSDESENHO[i][6]-=10
			OBJETOSDESENHO[i][5]=1
	if (key == 's' or key == 'S') and ROTATE == True :
		for i in OBJETOSSELECIONADOS:
			OBJETOSDESENHO[i][6]+=10
			OBJETOSDESENHO[i][5]=1
	if (key == '+') :
		for i in OBJETOSSELECIONADOS:
			#OBJETOSDESENHO[i][4]+=0.2
			OBJETOSDESENHO[i][3]+=0.05
	if (key == '-') :
		for i in OBJETOSSELECIONADOS:
			#OBJETOSDESENHO[i][4]-=0.2
			OBJETOSDESENHO[i][3]-=0.05
	if (key == 'l' or key == 'L') :
		if LUZES == True:
			LUZES=False
			disable()
		else:
			LUZES=True
			enable()
	if (key == 'w' or key == 'W') and ROTATE == False :
		for i in OBJETOSSELECIONADOS:
			if OBJETOSDESENHO[i][10] == True:
				OBJETOSDESENHO[i][10]=False
			else:
				OBJETOSDESENHO[i][10]=True
	if (key == 's' or key == 'S') and ROTATE == False :
		if SELECIONA == True:
			print("SELECIONA DESATIVADO")
			SELECIONA=False
			OBJETOSSELECIONADOS=[]
		else:
			print("SELECIONA ATIVADO")
			OBJETOSSELECIONADOS=[]
			SELECIONA=True
	if key == 'c' or key == 'C':
		limpaOBJ()
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Remove everything from screen (i.e. displays all white)
		glLoadIdentity() # Reset all graphic/shape's position

	if (key == 'z' or key == 'Z') :
		ZOOM+=0.5
	if (key == 'x' or key == 'X') :
		ZOOM-=0.5



	glutPostRedisplay()



def keyboardUp(bkey, x, y):
	global ROTATE,ROTX,ROTY
	key = bkey.decode("utf-8")
	if key == 'r' or key == 'R':
		ROTATE=False


def specialKey( key, x,y): 
	global OBJETOSSELECIONADOS,OBJETOSDESENHO
	if key == GLUT_KEY_LEFT: 
		for i in OBJETOSSELECIONADOS:
			OBJETOSDESENHO[i][1]-=0.1
	if key ==  GLUT_KEY_RIGHT: 
		for i in OBJETOSSELECIONADOS:
			OBJETOSDESENHO[i][1]+= 0.1
	if key == GLUT_KEY_UP: 
		for i in OBJETOSSELECIONADOS:
			OBJETOSDESENHO[i][2]+= 0.1
	if key ==  GLUT_KEY_DOWN: 
		for i in OBJETOSSELECIONADOS:
			OBJETOSDESENHO[i][2]-= 0.1
	glutPostRedisplay()

#---------------------------------
#-------------TELA DESENHO
#---------------------------------

def disable():
	glDisable(GL_LIGHTING)
	glDisable(GL_LIGHT0)
	glDisable(GL_DEPTH_TEST)

def enable():
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_DEPTH_TEST)

def InitGL(Width, Height): 

	#glMatrixMode(GL_PROJECTION)
	#gluPerspective(45.0, float(w)/float(h), 0.1, 100.0)
	#glMatrixMode(GL_MODELVIEW)

	mat_specular = [ 1.0, 1.0, 1.0, 1.0 ]
	mat_shininess = [ 50.0 ]
	light_position =  [1.0, 1.0, 1.0, 0.0] 
	glClearColor (0.0, 0.0, 0.0, 0.0)
	glShadeModel (GL_SMOOTH)

	glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
	glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
	glLightfv(GL_LIGHT0, GL_POSITION, light_position)

	glEnable(GL_COLOR_MATERIAL)
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_DEPTH_TEST)



def reshape ( w,  h):
	if LUZES == True:
		glViewport (0, 0, w, h)
		glMatrixMode (GL_PROJECTION)
		glLoadIdentity()
		if (w <= h):
			glOrtho (-1.5, 1.5, -1.5* h/ w, 1.5* h/ w, -10.0, 10.0)
		else:
			glOrtho (-1.5* w/ h, 1.5* w/ h, -1.5, 1.5, -10.0, 10.0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()



def TelaDesenho():
	global WIRE,OBJETOSDESENHO,OBJETOSSELECIONADOS
	#glClearColor(1.0, 0.0, 3.0, 0.0) # muda cor do backgroud

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Remove everything from screen (i.e. displays all white)
	glLoadIdentity() # Reset all graphic/shape's position
	#glOrtho(0.0, w, 0.0, h, 0.0, 1.0) # remapeia as cordenadas
	if REDISPLAY == True:
		glutPostRedisplay()

	
	glScalef(ZOOM, ZOOM, ZOOM)
	#[tipo,centroX,centroY,raio,escala,rotx,rotax,roty,rotay,cor,wire]
	for idx,obj in enumerate(OBJETOSDESENHO):
		CORATUAL=obj[9]
		RAIO=obj[3]
		POSICAOX=obj[1]
		POSICAOY=obj[2]
		ESCALA=obj[4]
		ROTAX=obj[6]
		ROTX=obj[5]
		ROTAY=obj[8]
		ROTY=obj[7]
		WIRE=obj[10]
		tipo=obj[0]

		if idx in OBJETOSSELECIONADOS:
			CORATUAL=BRANCO

		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()

		glColor3f(CORATUAL[0],CORATUAL[1],CORATUAL[2])
		glTranslatef(POSICAOX,POSICAOY,0.0)
		glScalef(ESCALA, ESCALA, ESCALA)

		if ROTX == 1:
			glRotatef(ROTAX,ROTX,0,0.0)
		if ROTY == 1:
			glRotatef(ROTAY,0,ROTY,0.0)


		if tipo == "Teapot" and WIRE == True:
			glutWireTeapot(RAIO)
		if tipo == "Teapot" and WIRE == False:
			glutSolidTeapot(RAIO)

		if tipo == "Sphere" and WIRE == False:
			glutSolidSphere(RAIO,40,40)
		if tipo == "Sphere" and WIRE == True:
			glutWireSphere(RAIO,40,40)

		if tipo == "Donut" and WIRE == False:
			glutSolidTorus(RAIO/2,RAIO,40,40)
		if tipo == "Donut" and WIRE == True:
			glutWireTorus(RAIO/2,RAIO,40,40)

		if tipo == "Cube" and WIRE == False:
			glutSolidCube(RAIO)
		if tipo == "Cube" and WIRE == True:
			glutWireCube(RAIO)


		glPopMatrix()
		glFlush()

	glutSwapBuffers() # limpa o buffer (buffer duplo para agilidade). SE FOR 1 BUFFER DL SINGLE
 
#---------------------------------
#-------------TELA MENU
#---------------------------------

def drawTeapot():
	glLoadIdentity()
	glTranslatef(-0.40,0.80,0.0)
	glutSolidTeapot(0.1)
	glFlush()

	x,y=normalizaCoordenada(-0.40,0.80,wMenu, hMenu)
	newOBJ=[x,y,0.11,"Teapot"] 
	OBJETOSMENU.append(newOBJ)

def drawCube():
	glLoadIdentity()
	glTranslatef(0.40,0.80,0.0)
	glutSolidCube(0.2)
	glFlush()

	x,y=normalizaCoordenada(0.40,0.80,wMenu, hMenu)
	newOBJ=[x,y,0.11,"Cube"] 
	OBJETOSMENU.append(newOBJ)

def drawSphere():
	glLoadIdentity()
	glTranslatef(-0.40,0.40,0.0)
	glutSolidSphere(0.11,40,40)
	glFlush()

	x,y=normalizaCoordenada(-0.40,0.40,wMenu, hMenu)
	newOBJ=[x,y,0.11,"Sphere"] 
	OBJETOSMENU.append(newOBJ)

def drawDonut():
	glLoadIdentity()
	glTranslatef(0.40,0.40,0.0)
	glutSolidTorus(0.05,0.1,40,40)
	glFlush()

	x,y=normalizaCoordenada(0.40,0.40,wMenu, hMenu)
	newOBJ=[x,y,0.15,"Donut"]
	OBJETOSMENU.append(newOBJ)

def circuloDeCor(x,y,cor,NomeCor):	
	glColor3f(cor[0],cor[1],cor[2])
	glLoadIdentity()
	glTranslatef(x,y,0.0)
	#glScalef(2.5, 1.0, 1.0)
	glutSolidSphere(0.2,40,40)
	glFlush()


	xN,yN=normalizaCoordenada(x,y,wMenu, hMenu)
	newOBJ=[xN,yN,0.15,NomeCor] #TeaPot
	OBJETOSMENU.append(newOBJ)


def menuCores():

	circuloDeCor(-0.70,-0.3,VERMELHO,"VERMELHO")
	circuloDeCor(0,-0.3,AZUL,"AZUL")
	circuloDeCor(0.7,-0.3,VERDE,"VERDE")	

	circuloDeCor(-0.70,-0.8,LARANJA,"LARANJA")
	circuloDeCor(0,-0.8,ROSA,"ROSA")
	circuloDeCor(0.7,-0.8,AMARELO,"AMARELO")


def TelaMenu():
	global OBJETOSMENU
	OBJETOSMENU=[]
	glClearColor(0.0, 0.5, 0.5, 0.0) # muda cor do backgroud
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Remove everything from screen (i.e. displays all white)
	glLoadIdentity() # Reset all graphic/shape's position


	drawTeapot()
	drawCube()
	drawSphere()
	drawDonut()
	menuCores()


	glutSwapBuffers() # limpa o buffer (buffer duplo para agilidade). SE FOR 1 BUFFER DL SINGLE

#---------------------------------
#-------------TELA INSTRUÇÕES
#---------------------------------


def telaInstrucoes():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) 
	glClearColor(0, 0, 0, 0) # muda cor do backgroud


	drawText()

	glutSwapBuffers() # limpa o buffer (buffer duplo para agilidade). SE FOR 1 BUFFER DL SINGLE


def text(x,y,text):
	glColor3f(1.0, 1.0, 1.0)
	glRasterPos2f(x, y)
	for t in text:
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(t))


def drawText(textString="Teste"):
	text(-1.0, 0.8,"Teclas:")
	text(-0.8, 0.6,"S          - Entra/Sai do modo Seleção de Objeto")
	text(-0.8, 0.4,"L          - Muda iluminacao")
	text(-0.8, 0.2,"C          - Limpa tela de desenho")
	text(-0.8, 0.0,"R+(A,W,S,D)- Rotaciona Objeto(s) selecionado(s)")
	text(-0.8, -0.2,"Z,X       - Aumenta/diminui ZOOM")
	text(-0.8, -0.4,"-,+       - Aumenta/diminui Objeto(s) selecionado(s)")
	text(-0.8, -0.6,"W         - Tira/coloca em modo Wire Objeto(s) selecionado(s)")
	text(-0.8, -0.8,"Q         - Sair")




if __name__ == "__main__":
	#Inicializacao
	glutInit() #inicializa o ambiente


	#Janela Instruções
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH) # Set the display mode to be colored (RGBA - SISTEMA DE CORES)(DOUBLE - BUFFER DUPLO)(DEPTH - PARA USAR ALGORITMO DE PROFUNDIDADE EM 3D ZBUFFER)
	glutInitWindowSize(500, 200) # tamanho da janela
	glutInitWindowPosition(500, 800) # posicao da janela
	glutCreateWindow("instruções") # cria janela com titulo 
	glutDisplayFunc(telaInstrucoes)

	#Janela Menu
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH) # Set the display mode to be colored (RGBA - SISTEMA DE CORES)(DOUBLE - BUFFER DUPLO)(DEPTH - PARA USAR ALGORITMO DE PROFUNDIDADE EM 3D ZBUFFER)
	glutInitWindowSize(wMenu, hMenu) # tamanho da janela
	glutInitWindowPosition(300, 100) # posicao da janela
	glutCreateWindow("Menu") # cria janela com titulo 
	glutDisplayFunc(TelaMenu)
	glutMouseFunc(clickMenu)

	#Janela De desenho
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH) # Set the display mode to be colored (RGBA - SISTEMA DE CORES)(DOUBLE - BUFFER DUPLO)(DEPTH - PARA USAR ALGORITMO DE PROFUNDIDADE EM 3D ZBUFFER)
	glutInitWindowSize(w, h) # tamanho da janela
	glutInitWindowPosition(500, 100) # posicao da janela
	glutCreateWindow("Tela de desenho") # cria janela com titulo 
	InitGL(w, h)
	glutDisplayFunc(TelaDesenho)
	glutReshapeFunc(reshape)
	glutKeyboardFunc(keyboard)
	glutKeyboardUpFunc(keyboardUp)
	glutSpecialFunc(specialKey)
	glutMouseFunc(clickDesenha)




	glutMainLoop() # coloca a janela criada em loop
