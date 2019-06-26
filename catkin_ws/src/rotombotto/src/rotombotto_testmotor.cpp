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
float vel_temp=0.0; //Variable para la prubra de velocidad de los motores, función pruebaMotores

	//Variables paraa guardar información de los tópicos
float dirMotor[2]={0,0}; //Variable para indicar los valores de dirección y velocidadesa los motores
				//[VelDer] [Velizq]
//_____________________________________________________________________________________________________________________

//>>>>>>>>>>> FUNCIONES <<<<<<<<<<<

	//Función para la pruba de los motores
int pruebaMotores(int contador){

	std::cout<<"Velocidad actual de los motores: >"<<vel_temp<<std::endl;



	if (contador>0&&contador<=10){ //[0:10]
		std::cout<<" MOTORES AVANZANDO"<<std::endl;
		vel_temp=contador/10;
		dirMotor[0]=vel_temp;
		dirMotor[1]=vel_temp;
	}

	else if (contador>10&&contador<=20){ //[11:20]
		std::cout<<" MOTORES RETROCESO"<<std::endl;
		vel_temp=(contador/10)-1;
		dirMotor[0]=(-1*vel_temp);
		dirMotor[1]=(-1*vel_temp);
	}

	else if (contador>20&&contador<=30){ //[21:30]
		std::cout<<" MOTORES GIRO IZQUIERDA"<<std::endl;
		vel_temp=(contador/10)-2;
		dirMotor[0]=vel_temp;
		dirMotor[1]=(-1*vel_temp);
	}

	else if (contador>30&&contador<=40){ //[31:40]
		std::cout<<" MOTORES GIRO DERECHA"<<std::endl;
		vel_temp=(contador/10)-3;
		dirMotor[0]=(-1*vel_temp);
		dirMotor[1]=vel_temp;
	}

	else if (contador==0){
		std::cout<<" MOTORES ALTO"<<std::endl;
		dirMotor[0]=0;
		dirMotor[1]=0;
	}

	else
		std::cout<<" MOTORES DESCONOCIDO"<<std::endl;

	contador=contador+1; //Aunmentando el contador

	if (contador>40)
		contador=0; //Reiniciando el contador

	return contador;

}//Fin de prueba motores


//_______________________________________________________________________________________________________________
//Función principal
int main(int  argc, char** argv){

	std::cout<<">>>>>ROTOMBOTTO EN MODO DE PRUEBA DE MOTORES EN LÍNEA<<<<<<"<<std::endl;
	ros::init(argc,argv,"ROTOMBOTTO");
	ros:: NodeHandle n;

 	//Datos a publicar
	std_msgs::Float32MultiArray  D_Motor; //Dirección del motor
	D_Motor.data.resize(2);	

    //Publicación de las velocidades de los motores la Roboclaw
    ros::Publisher pubDir=n.advertise <std_msgs::Float32MultiArray>("/hardware/motors/speeds",1);

	ros::Rate loop(1);
    ros::Rate r(10);

    cont=0;
	
	while(ros::ok()){

		cont=pruebaMotores(cont); //Se prueban los motores

		//Publicación de tópico de las direcciones
	  	D_Motor.data[0] = dirMotor[0]; 
	   	D_Motor.data[1] = dirMotor[1];
	    std::cout<<D_Motor<<std::endl;

		pubDir.publish(D_Motor);  //Envió de las direcciónes al nodo Motor.py

		ros::spinOnce();
		loop.sleep();
        std::cout<<""<<std::endl;

	} //Fin del while(ROS)

return 0;
}//Fin del main principal
