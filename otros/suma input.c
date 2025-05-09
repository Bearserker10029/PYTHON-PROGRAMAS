#include <stdio.h>
#include <math.h>

int main() {
    int num_1, num_2, suma;

    // Leer numeros
    printf("Introduce num 1: ");
    scanf("%i", &num_1);

    printf("Introduce num 2: ");
    scanf("%i", &num_2);

    // Calcular la suma
    suma = num_1 + num_2;

    printf("La suma total es: %i\n", suma);

    return 0;
}