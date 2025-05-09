#include <stdio.h>
#include <stdlib.h> // Para usar atof()

int main(int argc, char *argv[]) {
    // Verificar que se pasaron los argumentos correctos
    if (argc != 3) {
        printf("Uso: ./suma <numero1> <numero2>\n");
        return 1;
    }

    // Convertir los argumentos a números enteros
    int numero1 = atof(argv[1]);
    int numero2 = atof(argv[2]);

    // Sumar los números
    int suma = numero1 + numero2;

    // Mostrar el resultado
    printf("La suma de %i y %i es: %i\n", numero1, numero2, suma);

    return 0;
}