/**********************************************************************
*	Garcés Marín Daniel 		
*	TESIS <Construcción de una plataforma robótica abierta para pruebas de desempeño de componentes y algoritmos>
*
*	<ROTOMBOTTO> Nodo para prueba del software
*		El principal objetivo de este nodo es el dar una revisión de los elementos que componen el robot y publicar todos los
*		datos a disposición con el fin de revisar el estado del equipo y localizar discrepancias o problemas con el hardware.
*
*   Ultima versión: 4 de Marzo del 2019
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
float datos_Enc[12]={0,0,0,0,0,0,0,0,0,0,0,0}; //Variables para la funcion valorEnc()
float dir_MotorA[2]={0.0,0.0}; //Variable para indicar los valores de dirección y velocidadesa los motores

string dirMotor; //Variable para almacenar la dirección de los motores trasnmitida por SmartThings en función dirObtenida()
//_____________________________________________________________________________________________________________________

//>>>>>>>>>>> FUNCIONES <<<<<<<<<<<

	//Obtención de los valores de los fotoresistores
void valorFoto(const std_msgs::Float32MultiArray::ConstPtr& dFoto){

	for(i=0;i<8;i++){ //Vaciado de los valores fotoresitores
		datos_Foto[i]=dFoto->data[i];
		std::cout<<"Fotoresitor["<<i<<"]:_ "<<datos_Foto[i]<<std::endl;	}//Fin Vaciado de los valores fotoresitores

	//Tratamiento de los datos:: Obteniedo valor más alto;
	for(i=0;i<8;i++){ //comparación de todos los valores prra saber el más alto

		if(valor_foto<=datos_Foto[i]){ //valor actual mayor
			num_fot=i;
			valor_foto=datos_Foto[i]; }	} //Fin de la busqueda mayor

	std::cout<<"Fuente de luz ubicada en fotoresitor["<<num_fot<<"]:: "<<valor_foto<<std::endl;

	std::cout<<" --"<<std::endl;									}//Fin de valorFoto
//----------------------------------------------------------------------------------------

	//Obtención de los valores de los encoders
void valorEnc(const std_msgs::Float32MultiArray::ConstPtr& dEnc){

	std::cout<<"Encoders ::";
	for(i=0;i<12;i++){ //Vaciando los datos de los encoders
		datos_Enc[i]=dEnc->data[i];
		std::cout<<"["<<datos_Enc<<"]"; } //Fin del vaciado de los encoders

	std::cout<<" --"<<std::endl;  								}//Fin de valorEnc
//-----------------------------------------------------------------------------------------

	//Obtención del la dirección del nodo SMART THINGS
void dirObtenida(const std_msgs::String::ConstPtr& dirM){
	dirMotor=dirM->data;
	std::cout<<"Dirección recibida::_"<<dirMotor<<std::endl;	}//Fin de dirObtenida
//-----------------------------------------------------------------------------------------

	//Función para la pruba de los motores
void pruebaMotores(){

	float vel_prueba=125; //Velocidad con la que probarán los motores

	switch(temp){

					case 0:	//Avanza
							dir_MotorA[0]=vel_prueba;
							dir_MotorA[1]=vel_prueba;
							break;

					case 1://Atras
							dir_MotorA[0]=(-1*vel_prueba);
							dir_MotorA[1]=(-1*vel_prueba);
							break;

					case 2://Giro Derecha
							dir_MotorA[0]=vel_prueba;
							dir_MotorA[1]=(-1*vel_prueba);
							break;

					case 3://Giro Izquierda
							dir_MotorA[0]=(-1*vel_prueba);
							dir_MotorA[1]=vel_prueba;
							break;

					case 4://Alto
							dir_MotorA[0]=0;
							dir_MotorA[1]=0;
							break;

					case 5: //Prueba de SMART THINGS

							switch(dirMotor){ //Switch anidado para el Smart Things

												case "Fw":	//Avanza
														dir_MotorA[0]=vel_prueba;
														dir_MotorA[1]=vel_prueba;
														break;

												case "Bw"://Atras
														dir_MotorA[0]=(-1*vel_prueba);
														dir_MotorA[1]=(-1*vel_prueba);
														break;

												case "R"://Giro Derecha
														dir_MotorA[0]=vel_prueba;
														dir_MotorA[1]=(-1*vel_prueba);
														break;

												case "L"://Giro Izquierda
														dir_MotorA[0]=(-1*vel_prueba);
														dir_MotorA[1]=vel_prueba;
														break;

												case "stop"://Alto
														dir_MotorA[0]=0;
														dir_MotorA[1]=0;
												break;

												default://Alto
														dir_MotorA[0]=0;
														dir_MotorA[1]=0;
														break;

							} //Fin del switch anidado para Smart Things
							break;

					default://Alto
							dir_MotorA[0]=0;
							dir_MotorA[1]=0;
							break;
	}//fin del switch-case
	cont++;
	temp=cont/100;

}//Fin de prueba motores


//_______________________________________________________________________________________________________________
//Función principal
int main(int  argc, char** argv){

	std::cout<<">>>>>LABORATORIO DE BIOROBÓTICA<<<<<<"<<std::endl;
	std::cout<<"_>>XOCHITONAL en linea para prueba de hardware ..."<<std::endl;
	ros::init(argc,argv,"XochitonalV2");//********************************************
	ros:: NodeHandle n;

    //Obtención de los datos transmitidos por los diferentes nodos 
 	ros::Subscriber subFoto = n.subscribe("/hardware/sensors/foto",1000,valorFoto); //Nodo Sensors/Fotoresistores
 	ros::Subscriber subEnc = n.subscribe("/hardware/sensors/enc",1000,valorEnc);; //Nodo Sensors/Encoders 
 	ros::Subscriber subDir = n.subscribe("/hardware/smartThings/dir", 1000,dirObtenida); //Nodo SmartThings


 	//Datos a publicar
	std_msgs::Float32MultiArray  D_Motor; //Dirección del motor
	D_Motor.data.resize(2);	

    //Publicación de las velocidades de los motores al Arduino
    ros::Publisher pubDir=n.advertise <std_msgs::Float32MultiArray>("/hardware/motor/direction",1);

	ros::Rate loop(1);
    ros::Rate r(10);
	
	while(ros::ok()){

	pruebaMotores(); //Se prueban los motores

		//Publicación de tópico de las direcciones
    D_Motor.data = dir_MotorA; //<-----
	std::cout<<D_Motor<<std::endl;

		pubDir.publish(D_Motor);  //Envió de las direcciónes al nodo Motor.py

		ros::spinOnce();
		loop.sleep();
        std::cout<<""<<std::endl;

	} //Fin del while(ROS)

return 0;
}//Fin del main principal