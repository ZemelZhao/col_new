# C python 混编

python对于list的处理速度实在太慢 需要使用C混编提速

这里主要是记录可能需要用到的相关部分



1. 由于python传入到C的变量默认为int 从C传出到python里面也会默认为int变量 故需要在python引入函数时对函数传入变量或传出变量进行定义

```python
import numpy as np
import ctypes 
func = lib.testFunc
func.argtypes = [np.cytpeslib.ndpointer(dtype=np.float64, ndim=1, flags = 'C_CONTIGUOUS'), ctypes.c_int, ctypes.c_double]
func.restype = ctypes.c_double
```

```c
double testFunc(double* data, int len, double src){
    return src;
}
```

2. 对于未来传入的数据是以bytes格式传递的 可以使用如下的方式传入到C中

```python
import ctypes 
data = b'ab1234'
func = lib.testFunc
func.argtypes = [ctypes.c_char_p, c_int]
func(data, len(data))
```

```c
void testFunc(char* data, int len){
    for(int i=0; i<len; i++){
        printf("%d\n", data[i]);
    }
}
```

