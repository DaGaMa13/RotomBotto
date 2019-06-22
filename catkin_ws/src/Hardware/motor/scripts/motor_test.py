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

#Obtencion de las velociaddes por medio del topico /hardware/motors/speeds
def callbackSpeeds(msg):
    global leftSpeed
    global rightSpeed
    global newSpeedData
    #Las velocidades recibidas deben ser float en el rango [-1,1], respectivamente los valores de [0:127] traducidos a [0:1]
    #Siendo el valor 1 la maxima potencia del motor en la direccion indicada por medio de los signos
    # (+)>Adelante, (-)>Retroceso

    #Obteniedo datos del topico 
    leftSpeed = float(msg.data[0])
    rightSpeed = float(msg.data[1])
    print "[MOTOR_TEST|>>>Valores de velocidades obtenidos:: VelIzq:_"+str(float(leftSpeed))+" ; velDer:_"+str(float(rightSpeed))


    #Revision de los limites de veocidad obtenidas
    if leftSpeed > 1:
        leftSpeed = 1
    elif leftSpeed < -1:
        leftSpeed = -1
    if rightSpeed > 1:
        rightSpeed = 1
    elif rightSpeed < -1:
        rightSpeed = -1
    newSpeedData = True

#-------------------------------------------------------------------------------------------

# FUNCION PRINCIPAL 
def main(portName):
    print "Inicializando motores en modo de PRUEBA"

    ###Connection with ROS
    rospy.init_node("motor_test")

    #Suscripcion a Topicos
    subSpeeds = rospy.Subscriber("/hardware/motors/speeds", Float32MultiArray, callbackSpeeds)  #Topico para obtener vel y dir de los motores

    #Estableciendo parametros de ROS
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(20)

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
    newSpeedData = False
    speedCounter = 5

    #Variables para la Odometria
    robotPos = [0, 0, 0] # [X,Y,TETHA]


    #Ciclo ROS
    print "[VEGA]:: Probando los motores de ROTOMBOTTO"
    while not rospy.is_shutdown():

        if newSpeedData: #Se obtuvieron nuevos datos del topico /hardware/motors/speeds

            newSpeedData = False
            speedCounter = 5

            #Indicando la informacion de velocidades a la Roboclaw

            #Realizando trasnformacion de la informacion
            leftSpeed = int(leftSpeed*127)
            rightSpeed = int(rightSpeed*127)

            #Asignando las direcciones del motor izquierdo
            if leftSpeed >= 0:
                RC.ForwardM2(address, leftSpeed)
            else:
                RC.BackwardsM2(address, -leftSpeed)

            #Asignando las direcciones del motor derecho
            if rightSpeed >= 0:
                RC.ForwardM1(address, rightSpeed)
            else:
                RC.BackwardsM1(address, -rightSpeed)

        #Obteniendo informacion de los encoders
        encoderLeft = RC.ReadEncM2(address) #Falta multiplicarlo por -1, tal vez no sea necesario
        encoderRight = RC.ReadEncM1(address) #El valor negativo obtenido en este encoder proviene de la posicion de orientacion del motor.
        RC.ResetEncoders(address)

        print "[VEGA]:: Lectura de los enconders Encoders: EncIzq" + str(encoderLeft) + "  EncDer" + str(encoderRight)
        

    #FIN DEL WHILE

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
*   <HARDWARE> Nodo motor
*   El principal objetivo de este nodo es el de manejar el control de los motores por medio de la tarjeta roboclaw  
*       -Se debe destacar que se utilza una liberia para el uso de la tarjeta alojada en el paquete "hardware_tools"
*       Agradecimientos a Marco Antonio Negrete Villanueva y a MARCOSOFT
*       --  NODO ESPECFICAMENTE PARA PRUEBAS DE HARDWARE 
*       
*   Ultima version: 18 de Junio del 2019
*
********************************************************************************'''