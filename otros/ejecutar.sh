#!/bin/bash

# Ejecutar el programa en Python
echo "Ejecutando el programa en Python..."
python3 ejercicio1.py

# Ejecutar el programa en C
echo "Ejecutando el programa en C..."
gcc -o suma_nueva ejercicio1.c
./suma_nueva