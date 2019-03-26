/**********************************************************************
*	Garcés Marín Daniel 		
*	TESIS <Construcción de una plataforma robótica abierta para pruebas de desempeño de componentes y algoritmos>
*
*	<ROTOMBOTTO> Nodo para prueba del software
*		El principal objetivo de este nodo es el dar una revisión de los elementos que componen el robot y publicar todos los
*		datos a disposición con el fin de revisar el estado del equipo y localizar discrepancias o problemas con el hardware.
*
*   Ultima versión: 25 de Marzo del 2019
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
int num_fot=0; //Variable para la función valorFoto()
float valor_foto=0.0; //Variable para la función valorFoto()

	//Variables paraa guardar información de los tópicos
float datos_Foto[8]={0,0,0,0,0,0,0,0}; //Variable para la función valorFoto()
float datos_Tempt=0; //Variables para la funcion valorTempt()
float dir_MotorA[2]={0.0,0.0}; //Variable para indicar los valores de dirección y velocidadesa los motores

//_____________________________________________________________________________________________________________________

//>>>>>>>>>>> FUNCIONES <<<<<<<<<<<

	//Obtención de los valores de los fotoresistores
void valorFoto(const std_msgs::Float32MultiArray::ConstPtr& dFoto){

	for(i=0;i<4;i++){ //Vaciado de los valores fotoresitores
		datos_Foto[i]=dFoto->data[i];
		std::cout<<"Fotoresitor["<<i<<"]:_ "<<datos_Foto[i]<<std::endl;	}//Fin Vaciado de los valores fotoresitores

	//Tratamiento de los datos:: Obteniedo valor más alto;
	for(i=0;i<4;i++){ //comparación de todos los valores prra saber el más alto

		if(valor_foto<=datos_Foto[i]){ //valor actual mayor
			num_fot=i;
			valor_foto=datos_Foto[i]; }	} //Fin de la busqueda mayor

	std::cout<<"Fuente de luz ubicada en fotoresitor["<<num_fot<<"]:: "<<valor_foto<<std::endl;

	std::cout<<" --"<<std::endl;									}//Fin de valorFoto
//----------------------------------------------------------------------------------------

	//Obtención de la temperatura registrada en el robot
void valorTempt(const std_msgs::Float32MultiArray::ConstPtr& dEnc){

	std::cout<<"Temperatura::";
		datos_Tempt]=dEnc->data;
		std::cout<<"["<<datos_Tempt<<"]";  //Fin del vaciado de los encoders

	std::cout<<" --"<<std::endl;  								}//Fin de valorEnc
//-----------------------------------------------------------------------------------------

	//Obtención del la dirección del nodo SMART THINGS
void dirObtenida(const std_msgs::String::ConstPtr& dirM){
	dirMotor=dirM->data;
	std::cout<<"Dirección recibida::_"<<dirMotor<<std::endl;	}//Fin de dirObtenida
//-----------------------------------------------------------------------------------------

	//Función para la pruba de los motores
void pruebaMotores(){


}//Fin de prueba motores


//_______________________________________________________________________________________________________________
//Función principal
int main(int  argc, char** argv){

	std::cout<<">>>>>ROTOMBOTTO EN MODO DE PRUEBA EN LÍNEA<<<<<<"<<std::endl;
	ros::init(argc,argv,"ROTOMBOTTO");
	ros:: NodeHandle n;

    //Obtención de los datos transmitidos por los diferentes nodos 
 	ros::Subscriber subFoto = n.subscribe("/hardware/sensors/luz",1000,valorFoto); //Nodo Sensors/Fotoresistores
 	ros::Subscriber subEnc = n.subscribe("/hardware/sensors/tempt",1000,valorTempt);; //Nodo Sensors/Temperatura
 	//ros::Subscriber subEnc = n.subscribe("/hardware/joystick/data",1000,dirObtenida);; //Nodo Sensors/Temperatura


 	//Datos a publicar
	std_msgs::Float32MultiArray  D_Motor; //Dirección del motor
	D_Motor.data.resize(2);	

    //Publicación de las velocidades de los motores al Arduino
    //ros::Publisher pubDir=n.advertise <std_msgs::Float32MultiArray>("/hardware/motor/speeds",1);

	ros::Rate loop(1);
    ros::Rate r(10);
	
	while(ros::ok()){

	//pruebaMotores(); //Se prueban los motores

		//Publicación de tópico de las direcciones
    //D_Motor.data = dir_MotorA; //<-----
	//std::cout<<D_Motor<<std::endl;

		//pubDir.publish(D_Motor);  //Envió de las direcciónes al nodo Motor.py

		ros::spinOnce();
		loop.sleep();
        std::cout<<""<<std::endl;

	} //Fin del while(ROS)

return 0;
}//Fin del main principal