#!/usr/bin/env python
import math
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
#_________________________________________________________________________________________________________________________

def callbackJoy(msg):

	global vel_D
	global vel_I
	global b
	global bD
	global bI 

	print "Obteniendo los datos del control joystick"
	print "-----------------------------------------------"

	#Obteniedo los datos del joystuck derecho para cotrol de la base movil
	StickD_X = msg.axes[3]
	StickD_Y = msg.axes[4]

	print "Datos del stick derecho:::  x:_"+str(float(StickD_X))+"  y:_"+str(float(StickD_Y))

	boton_b = msg.buttons[1]
	boton_I = msg.buttons[4]
	boton_D = msg.buttons[5]
	#boton_jusan = msg.buttons[13]

	b = float(boton_b)
	bD = float(boton_D)
	bI = float(boton_I)
	#b13 = float(boton_jusan)

	if b == 1:
		print "Boton B presionado"

	elif bD == 1:
		print "Boton DERECHO presionado"

	elif bI == 1:
		print "Boton IZQUIERDO presionado"

	else:
		print "Ningun boton presionado"

	#EXTRA

	#if b13 == 1:
	#	print "Obteniedo velocidades por medio de HORI"
	#	StickD_X = msg.axes[2]
	#	StickD_Y = msg.axes[3]

	#	print "Datos HORI del stick derecho:::  x:_"+str(float(StickD_X))+"  y:_"+str(float(StickD_Y))
	#	print "-------------------------------------------------------------"

	#Obteniedo velocidades

	magnitud = math.sqrt(StickD_X*StickD_X + StickD_Y*StickD_Y)

	if magnitud > 0.15: 

		if (StickD_Y > 0) and (StickD_Y>StickD_X): #Avanza [1,1]

			vel_D = float(magnitud) 
			vel_I = float(magnitud)

		elif (StickD_Y) < 0 and (StickD_Y<StickD_X): #Atras [-1,-1]

			vel_D = float(magnitud)*(-1)
			vel_I = float(magnitud)*(-1)

		elif (StickD_X < 0) and (StickD_X<=StickD_Y): #Giro Derecha [-1,1]

			vel_D = float(magnitud)*(-1)
			vel_I = float(magnitud)

		elif (StickD_X > 0) and (StickD_Y>=StickD_X): #Giro Izquierda [1,-1]

			vel_D = float(magnitud)
			vel_I = float(magnitud)*(-1)


	else: #ALTO
		vel_D = 0
		vel_I = 0

	print "Velocidades obtenidas: Vel Der = "+str(vel_D)+"  Vel Izq = "+str(vel_I)


	print "****************************************************"


#_________________________________________________________________________________________________________________________
def main():

	global vel_D
	global vel_I
	global b
	global bD
	global bI 

	vel_D = 0
	vel_I = 0
	b = 0
	bD = 0
	bI = 0

	msgVel = Float32MultiArray()
	msgJoy = Float32MultiArray()

	print "JOYSTICK TEST en linea"
	rospy.init_node("joystick")

	#TOPICOS a subscribirse
	rospy.Subscriber("/hardware/joy", Joy, callbackJoy) #Suscrpcion al nodo predeterminado JOY

	#Topicos a publicar
	pubVel=rospy.Publisher("/hardware/motors/speeds", Float32MultiArray, queue_size=1)
	pubJoy=rospy.Publisher("/hardware/joystick/data", Float32MultiArray, queue_size=1)


	loop = rospy.Rate(10)
	while not rospy.is_shutdown():

		#print "Recibiendo datos----"

		#Asignando datos recolectados
		msgVel.data = [vel_D,vel_I]
		msgJoy.data = [b,bD,bI]

		#Publicando topicos
		pubVel.publish(msgVel)
		pubJoy.publish(msgJoy)

	#rospy.spin()

#_________________________________________________________________________________________________________________________
if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass

'''******************************************************************************
*   Garces Marin Daniel         
*   TESIS <Construccion de una plataforma robotica abierta para pruebas de desempeno de componentes y algoritmos>
*
*   <HARDWARE_TOOLS> Hodo Joystick
*   El principal objetivo de este nodo es el de manejar el control alambrico tipo joystick para el control del movimiento de
*   la plataforma robotica movil. <MODO TEST>
*       #Agradecimientos a Marco Antonio Negrete Villanueva y a MARCOSOFT
*       
*   Ultima version: 8 de Mayo del 2019
*******************************************************************************'''