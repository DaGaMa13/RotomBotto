#!/usr/bin/env python
'''******************************************************************************
*	Garcés Marín Daniel 		
*	TESIS <Construcción de una plataforma robótica abierta para pruebas de desempeño de componentes y algoritmos>
*
*	<HARDWARE_TOOLS> Hodo Joystick
*	El principal objetivo de este nodo es el de manejar el control alambrico tipo joystick para el control del movimiento de
*   la plataforma robótica móvil. 
*		#Agradecimientos a Marco Antonio Negrete Villanueva y a MARCOSOFT.s
*		
*   Ultima versión: 22 de Marzo del 2019
*******************************************************************************'''
# ダ・ガ・マ・jû-san

import math
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty


def callbackJoy(msg):
    global speedX
    global speedY
    global yaw
    global panPos
    global tiltPos
    global b_Button
    global spine	
    global mov_spine
    global waist
    global mov_waist	
    global shoulders
    global mov_shoulders
    global spine_button
    global waist_button
    global shoulders_button_1
    global shoulders_button_2
    global skip_state


    ### Read of b_button for stop the mobile base
    global stop
    ### Red button for stop of mobile base
    stop = msg.buttons[1]
    skip_state = msg.buttons[3]

    ### Control of head with left Stick 
    leftStickX = msg.axes[0]
    leftStickY = msg.axes[1]

    if msg.axes[2] == 0 and msg.axes[5] != 0:
        leftTigger = msg.axes[2]
        rightTigger = -(msg.axes[5] - 1) 

    elif msg.axes[5] == 0 and msg.axes[2] != 0:
        leftTigger = -(msg.axes[2] - 1)
        rightTigger = msg.axes[5] 

    elif msg.axes[5] == 0 and msg.axes[2] == 0:
        leftTigger = 0
        rightTigger = 0 
    else:
        leftTigger = -(msg.axes[2] - 1)
        rightTigger = -(msg.axes[5] - 1) 


    #print "leftTigger: " + str(leftTigger) +" rightTigger: " + str(rightTigger)

    ### Tigger button for speed y componente

    magnitudTiggerDiference = math.sqrt((leftTigger*leftTigger) + (rightTigger*rightTigger))
    #print "diference: " + str(magnitudTiggerDiference)
    if magnitudTiggerDiference > 0.15:
        speedY = (leftTigger - rightTigger)/2
    else:
        speedY = 0

    magnitudLeft = math.sqrt(leftStickX*leftStickX + leftStickY*leftStickY)
    if magnitudLeft > 0.1:
        panPos = leftStickX
        tiltPos = leftStickY
    else:
        panPos = 0
        tiltPos = 0
    

    ### Control of mobile-base with right Stick
    rightStickX = msg.axes[3]
    rightStickY = msg.axes[4]
    magnitudRight = math.sqrt(rightStickX*rightStickX + rightStickY*rightStickY)
    if magnitudRight > 0.15:
        speedX = rightStickY
        yaw = rightStickX
    else:
        speedX = 0
        yaw = 0

    #spine_button = msg.axes[7]
    spine_button = 0
    if msg.buttons[13]:
        spine_button = 1
    elif msg.buttons[14]:
        spine_button = -1

    if(spine_button == 1 or spine_button ==-1):
	mov_spine=True
	
    else:
	mov_spine=False

    #waist_button = msg.axes[6]
    waist_button = 0
    if msg.buttons[12]:
        waist_button = 1
    elif msg.buttons[11]:
        waist_button = -1

    if(waist_button == 1 or waist_button ==-1):
        mov_waist=True
        
    else:
        mov_waist=False
    
    shoulders_button_1 = msg.buttons[6]
    shoulders_button_2 = msg.buttons[7]

    if(shoulders_button_1 == 1 or shoulders_button_2 == 1):
	mov_shoulders=True
    else:
        mov_shoulders=False	


def main():
    global leftSpeed
    global rightSpeed
    global panPos 
    global tiltPos

    global speedX
    global speedY
    global yaw
    global stop
    global mov_spine
    global spine	
    global waist
    global mov_waist
    global shoulders
    global mov_shoulders
    global spine_button
    global waist_button
    global shoulders_button_1
    global shoulders_button_2
    global skip_state

    leftSpeed = 0
    rightSpeed = 0
    panPos = 0
    tiltPos = 0
    b_Button = 0
    stop = 0
    skip_state = 0
    speedY = 0
    speedX = 0
    yaw = 0
    spine =0
    mov_spine=False
    waist=0
    mov_waist=False
    shoulders=0
    mov_shoulders=False

    msgSpeeds = Float32MultiArray()
    msgHeadPos = Float32MultiArray()
    msgSpine = Float32()
    msgWaist = Float32()
    msgShoulders = Float32()

    #Variables donde se almacenarán los datos apublicar	
    msgTwist = Twist()
    msgStop = Empty()
    #msgHeadTorque = Float32MultiArray()
    
    print "JOYSTICK en línea"
    rospy.init_node("joystick_node")
       
    # rospy.Subscriber("/hardware/joy", Joy, callbackJoy)
    rospy.Subscriber("/hardware/joy", Joy, callbackJoy)

    #Topicos a publicaar

    pubStop = rospy.Publisher("/hardware/robot_state/stop", Empty, queue_size = 1)
    pubTwist = rospy.Publisher("/hardware/joystick/data", Twist, queue_size =1)

    loop = rospy.Rate(10)
    while not rospy.is_shutdown():

        #Publicación de las direcciones y velocidades para los motores
        if math.fabs(speedX) > 0 or math.fabs(speedY) > 0 or math.fabs(yaw) > 0:
            msgTwist.linear.x = speedX
            msgTwist.linear.y = speedY/2.0
            msgTwist.linear.z = 0
            msgTwist.angular.z = yaw
            print "x: " + str(msgTwist.linear.x) + "  y: " + str(msgTwist.linear.y) + " yaw: " + str(msgTwist.angular.z)
            pubTwist.publish(msgTwist)

        if stop == 1:
            pubStop.publish(msgStop)

        loop.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
