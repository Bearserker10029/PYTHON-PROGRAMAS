Cómo usar mprof para medir huella de memoria
mprof es una herramienta del paquete memory_profiler que permite perfilar la memoria de procesos de Python en tiempo real y generar gráficos visuales.

1. Perfilado de scripts normales (sync, async, thread, thread pool)
```
mprof run html_fetch_sync.py
mprof run html_fetch_async.py
mprof run html_fetch_thread.py
mprof run html_fetch_thread_pool.py
```

Luego, para graficar:

```
mprof plot
```
Esto abrirá una ventana con el gráfico de uso de memoria a lo largo del tiempo.

Perfilado de versiones multiproceso (multiprocessing)
El perfilado estándar no captura los subprocesos. Para eso:

```
mprof run --multiprocess html_fetch_process.py
mprof run --multiprocess html_fetch_process_pool.py
```
Esto permitirá registrar la memoria usada por cada proceso generado. Sin esta opción, los procesos secundarios no se incluirán en la medición.

La opción --multiprocess solo está disponible a partir de memory_profiler>=0.61, por eso está incluida en los requisitos.

Consejos adicionales
Si haces múltiples pruebas, mprof generará múltiples archivos (.dat). Puedes eliminarlos con:

```
mprof clean
```

Puedes exportar los gráficos como imágenes con:

```
mprof plot -o memoria.png
```
