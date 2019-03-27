#!/usr/bin/env python
import serial, time, sys, math
import rospy
from std_msgs.msg import Empty
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Twist
import Roboclaw 
import tf

# Funcion para solucionar problemas frecuentes en el uso de la paqueteria
def printHelp():
    print "Ayuda/Help:"
    print "\t --port \t Serial port name. El valor por defecto del puerto para el uso de la roboclaw es \"/dev/ttyACM0\""
    print " hardware/motors/speeds\t Los valores usados en el topico deben encontrarse en el rango [-1, 1], 1 max velocidad del motor"
    print " En caso de que se haya quemado la tarjeta roboclaw: Sabes lo que cuesta ese equipo hijo?"

# Funcion para detener el movimiento con los motores, se suscribe a un topico en especifico /hardware/motors/stop
def callbackStop(msg):
    velIzq = 0
    velDer = 0
    newSpeedData = True

# Funcion para obtener las velocidades y direccion de los motores, topico /hardware/motors/speeds
def callbackSpeeds(msg):

    #Variables globales, se espera que los valores obtenidos se encuentren entre el rango de [-1,1] siendo {1} la vel. max. del motor
    global velIzq
    global velDer
    global nuevosDatosVel

    velIzq = msg.data[0]
    velDer = msg.data[1]
    print "Valores de velocidades obtenidos:: VelIzq:_"+VelIzq+" ; velDer:_"+velDer

    #Transformacion a valores que superen los limites
    if velIzq > 1:
        velIzq = 1
    elif velIzq < -1:
        velIzq = -1
    if velDer > 1:
        velDer = 1
    elif velDer < -1:
        velDer = -1
    nuevosDatosVel = True

def calculateOdometry(currentPos, leftEnc, rightEnc): #Encoder measurements are assumed to be in ticks
    leftEnc = leftEnc * 0.39/980 #From ticks to meters
    rightEnc = rightEnc * 0.39/980
    deltaTheta = (rightEnc - leftEnc)/0.48 #0.48 is the robot diameter
    if math.fabs(deltaTheta) >= 0.0001:
        rg = (leftEnc + rightEnc)/(2*deltaTheta)
        deltaX = rg*math.sin(deltaTheta)
        deltaY = rg*(1-math.cos(deltaTheta))
    else:
        deltaX = (leftEnc + rightEnc)/2
        deltaY = 0
    currentPos[0] += deltaX * math.cos(currentPos[2]) - deltaY * math.sin(currentPos[2])
    currentPos[1] += deltaX * math.sin(currentPos[2]) + deltaY * math.cos(currentPos[2])
    currentPos[2] += deltaTheta
    return currentPos

