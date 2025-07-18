#include <math.h>
#include <stdio.h>
double calcular_Pearson_c(short *arreglo_x, short *arreglo_y, int N)
{
    double suma_x = 0;
    double sx = 0;
    double prom_x;
    for (int i = 0; i < N; i++)
    {
        suma_x = (double)arreglo_x[i] + suma_x;
    }
    prom_x = suma_x / N;

    for (int i = 0; i < N; i++)
    {
        sx = (((double)arreglo_x[i] - prom_x) * ((double)arreglo_x[i] - prom_x)) + sx;
    }
    sx = sqrt(sx);

    double suma_y = 0;
    double sy = 0;
    double prom_y;
    for (int i = 0; i < N; i++)
    {
        suma_y = (double)arreglo_y[i] + suma_y;
    }
    prom_y = suma_y / N;

    for (int i = 0; i < N; i++)
    {
        sy = (((double)arreglo_y[i] - prom_y) * ((double)arreglo_y[i] - prom_y)) + sy;
    }
    sy = sqrt(sy);

    double sxy = 0;
    for (int i = 0; i < N; i++)
    {
        sxy = ((double)arreglo_y[i] - prom_y) * ((double)arreglo_x[i] - prom_x) + sxy;
    }
    //    printf("%lf\n",sx);
    //    printf("%lf\n",sy);
    //    printf("%lf\n",sxy);
    //    printf("%lf\n",sxy/(sx*sy));
    return sxy / (sx * sy);
}

// gcc -FPic -shared lib_coef.c -o lib_coef.so -lm
// gcc -FPic -shared lib_coef.c -o lib_coef.so -lm -Os