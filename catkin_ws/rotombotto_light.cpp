/**********************************************************************
*	Garcés Marín Daniel 		
*	TESIS <Construcción de una plataforma robótica abierta para pruebas de desempeño de componentes y algoritmos>
*
*	<ROTOMBOTTO> Nodo seguimiento de luz
*		Nodo cuyo principal objetivo es ofrecer un comportamiento reactivo de seguimiento de luz.
*
*   Ultima versión: 4 de Marzo del 2019
**********************************************************************/

//>>>>>>>> LIBRERÍAS <<<<<<<<<<<<<
#include "ros/ros.h"
// ダ・ガ・マ・jû-san
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
float valor_foto=0; //Variable para la función valorFoto()
float vel_motores=125; //Velocidad estándar para los motores

	//Variables paraa guardar información de los tópicos
float datos_Foto[8]={0,0,0,0,0,0,0,0}; //Variable para la función valorFoto()
float dir_MotorA[2]={0.0,0.0}; //Variable para indicar los valores de dirección y velocidadesa los motores
//_____________________________________________________________________________________________________________________

//>>>>>>>>>>> FUNCIONES <<<<<<<<<<<

	//Obtención de los valores de los fotoresistores
void valorFoto(const std_msgs::Float32MultiArray::ConstPtr& dFoto){

	for(i=0;i<8;i++){ //Vaciado de los valores fotoresitores
		datos_Foto[i]=dFoto->data[i];
		std::cout<<"Fotoresitor["<<i<<"]:_ "<<datos_Foto[i]<<std::endl;	}//Fin Vaciado de los valores fotoresitores

	//Tratamiento de los datos:: Obteniedo valor más alto;
	valor_foto=0.0; //reinicio del valor mas alto
	for(i=0;i<8;i++){ //comparación de todos los valores prra saber el más alto

		if(valor_foto<=datos_Foto[i]){ //valor actual mayor
			num_fot=i;
			valor_foto=datos_Foto[i]; }	} //Fin de la busqueda mayor

	std::cout<<"Fuente de luz ubicada en fotoresitor["<<num_fot<<"]:: "<<valor_foto<<std::endl;		}//Fin de valorFoto
//------------------------------------------------------------------------------------------------------------------------

	//Funcion Seguimiento de la luz: Secuencia de movimiento Completamente reactivo usando solo el valor del fotoresistor mas alto
void lightSearch(){

	switch(num_fot){
					case 0: //Fuente de luz frente al objetivo
							dir_MotorA[0]=vel_prueba;
							dir_MotorA[1]=vel_prueba;
						break;

					case 1: //Fuente de luz derecha al objetivo
							dir_MotorA[0]=vel_prueba;
							dir_MotorA[1]=(-1*vel_prueba);
						break;

					case 2: //Fuente de luz detras al objetivo
							dir_MotorA[0]=(-1*vel_prueba);
							dir_MotorA[1]=(-1*vel_prueba);
						break;

					case 3://Fuente de luz izquierda al objetivo
							dir_MotorA[0]=(-1*vel_prueba);
							dir_MotorA[1]=vel_prueba;
						break;

					default: //ALTO, no hay nada claro
							dir_MotorA[0]=0;
							dir_MotorA[1]=0;
							break;
	}//Fin del switch case
}//Fin de la FUNCIÓN LIGHT SEARCH

//-------------------------------------------------------------------------------------------------------------------

	//Funcion Seguimiento de la luz: Secuencia la cual analiza el valor mas alto mas el de sus adyacentes
