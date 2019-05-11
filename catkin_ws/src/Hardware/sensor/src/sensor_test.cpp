/********************************************************************
*	Garcés Marín Daniel 		
*	TESIS <Construcción de una plataforma robótica abierta para pruebas de desempeño de componentes y algoritmos>
*
*	<HARDWARE> Nodo Sensor
*		El principal objetivo de este nodo es recuperar la información obtenida por el arduino y los sensores integrados a este
*		para posteriormente segmentarlos en diferentes tópicos.		
*		-- >>> NODO ESPECFICAMENTE PARA PRUEBAS DE HARDWARE <<<<<
*		
*   Ultima versión: 9 de Mayo del 2019
*********************************************************************/

// ダ・ガ・マ・jû-san
//>>>>>>>> LIBRERÍAS <<<<<<<<<<<<<
#include "ros/ros.h"
#include "std_msgs/Float32MultiArray.h"
#include <stdio.h>
#include <stdlib.h>
#include <termios.h>
#include <unistd.h>
#include <termio.h>
#include <sys/ioctl.h>
//----------------------------------------

	//>>>VARIABLES GLOBALES
int i=0, j=0; //varaibles para contadores
float val_Foto[4]={0,0,0,0}; //Valores de los sensores de luz
float val_Tempt=0; //Valores del sensor de temperatura

//_____________________________________________________________________
	//>>>FUNCIONES

void callbackArduino(const std_msgs::Float32MultiArray::ConstPtr& dataArduino){

	for(i=0;i<4;i++){ //Vaciando los datos de los sensores de luz
		val_Foto[i]=dataArduino->data[i]; 
		std::cout<<"Fotoresitor-"<<i<<":_ "<<val_Foto[i]<< std::endl;	}  //Fin del vaciado sensor luz

		val_Tempt=dataArduino->data[4]; 
		std::cout<<"Temperatura:_ "<<val_Tempt<< std::endl;

}//fin del callbackArduino

//_________________________________________________________________________

	//>>>FUNCIÓN MAIN PRINCIPAL
int main(int  argc, char** argv){

	//std::cout<<"     >>>>>LABORATORIO DE BIOROBÓTICA<<<<<<"<<std::endl;
	std::cout<<">_ROTOMBOTTO (SENSOR TEST NODE) en línea"<<std::endl;
	std::cout<<">_Recolectando datos...."<<std::endl;

	//_>Inicialiación del nodo de ROS); //Publicar datos enconders

	ros::init(argc,argv,"RotomBotto");
	ros:: NodeHandle n;

	//_>Obtención de los datos proporcionados por el arduino
 	ros::Subscriber subArd = n.subscribe("/hardware/arduino/data", 1000, callbackArduino); //Obtener los datos de lso sensores

	//_>Variables a publicar
	std_msgs::Float32MultiArray data_luz; //Datos de los fotoresistores
	data_luz.data.resize(4);	

	std_msgs::Float32MultiArray data_tempt; //Datos de los encoders
	data_tempt.data.resize(1);

	//_>Tópicos que se van a publicar con la información por separado
	ros::Publisher pubFoto=n.advertise <std_msgs::Float32MultiArray> ("/hardware/sensors/luz",10); //Publicar datos fotoresistores
	ros::Publisher pubEnc=n.advertise <std_msgs::Float32MultiArray> ("/hardware/sensors/tempt",10); //Publicar datos temperatura

	ros::Rate loop(10);
    ros::Rate r(1000);
	
	//Ciclo ROS
	while(ros::ok()){

		//Asignación de los valores para publicar
		for(i=0;i<4;i++){
		data_luz.data[i]=val_Foto[i];} //Sensores de luz

		data_tempt.data[0]=val_Tempt; //Encoders

		//Publicación de los tópicos
		pubFoto.publish(data_luz);
		pubEnc.publish(data_tempt);
        std::cout<<"Datos de sensores publicados correctamete"<<std::endl;


		ros::spinOnce();
		loop.sleep();
        std::cout<<""<<std::endl;

	} //Fin del while(ROS)

}//Fin del MAIN 