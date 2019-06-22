/**********************************************************************
*	Garcés Marín Daniel 		
*	TESIS <Construcción de una plataforma robótica abierta para pruebas de desempeño de componentes y algoritmos>
*
*	<ROTOMBOTTO> Nodo para prueba de los motores 
*		El principal objetivo de este nodo es el dar una revisión de los motores, por medio de enviar direcciones automaticamente
*		incrementales y decrementales por medio de este nodo, con el fin de probar la interacciín motores-roboclaw-nodos del sistema.
*
*   Ultima versión: 10 de Junio del 2019
**********************************************************************/

//>>>>>>>> LIBRERÍAS <<<<<<<<<<<<<
// ダ・ガ・マ・jû-san
#include "ros/ros.h"
#include "std_msgs/Float32MultiArray.h"
#include "std_msgs/String.h"
#include <stdio.h>
#include <stdlib.h>
#include <termios.h>
#include <unistd.h>
#include <termio.h>
#include <sys/ioctl.h>
#include <string>
#include <iostream>
using namespace std;
//----------------------------------

//>>> VARAIBLES GLOBALES

	//Variables de apoyo
int i=0,j=0; //varaibles contadores
int temp=0,cont=0; //Varaibles para la dirección de prueba de los motores, función pruebaMotores()

	//Variables paraa guardar información de los tópicos
float datos_joy[3]= {0,0,0}; //Variables para el tópico de información del joystick
float dirMotor[2]={0,0}; //Variable para indicar los valores de dirección y velocidadesa los motores

//_____________________________________________________________________________________________________________________

//>>>>>>>>>>> FUNCIONES <<<<<<<<<<<


	//Obtención del la dirección del nodo SMART THINGS
void dataJoy(const std_msgs::Float32MultiArray::ConstPtr& dataJ){

	datos_joy[0] = dataJ->data[0]; //Boton B
	datos_joy[1] = dataJ->data[1]; //BOTON DERECHO
	datos_joy[2] = dataJ->data[2]; //BOTON Izquierdo

	std::cout<<"Datos de los botones recibidos:: B:"<<datos_joy[0]<<" B_DER:"<<datos_joy[1]<<" B_IZQ:"<<datos_joy[2]<<std::endl;	}//Fin de dirObtenida
//-----------------------------------------------------------------------------------------

	//Función para la pruba de los motores
void pruebaMotores(const std_msgs::Float32MultiArray::ConstPtr& motorD){

	dirMotor[0] = motorD->data[0]; //Velocidad motor Derecho
	dirMotor[1] = motorD->data[1]; //Velocidad motor Izquiero

	std::cout<<"Datos de los botones recibidos:: VEL_DER:"<<dirMotor[0]<<" VEL_IZQ:"<<dirMotor[0]<<std::endl;

	if (dirMotor[0]>0 && dirMotor[1]>0)
		std::cout<<" MOTORES AVANZANDO"<<std::endl;

	else if (dirMotor[0]<0 && dirMotor[1]<0)
		std::cout<<" MOTORES RETROCESO"<<std::endl;

	else if (dirMotor[0]>0 && dirMotor[1]<0)
		std::cout<<" MOTORES GIRO IZQUIERDA"<<std::endl;

	else if (dirMotor[0]<0 && dirMotor[1]>0)
		std::cout<<" MOTORES GIRO DERECHA"<<std::endl;

	else if (dirMotor[0]==0 && dirMotor[1]==0)
		std::cout<<" MOTORES ALTO"<<std::endl;

	else
		std::cout<<" MOTORES DESCONOCIDO"<<std::endl;

}//Fin de prueba motores


//_______________________________________________________________________________________________________________
//Función principal
int main(int  argc, char** argv){

	std::cout<<">>>>>ROTOMBOTTO EN MODO DE PRUEBA EN LÍNEA<<<<<<"<<std::endl;
	ros::init(argc,argv,"ROTOMBOTTO");
	ros:: NodeHandle n;

    //Obtención de los datos transmitidos por los diferentes nodos 
 	ros::Subscriber subFoto = n.subscribe("/hardware/sensors/luz",10,valorFoto); //Nodo Sensors/Fotoresistores
 	ros::Subscriber subTempt = n.subscribe("/hardware/sensors/tempt",10,valorTempt); //Nodo Sensors/Temperatura
 	ros::Subscriber subJoy = n.subscribe("/hardware/joystick/data",100,dataJoy); //Nodo Hardware/joy

 	//Datos a publicar
	std_msgs::Float32MultiArray  D_Motor; //Dirección del motor
	D_Motor.data.resize(2);	

    //Publicación de las velocidades de los motores la Roboclaw
    ros::Publisher pubDir=n.advertise <std_msgs::Float32MultiArray>("/hardware/motors/speeds",1);

	ros::Rate loop(1);
    ros::Rate r(10);
	
	while(ros::ok()){

	//pruebaMotores(); //Se prueban los motores

		//Publicación de tópico de las direcciones
	  //D_Motor.data[0] = 1; 
	   //D_Motor.data[1] = 1;
	    //std::cout<<D_Motor<<std::endl;

		//pubDir.publish(D_Motor);  //Envió de las direcciónes al nodo Motor.py

		ros::spinOnce();
		loop.sleep();
        std::cout<<""<<std::endl;

	} //Fin del while(ROS)

return 0;
}//Fin del main principal