void lightSearch2(){

	float v_parcialFoto=0.0; //Valor que representa el 70% del valor mas alto de los 8 fotoresistores
	float valor_FotoIzq=0.0,valor_FotoDer=0.0; // Valores para almacenar los valores de los fotoresistores adyacentes
	int mov_temp=8;  //indicará el movimiento del robót que se implementará, está habilitado para la opción por default

	v_parcialFoto = (valor_foto*0.70); //Foto resistores con una diferencia de 10% del valor mas álto
	valor_FotoDer=datos_Foto[num_fot+1];
	valor_FotoIzq=datos_Foto[num_fot-1];
	std::cout<<" moviendose"<<std::endl;

	//Analisis de los datos recibidos

	if(valor_FotoIzq >= v_parcialFoto && valor_FotoDer >= v_parcialFoto){//Caso fuente de luz centrada (1° if)
		mov_temp=num_fot;	}//fin primer if

	//Caso en que la fuente de luz esta inclinada hacia el lado izquierda (2° if)
	else if(valor_FotoIzq>=v_parcialFoto && valor_FotoIzq > valor_FotoDer){
		mov_temp=valor_foto-1;	}//fin segundo if

	//Caso en que la fuente de luz esta inclinada hacia el lado izquierda (3° if)
	else if(valor_FotoDer >= v_parcialFoto && valor_FotoDer > valor_FotoIzq){
		mov_temp=valor_foto+1;	}//fin tercer if

	else{ //Caso en que no se puede verificar correctamente la ubicación de la fuente de luz
	 	mov_temp=8; }

	//Asignando el movimiento del robot
	switch(mov_temp){

					case 0: //Fuente de luz frente al objetivo
							dir_MotorA[0]=vel_motores;
							dir_MotorA[1]=vel_motores;
						break;

					case 1: //Fuente de luz frente derecha al objetivo
							dir_MotorA[0]=vel_motores;
							dir_MotorA[1]=(-1*vel_motores)/2;
						break;

					case 2: //Fuente de luz derecha al objetivo
							dir_MotorA[0]=vel_motores;
							dir_MotorA[1]=(-1*vel_motores);
						break;

					case 3: //Fuente de luz atras derecha al objetivo
							dir_MotorA[0]=(-1*vel_motores);
							dir_MotorA[1]=vel_motores/2;
						break;

					case 4: //Fuente de luz detras al objetivo
							dir_MotorA[0]=(-1*vel_motores);
							dir_MotorA[1]=(-1*vel_motores);
						break;

					case 5: //Fuente de luz atras izquierda al objetivo
							dir_MotorA[0]=vel_motores/2;
							dir_MotorA[1]=(-1*vel_motores);
						break;

					case 6: //Fuente de luz izquierda al objetivo
							dir_MotorA[0]=(-1*vel_motores);
							dir_MotorA[1]=vel_motores;
						break;	

					case 7: //Fuente de luz frente izquierda al objetivo
							dir_MotorA[0]=(-1*vel_motores)/2;
							dir_MotorA[1]=vel_motores;
						break;

					default:
							dir_MotorA[0]=0;
							dir_MotorA[1]=0;
							break;
	}//Fin del switch case "mov_temp"
}//Fin de la FUNCIÓN LIGHT SEARCH 2

//_______________________________________________________________________________________________________________
//Función principal
int main(int  argc, char** argv){

	std::cout<<">>>>>LABORATORIO DE BIOROBÓTICA<<<<<<"<<std::endl;
	std::cout<<"_>>XOCHITONAL en linea para seguimiento de una fuente luminosa..."<<std::endl;
	ros::init(argc,argv,"TeporingoV3");//********************************************
	ros:: NodeHandle n;

    //Obtención de los datos transmitidos por los diferentes nodos 
 	ros::Subscriber subFoto = n.subscribe("/hardware/sensors/foto",1000,valorFoto); //Nodo Sensors

 	//Datos a publicar
	std_msgs::Float32MultiArray  D_Motor; //Dirección del motor
	D_Motor.data.resize(2);	

    //Publicación de las velocidades de los motores al Arduino
    ros::Publisher pubDir=n.advertise <std_msgs::Float32MultiArray>("/hardware/motor/direction",1);

	ros::Rate loop(1); //10
    ros::Rate r(100); //1000
	
	while(ros::ok()){

		lightSearch(); //Analizando datos del fotoresistores para asignar el movimiento
		//lightSearch2(); //Analizando datos del fotoresistores para asignar el movimiento

		//Publicación de tópico de las direcciones
        D_Motor.data = dirMotor; 
		
		pubDir.publish(D_Motor);  //Envió de las direcciónes al nodo Motor.py

		ros::spinOnce();
		loop.sleep();
        std::cout<<""<<std::endl;
	} //Fin del while(ROS)

return 0;
}//Fin del main principal