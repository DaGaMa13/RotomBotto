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

- [catkin_ws]: Carpeta que contiene el workspace de ROS del sistema de la plataforma robótica móvil y donde se encuentra la mayor parte de la arquitectura del robot.


- [Rotombotto_Documentación]: Carpeta que contendrá los archivos donde se registró el desarrollo total del proyecto, el contenido de esta carpeta se divide en:

	*<Rotombotto_Diagramas&Esquematicos>: En esta carpeta se almacenan los diagramas y esquemáticos que se desarrollaron para documentan la contrucción adecuada de la plataforma robótica móvil.
	*<Rotombotto_Media&Evidencias>: En esta carpeta se almacenan los archivos fotográficos y videográficos que servirán como evidencia del proyecto de la plataforma robótica.
	*Tesis_Plataforma_Robótica_DGM: El documento de tesis que se presentó durante el desarrollo de la plataforma robótica por parte del creador del presente proyecto y su servidor. 


- [RotombottoManufactura&desarrollo]: Carpeta que contendrá los archivos para la reproducción de algunos de los componentes de la plataforma robótica de diseño o modificación propia y los cuales pueden ser modificados por el usuario en función de sus necesidades; el contenido de esta carpeta se divide en:

	*<Rotombotto_DiseñoChasis>: En esta carpeta se almacenan los archivos del diseño del chasis báse utilizado para la plataforma rovótica móvil.
	*<Rotombotto_Impresión_3D>: En esta carpeta se almacenan los archivos del diseño de las caracasaa protectoras y otros componentes cuyos modelos fueron diseñados para ser manufacturados por medio de impresión 3D.
	*<Rotombotto_PCB>: En esta carpeta se almacenan los archivos del diseño para placas PCB para la conexion con los componentes electrónicos involucrados con el dispositivo Arduino MEGA.


- [RotomBotto_Programación_componentes]:  Carpeta que contendrá los archivos para la programación de las unidades de procesamiento que componen la plataforma robótica móvil, el contenido de esta carpeta se divide en:

	*<Arduino_files>: En esta carpeta se almacena el archivo de extensión ".ino" para la programación del Arduino MEGA.
	*<RaspberryPi_SD_Image>: En esta carpeta se almacena una copia del SO utilizado para la implementación del software de la plataforma robótica móvil en la tarjeta Raspberry Pi 3 para una instalación más directa del proyecto desarrollado.

