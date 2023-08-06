#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
Importa a Classe Serial
"""
from LibSerial1 import Serial

"""
Instancia o objeto Serial;
"""
serial = Serial( "COM1", 9600 );

"""
Chama os métodos do objeto serial;
"""
print("Comport: " 	+ serial.getComport()); 
print("BaudRate: " 	+ str(serial.getBaudRate())); 
print("Date: " 		+ str(serial.getTime())); 
print("Random: " 	+ str(serial.getRandom())); 