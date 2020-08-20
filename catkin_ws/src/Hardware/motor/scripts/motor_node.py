#!/usr/bin/env python
import serial, time, sys, math
import rospy
from std_msgs.msg import Empty
from std_msgs.msg import Float32
from std_msgs.msg import Float32MultiArray
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Twist
from roboclaw import Roboclaw #archivo_driver.py -> nombre_clase
import tf

#Despligue de las opciones de ayuda necesarios en caso de que exista algun problema
def printHelp():
    print "Ayuda/Help:"
    print "\t --port \t Serial port name. El valor por defecto del puerto para el uso de la roboclaw es \"/dev/ttyACM0\""
    print ">> /hardware/motors/speeds\t Los valores usados en el topico deben encontrarse en el rango [-1, 1], 1 max velocidad del motor"
    print "<!> En caso de que se haya quemado la tarjeta roboclaw: Sabes lo que cuesta ese equipo hijo?<!>"

#Obtencion de las velociaddes por medio del topico /hardware/motors/speeds :: [Vel_Der , Vel Izq] >>> [M1, M2]
def callbackSpeeds(msg):
    
    #Las velocidades recibidas deben ser float en el rango [-1,1], respectivamente los valores de [0:127] traducidos a [0:1]
    #Siendo el valor 1 la maxima potencia del motor en la direccion indicada por medio de los signos
    # (+)>Adelante, (-)>Retroceso

    global leftSpeed
    global rightSpeed
    global newSpeedData

    #Obteniedo datos del topico 
    rightSpeed = float(msg.data[0])
    leftSpeed= float(msg.data[1])
    
    #print "[MOTOR_TEST|>>>Velocidades::  velDer:_"+str(float(rightSpeed))" ; VelIzq:_"+str(float(leftSpeed))+

    #Revision de los limites de veocidad obtenidas
    if leftSpeed > 1:
        leftSpeed = 1
    elif leftSpeed < -1:
        leftSpeed = -1
    if rightSpeed > 1:
        rightSpeed = 1
    elif rightSpeed < -1:
        rightSpeed = -1

    newSpeedData = True #Se activa bandera de que nuevos datos fueron obtenidos

#-------------------------------------------------------------------------------------------

#Algortimo para el calculo de la Odometria del robot segun los datos obtenidos de los encoders

def calculateOdometry(currentPos, leftEnc, rightEnc): #Los datos de los encoders se asume esten en pulsos

    leftEnc =leftEnc * 0.39/980 #De pulsos a metros  [!!!!!!!!!!]
    rightEnc = rightEnc * 0.39/980

    deltaTheta = (rightEnc - leftEnc)/0.48 #0.48m es el diametro del robot [!!!!!!!!!!!!]

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


#-------------------------------------------------------------------------------------------

