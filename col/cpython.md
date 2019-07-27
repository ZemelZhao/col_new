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
func.argtypes = [ctypes.c_char_p, ctypes.c_int]
func(data, len(data))
```

```c
void testFunc(char* data, int len){
    for(int i=0; i<len; i++){
        printf("%d\n", data[i]);
    }
}
```

3. 对于未来传入的数据是以numpy.array的形式传入C中

```python
import ctypes
import numpy as np
func = lib.testFunc
func.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS), ctypes.c_int]
data = np.arange(0, 10)
func(data, data.shape[0])
```

```cpp
void testFunc(double* data, int len){
    for (int i=0; i<len; i++){
        data[i] = data[i]*2
    }
}
```

这里值得注意的是在c中创建一个python的numpy.array是一件极为麻烦的事情 但是可以在python中创建完之后放到C中 C会把这个作为一个正常的数组指针去处理 如果需要可以把需要结果重新赋值给这个数组 这个是可以在python中直接读取的 因为这两部分是共用同一块内存空间。这样可以避免在C中算完的数组python拿回来的指针根本无法正常使用 必须再一一赋值给数组才能正常使用 这样可以极大的提高效率

4. 对于打包成python可使用的动态链接库

```python
# setup.py
# python setup.py build
def configuration(parent_package='', top_path=None):
    """DocString for configuration"""
    #@todo: to be defined.
    #:parent_package='': @todo.
    #:top_path=None: @todo.
    from numpy.distutils.misc_util import Configuration
    config = Configuration('testp', parent_package, top_path)
    config.add_extension('_test', sources=['testc.cpp'])

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(configuration=configuration)
```

第一行注释表示的是这个的文件名 第二行表示的是使用这个setup.py的方法

之后就可以在build文件夹下找到一个.so文件 这个就是可以使用的动态链接库

如果不使用setup.py也可以生成动态链接库 但是这个使用该.so文档的.py文件是无法被其他.py文件import的 这里会报ImportError的。

5. 针对cpp文件 也是可以正常使用的

这里可以先申请一个cpp的class 但是如果包装城动态链接库 必须使用extern “C“

```cpp
class A{
    public:
    int a = 3; 
    int b = 5;
}
extern "C"{
    A data;
    int funcA(void){
        return data.a;
    }
    void funcB(int a){
        return a*data.b;
    }
}
```

