void modifica_arreglo_c(char *arreglo_in, char *arreglo_out, int N)
{
    for (int i = 0; i < N; i++)
    {
        arreglo_out[i] = arreglo_in[i] * 10;
    }
}

void modifica_arreglo_c_float(float *arreglo_in, float *arreglo_out, int N)
{
    for (int i = 0; i < N; i++)
    {
        arreglo_out[i] = arreglo_in[i] * 10;
    }
}