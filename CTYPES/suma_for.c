#include <stdio.h>
#include <time.h>
float sumaFor(int N)
{
    int suma = 0;
    for (int i = 1; i <= N; i++)
    {
        suma += (float)i;
    }
    return suma;
}

int main()
{
    // srandom(time(NULL));

    struct timespec ti, tf;
    double elapsed;
    clock_gettime(CLOCK_REALTIME, &ti);
    sumaFor(1024);
    clock_gettime(CLOCK_REALTIME, &tf);
    elapsed = (tf.tv_sec - ti.tv_sec) * 1e9 + (tf.tv_nsec - ti.tv_nsec);
    printf("Tiempo de ejecución %lf ns\n", elapsed);
    return 0;
}