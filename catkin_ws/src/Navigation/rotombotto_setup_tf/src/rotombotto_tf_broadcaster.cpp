/**********************************************************************
* Garcés Marín Daniel     
* TESIS <Construcción de una plataforma robótica abierta para pruebas de desempeño de componentes y algoritmos>
*
* <NAVIGATION/SETUP_TF> Nodo para la creación del arbol de trasnformadas
*   El principal objetivo de este nodo es ofrecer los datos adecuados para la creación del arbotl de trasnformadas 
*   de la plataforma róbótica móvil con respecto a la localización del laser.
*
*   Ultima versión: 1 de Octubre del 2019
**********************************************************************/

//>>>>>>>> LIBRERÍAS <<<<<<<<<<<<<
// ダ・ガ・マ・jû-san
#include <ros/ros.h>
#include <tf/transform_broadcaster.h>

int main(int argc, char** argv){
  ros::init(argc, argv, "rotombotto_tf_publisher");
  ros::NodeHandle n;

  ros::Rate r(100);

  tf::TransformBroadcaster broadcaster;

  while(n.ok()){
    broadcaster.sendTransform(
      tf::StampedTransform(
        tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(0.1, 0.0, 0.2)),
        ros::Time::now(),"base_link", "base_laser"));
    r.sleep();
  }
}
