#include <stdio.h>
void test_cache (double *a, double *b, double *c, double *d, int N, int M)
{   
    //printf("%p \n",a);
    //printf("%p \n",b);
    int i,j;
	for (i = 0;i < N; i = i + 1){
		for (j = 0; j < M; j = j + 1) {
			a[i+M*j] = 2/b[i+M*j] *c[i+M*j];
			d[i+M*j] = a[i+M*j] + c[i+M*j];
		}
	}
}
void test_cache2 (double *a, double *b, double *c, double *d, int N, int M)
{   //printf("%p \n",a);
    //printf("%p \n",b);
	int i,j;
	for (i = 0;i < N; i = i + 1){
		for (j = 0; j < M; j = j + 1) {
			a[i+M*j] = 2/b[i+M*j] *c[i+M*j];
		}
	}
	
    for (i = 0;i < N; i = i + 1){
		for (j = 0; j < M; j = j + 1){
			d[i+M*j] = a[i+M*j] + c[i+M*j];
		}
	}
    
}
    