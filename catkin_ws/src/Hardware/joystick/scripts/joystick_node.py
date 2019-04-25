#!/usr/bin/env python

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

def main():
    global leftSpeed
    global rightSpeed
    global panPos 
    global tiltPos

    global speedX
    global speedY
    global yaw
    global stop

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

    #Variables donde se almacenaran los datos a publicar	
    msgTwist = Twist()
    msgStop = Empty()
    
    print "JOYSTICK en linea"
    rospy.init_node("joystick")
       
    # rospy.Subscriber("/hardware/joy", Joy, callbackJoy)
    rospy.Subscriber("/hardware/joy", Joy, callbackJoy)

    #Topicos a publicar
    pubStop = rospy.Publisher("/hardware/robot_state/stop", Empty, queue_size = 1)
    pubTwist = rospy.Publisher("/hardware/joystick/data", Twist, queue_size =1)

    loop = rospy.Rate(10)
    while not rospy.is_shutdown():

        #Publicacion de las direcciones y velocidades para los motores
        if math.fabs(speedX) > 0 or math.fabs(speedY) > 0 or math.fabs(yaw) > 0:
            msgTwist.linear.x = speedX
            msgTwist.linear.y = speedY/2.0
            msgTwist.linear.z = 0
            msgTwist.angular.z = yaw
            #print "x: " + str(msgTwist.linear.x) + "  y: " + str(msgTwist.linear.y) + " yaw: " + str(msgTwist.angular.z)
            pubTwist.publish(msgTwist)

        if stop == 1:
            pubStop.publish(msgStop)

        #loop.sleep()

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
*   la plataforma robotica movil. 
*       #Agradecimientos a Marco Antonio Negrete Villanueva y a MARCOSOFT
*       
*   Ultima version: 26 de Marzo del 2019
*******************************************************************************'''