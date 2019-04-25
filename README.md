# RotomBotto

Construcción de una plataforma robótica abierta para pruebas de desempeño de componentes y algoritmos.
Daniel Garcés Marín

Director de tesis: Marco Antonio Negrete Villanueva

En colaboración con el Laboratorio de Biorobótica de la Facultad de Ingeniería de la UNAM.

=> Objetivo general

Diseño e implementación de una plataforma robótica abierta para uso docente y de investigación que ofrezca a aquellos inmersos en el campo de la robótica, características equivalentes a aquellas plataformas comerciales ofrecidas por empresas privadas, con la ventaja de que tanto el diseño en hardware y en software puede ser modificado por el usuario, adaptando el diseño de la plataforma robótica, a nivel de hardware, para disminuir su costo y hacerla más accesible.

=>Objetivos particulares

- Desarrollar una plataforma robótica móvil siguiendo las metodologías de la iniciativa Open Source en cuestión de diseño de hardware y software.
- Documentar el diseño y características de todos los elementos mecánicos, eléctricos y electrónicos que se requieren para la construcción de una plataforma robótica base, así como el proceso de construcción de la misma.
- Desarrollar una arquitectura de software implementada en ROS con los algoritmos necesarios con el que se pueda tener un correcto funciona miento de los componentes incluidos en la plataforma.
-Ofrecer alternativas para la construcción de la plataforma en caso de no contar con los elementos sugeridos y ofrecer soporte en la plataforma de software para dichos elementos.
- Implementar algoritmos usados en temas de navegación, visión computacional y planeación de acciones; consecuentemente implementar algoritmos para la calibración, adecuación y caracterización de sensores, así como el análisis de la información recopilada por l


=> Organización del repositorio


A continuación se describirán brevemente la organización y el contenido del repositorio.

- [Arduino_files]: En esta carpeta se encuentra los archivos que se utilizarán para la programación del Arduino Mega utilizado en el robot, además de un diagrama de conexiones con los sensores.

- [catkin_ws]: Carpeta que contiene el workspace de ROS del sistema de la plataforma robótica móvil y donde se encuentra la mayor parte de la arquitectura del robot.

- [Manufactura]: Carpeta que contendrá los archivos de las caracasa protectoresy los diagramas con los que se diseño el chasis de la plataforma robótica móvil para que el usuario sea capaz de disponer de sus propios elementos cuando se requiera. 

- [Media_RotomBotto]: En esta carpeta se guardará evidencia fotográfica y videográfica de la paltaforma robotica móvil.

- [RaspberryPi_SD_Image]: En esta carpeta se guardará una copia del SO utilizado para la implementación del software de la plataforma robótica móvil en la tarjeta Raspberry Pi 3 para una instalación más directa del proyecto desarrollado.

