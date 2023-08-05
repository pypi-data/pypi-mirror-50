from distutils.core import setup, Extension
import os

version = os.environ.get('PYDINEMIC_VERSION')

pydinemic = None
if os.path.exists('/usr/lib/x86_64-linux-gnu/libboost_python-py36.so'):
    pydinemic = Extension('pydinemic',
                          sources=['src/pydinemic/module.cpp',
                                   'src/pydinemic/pyaction.cpp',
                                   'src/pydinemic/pydfield.cpp',
                                   'src/pydinemic/pydlist.cpp',
                                   'src/pydinemic/pydmodel.cpp'],
                          include_dirs=['/usr/include', 'src/pydinemic'],
                          library_dirs=['/usr/lib/x86_64-linux-gnu/'],
                          runtime_library_dirs=['/usr/lib/x86_64-linux-gnu/'],
                          libraries=['boost_python3', 'dinemic'])
elif os.path.exists('/usr/lib/x86_64-linux-gnu/libboost_python-py35.so'):
    pydinemic = Extension('pydinemic',
                          sources=['src/pydinemic/module.cpp',
                                   'src/pydinemic/pyaction.cpp',
                                   'src/pydinemic/pydfield.cpp',
                                   'src/pydinemic/pydlist.cpp',
                                   'src/pydinemic/pydmodel.cpp'],
                          include_dirs=['/usr/include'],
                          library_dirs=['/usr/lib/x86_64-linux-gnu/'],
                          runtime_library_dirs=['/usr/lib/x86_64-linux-gnu/'],
                          libraries=['boost_python-py36', 'dinemic'])
elif os.path.exists('/usr/lib/x86_64-linux-gnu/libboost_python-py36.so'):
    pydinemic = Extension('pydinemic',
                          sources=['src/pydinemic/module.cpp',
                                   'src/pydinemic/pyaction.cpp',
                                   'src/pydinemic/pydfield.cpp',
                                   'src/pydinemic/pydlist.cpp',
                                   'src/pydinemic/pydmodel.cpp'],
                          include_dirs=['/usr/include'],
                          library_dirs=['/usr/lib/x86_64-linux-gnu/'],
                          runtime_library_dirs=['/usr/lib/x86_64-linux-gnu/'],
                          libraries=['boost_python-py36', 'dinemic'])
elif os.path.exists('/usr/lib/x86_64-linux-gnu/libboost_python-py36.so'):
    pydinemic = Extension('pydinemic',
                          sources=['src/pydinemic/module.cpp',
                                   'src/pydinemic/pyaction.cpp',
                                   'src/pydinemic/pydfield.cpp',
                                   'src/pydinemic/pydlist.cpp',
                                   'src/pydinemic/pydmodel.cpp'],
                          include_dirs=['/usr/include'],
                          library_dirs=['/usr/lib/x86_64-linux-gnu/'],
                          runtime_library_dirs=['/usr/lib/x86_64-linux-gnu/'],
                          libraries=['boost_python-py37', 'dinemic'])
else:
    print('Failed to find boost::python libraries. Check in your system')

setup(name='pydinemic',
      version='19.07.6',
      author='cloudover.io ltd.',
      description='Dinemic framework for python',
      package_dir={'': 'src'},
      packages=['pkg'],
      headers=['src/pydinemic/module.h',
               'src/pydinemic/pyaction.h',
               'src/pydinemic/pydfield.h',
               'src/pydinemic/pydlist.h',
               'src/pydinemic/pydmodel.h',
               'src/pydinemic/pyaction.h'],
      ext_modules=[pydinemic])