# FUNCION PRINCIPAL 
def main(portName):
    print "Inicializando motores en modo de PRUEBA"

    ###Connection with ROS
    rospy.init_node("motor_node")

    #Suscripcion a Topicos
    subSpeeds = rospy.Subscriber("/hardware/motors/speeds", Float32MultiArray, callbackSpeeds)  #Topico para obtener vel y dir de los motores

    #Publicacion de Topicos

    #pubRobPos = rospy.Publisher("mobile_base/position", Float32MultiArray,queue_size = 1)
    #Publica los datos de la posición actual del robot

    pubOdometry = rospy.Publisher("mobile_base/odometry", Odometry, queue_size = 1) 
    #Publica los datos obtenidos de los encoders y analizados para indicar la posicion actual del robot

    #Estableciendo parametros de ROS
    br = tf.TransformBroadcaster() #Adecuando los datos obtenidos al sistema de coordenadas del robot
    rate = rospy.Rate(1)

    #Comunicacion serial con la tarjeta roboclaw Roboclaw

    print "Roboclaw.-> Abriendo conexion al puerto serial designacion: \"" + str(portName) + "\""
    RC= Roboclaw(portName, 38400)
    #Roboclaw.Open(portName, 38400)
    RC.Open()
    address = 0x80
    print "Roboclaw.-> Conexion establecida en el puerto serila designacion \"" + portName + "\" a 38400 bps (Y)"
    print "Roboclaw.-> Limpiando lecturas de enconders previas"
    RC.ResetEncoders(address)

    #Varibles de control de la velocidad
    global leftSpeed
    global rightSpeed
    global newSpeedData

    leftSpeed = 0 #[-1:0:1]
    rightSpeed = 0 #[-1:0:1]
    newSpeedData = False #Al inciar no existe nuevos datos de movmiento
    speedCounter = 5

    #Variables para la Odometria
    robotPos = Float32MultiArray()
    robotPos = [0, 0, 0] # [X,Y,TETHA]


    #Ciclo ROS
    #print "[VEGA]:: Probando los motores de ROTOMBOTTO"
    while not rospy.is_shutdown():

        if newSpeedData: #Se obtuvieron nuevos datos del topico /hardware/motors/speeds

            newSpeedData = False
            speedCounter = 5

            #Indicando la informacion de velocidades a la Roboclaw

            #Realizando trasnformacion de la informacion
            leftSpeed = int(leftSpeed*127)
            rightSpeed = int(rightSpeed*127)

            #Asignando las direcciones del motor derecho
            if rightSpeed >= 0:
                RC.ForwardM1(address, rightSpeed)
            else:
                RC.BackwardM1(address, -rightSpeed)

            #Asignando las direcciones del motor izquierdo
            if leftSpeed >= 0:
                RC.ForwardM2(address, leftSpeed)
            else:
                RC.BackwardM2(address, -leftSpeed)

        else: #NO se obtuvieron nuevos datos del topico, los motores se detienen

            speedCounter -= 1 

            if speedCounter == 0:
                RC.ForwardM1(address, 0)
                RC.ForwardM2(address, 0)
 
            if speedCounter < -1:
                speedCounter = -1

        #-------------------------------------------------------------------------------------------------------

        #Obteniendo informacion de los encoders
        encoderLeft = RC.ReadEncM2(address) #Falta multiplicarlo por -1, tal vez no sea necesario
        encoderRight = RC.ReadEncM1(address) #El valor negativo obtenido en este encoder proviene de la posicion de orientacion del motor.
        RC.ResetEncoders(address)

        #print "Lectura de los enconders Encoders: EncIzq" + str(encoderLeft) + "  EncDer" + str(encoderRight)

        ###Calculo de la Odometria
        robotPos = calculateOdometry(robotPos, encoderLeft, encoderRight)

        #pubRobPos=.publish(robotPos) ##Publicando los datos de la pocición obtenida

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

        pubOdometry.publish(msgOdom) #Publicando los datos de odometría

        rate.sleep()

    #Fin del WHILE ROS
    #------------------------------------------------------------------------------------------------------

    RC.ForwardM1(address, 0)
    RC.ForwardM2(address, 0)
    RC.Close()

#FIN DEL MAIN()

#______________________________________________________________________________________________________________________

#Definicion del programa principal con el puerto ttyACM a utilzar
if __name__ == '__main__':
    try:
        if "--help" in sys.argv:
            printHelp()
        elif "-h" in sys.argv:
            printHelp()
        else:
            portName = "/dev/ttyACM1"
            if "--port" in sys.argv:
                portName = sys.argv[sys.argv.index("--port") + 1]
            main(portName)

    except rospy.ROSInterruptException:
        pass

'''******************************************************************************
*   Garces Marin Daniel         
*   TESIS <Construccion de una plataforma robotica abierta para pruebas de desempeno de componentes y algoritmos>
*
*   <HARDWARE> Nodo MOTOR_TEST motor
*   El principal objetivo de este nodo es el de manejar el control de los motores por medio de la tarjeta roboclaw  
*       -Se debe destacar que se utilza una liberia para el uso de la tarjeta alojada en el paquete "driver_roboclaw"
*       Agradecimientos a Marco Antonio Negrete Villanueva y a MARCOSOFT
*       
*   Ultima version: 23 de Marzo del 2020
*
********************************************************************************'''