# FUNCION PRINCIPAL 
def main(portName):
    print "Inicializando motores en modo de PRUEBA"

    ###Connection with ROS
    rospy.init_node("motor_test")

    #Suscripcion a Topicos
    subStop = rospy.Subscriber("/hardware/motors/stop", Empty, callbackStop) #Topico para detener el movimiento del robot
    subSpeeds = rospy.Subscriber("/hardware/motors/speeds", Float32MultiArray, callbackSpeeds)  #Topico para obtener vel y dir de los motores

    #Publicacion de Topicos
    pubOdometry = rospy.Publisher("mobile_base/odometry", Odometry, queue_size = 1) ##PENDIENTE

    br = tf.TransformBroadcaster()
    rate = rospy.Rate(20)

    #Comunicacion serial con la tarjeta roboclaw Roboclaw

    print "Roboclaw.-> Abriendo conexion al puerto serial designacion: \"" + portName + "\""
    Roboclaw.Open(portName, 38400)
    address = 0x80
    print "Roboclaw.-> Conexion establecida en el puerto serila designacion \"" + portName + "\" a 38400 bps (Y)"
    print "Roboclaw.-> Limpiando lecturas de enconders previas"
    Roboclaw.ResetQuadratureEncoders(address)

    #Variables para la designacion de velocidad a los motores
    global velIzq
    global velDer
    global nuevosDatosVel

    velIzq = 0
    velDer = 0
    nuevosDatosVel = False
    speedCounter = 5

    ###Variables for odometry
    robotPos = [0, 0, 0]

    while not rospy.is_shutdown():

        if nuevosDatosVel: #Se obtuvieron nuevos datos del topico /hardware/motors/speeds

            nuevosDatosVel = False
            speedCounter = 5

            velIzq = int(velIzq*127)
            velDer = int(velDer*127)
            if velIzq >= 0:
                Roboclaw.DriveForwardM2(address, velIzq)
            else:
                Roboclaw.DriveBackwardsM2(address, -velIzq)
            if velDer >= 0:
                Roboclaw.DriveForwardM1(address, velDer)
            else:
                Roboclaw.DriveBackwardsM1(address, -velDer)

        else: #NO se obtuvieron nuevos datos del topico, los motores se detienen

            speedCounter -= 1

            if speedCounter == 0:
                Roboclaw.DriveForwardM1(address, 0)
                Roboclaw.DriveForwardM2(address, 0)
 
            if speedCounter < -1:
                speedCounter = -1

        encoderLeft = -Roboclaw.ReadQEncoderM2(address)
        encoderRight = -Roboclaw.ReadQEncoderM1(address) #The negative sign is just because it is the way the encoders are wired to the roboclaw
        Roboclaw.ResetQuadratureEncoders(address)


        ###Odometry calculation
        robotPos = calculateOdometry(robotPos, encoderLeft, encoderRight)
        print "Encoders: " + str(encoderLeft) + "  " + str(encoderRight)

        ##Odometry and transformations
        ts = TransformStamped()
        ts.header.stamp = rospy.Time.now()
        ts.header.frame_id = "odom"
        ts.child_frame_id = "base_link"
        ts.transform.translation.x = robotPos[0]
        ts.transform.translation.y = robotPos[1]
        ts.transform.translation.z = 0
        ts.transform.rotation = tf.transformations.quaternion_from_euler(0, 0, robotPos[2])
        br.sendTransform((robotPos[0], robotPos[1], 0), ts.transform.rotation, rospy.Time.now(), ts.child_frame_id, ts.header.frame_id)
        msgOdom = Odometry()
        msgOdom.header.stamp = rospy.Time.now()
        msgOdom.pose.pose.position.x = robotPos[0]
        msgOdom.pose.pose.position.y = robotPos[1]
        msgOdom.pose.pose.position.z = 0
        msgOdom.pose.pose.orientation.x = 0
        msgOdom.pose.pose.orientation.y = 0
        msgOdom.pose.pose.orientation.z = math.sin(robotPos[2]/2)
        msgOdom.pose.pose.orientation.w = math.cos(robotPos[2]/2)
        pubOdometry.publish(msgOdom)

        rate.sleep()

    #Fin del while

    Roboclaw.DriveForwardM1(address, 0)
    Roboclaw.DriveForwardM2(address, 0)
    Roboclaw.Close()

#Fin del al funcion principal Main

if __name__ == '__main__':
    try:
        if "--help" in sys.argv:
            printHelp()
        elif "-h" in sys.argv:
            printHelp()
        else:
            portName = "/dev/ttyACM0"
            if "--port" in sys.argv:
                portName = sys.argv[sys.argv.index("--port") + 1]
            main(portName)

    except rospy.ROSInterruptException:
        pass

'''******************************************************************************
*   Garces Marin Daniel         
*   TESIS <Construccion de una plataforma robotica abierta para pruebas de desempeno de componentes y algoritmos>
*
*   <HARDWARE> Nodo motor
*   El principal objetivo de este nodo es el de manejar el control de los motores por medio de la tarjeta roboclaw  
*       -Se debe destacar que se utilza una liberia para el uso de la tarjeta alojada en el paquete "hardware_tools"
*       Agradecimientos a Marco Antonio Negrete Villanueva y a MARCOSOFT
*       --  NODO ESPECFICAMENTE PARA PRUEBAS DE HARDWARE 
*       
*   Ultima version: 26 de Marzo del 2019
*******************************************************************************'''