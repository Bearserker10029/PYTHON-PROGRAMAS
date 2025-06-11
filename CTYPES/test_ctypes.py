import ctypes
import math
if __name__ == '__main__':

    a = 10
    b = 20
    c = 30

    lib = ctypes.CDLL('./lib_suma.so')
    lib.suma.argtypes = [ctypes.c_int32,ctypes.c_int32,ctypes.c_int32]
    lib.suma.restype = ctypes.c_int32

    print(lib.suma(a,b,c))

    lib.suma_max.argtypes = [ctypes.c_ulonglong, ctypes.c_ulonglong, ctypes.c_ulonglong,ctypes.c_ulonglong]
    lib.suma_max.restype = ctypes.c_ulonglong
    d = 2**9
    print(lib.suma_max(a,b,c,d))

    lib.operacion.argtypes = [ctypes.c_double,ctypes.c_double]
    lib.operacion.restype = ctypes.c_double    

    print(lib.operacion(math.pi,math.e))