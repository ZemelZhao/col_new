import os
import sys

file_path = os.path.split(os.path.realpath(__file__))[0]
print(file_path)
os.system('python %s build' % os.path.join(file_path, 'setup.py'))

os.system('mv %s %s' %(os.path.join(file_path, 'build', 'lib.linux-x86_64-3.6', 'filter',
                                    '_filter.cpython-36m-x86_64-linux-gnu.so'),
                       os.path.join(file_path, '_filter.cpython-36m-x86_64-linux-gnu.so')))
