
double ordenac(int N, double *arreglo, double *arreglo_salida){
    double numcopia;
    for(int i=0; i<(N/4); i++)
    {
        for (int j=0; j<4;j++){
            if (j==3){
                numcopia=arreglo[i*4+j];
                arreglo_salida[i*4+j]=arreglo[i*4];
                arreglo_salida[i*4]=numcopia;
            }
            else{
                arreglo_salida[i*4+j]=arreglo[i*4+j];
            }
        }
    }

return *arreglo_salida;
}
