Software installation guide.

1) Operating system. Prefereable is 

Linux Ubuntu 12 or higher. 

In principle, all the used software can be used under other OSes, however installation pecularities  you should figure out yourself, 

2) Python 2.7 (not Python 3!) - installed at Ubuntu 14.x by default. Check it by typing 

> python

in terminal. It will output python version, it should be 2.7.x

Additionally run

> sudo sudo apt-get install python-pip
> sudo pip install numpy

(or 
>  pip install --user numpy

if you install it for you only - in this case sudo rights are not needed. 
)

Check that nympy is installed by typing 

> python -c "import numpy"

There should not be any error message. Repeat for other packages.

2.1) Other python packeges:

cython:

> sudo pip install cython

h5py:

> sudo pip install h5py

matplotlib:
> sudo apt-get install libfreetype6-dev libxft-dev
> sudo pip install matplotlib

3) HDF5. Install library and viewer from Ubuntu software repository: 

> sudo apt-get install libhdf5-serial-dev
> sudo apt-get install hdfview
> sudo apt-get install hdf5-tools

4) CPLEX ILP solver (academic license only !). Read here how to register and download it (or ask me for a CD to install it at the university):

https://www.ibm.com/developerworks/community/blogs/jfp/entry/cplex_studio_in_ibm_academic_initiative?lang=en

5) BOOST library:

> sudo apt-get install libboost-all-dev

6) OpenGM (github version): http://hci.iwr.uni-heidelberg.de/opengm2/?l0=library

  >git clone https://github.com/opengm/opengm.git

Roll back to a compilable version (the latest one currently is not compilable)

  >git checkout 964ccc53441f3a9e8f5af9324ad31c5771cc3f81

use cmake-gui .  to configure and generate makefile

>cd opengm
opengm> cmake-gui .

Select "Grouped" and "Advanced" in the top-right corner and press "Configure"

In submenus select:

BUILD:

BUILD_COMMANDLINE
BUILD_EXAMPLES
BUILD_TUTORIALS
BUILD_PYTHON_WRAPPER

WITH:

WITH_BOOST
WITH_CONICBUNDLE
WITH_CPLEX
WITH_HDF5
WITH_MAXFLOW
WITH_MAXFLOW_IBSF
WITH_QPBO
WITH_TRWS
WITH_MRF

and run Configure. Read the output errors. Most probably, you will be asked to provide a path to the CPLEX/CONCERT library. Do it like in this picture:
http://cvlab-dresden.de/HTML/people/bogdan/teaching/slides-script/ml2-ss15/cmake-gui-screen.png

Run Generate.

Probably after running Configure you were asked to run 'make externalLibs'. Do it in the build folder of opengm:

opengm> make externalLibs

Then get back to cmake-gui:

opengm> cmake-gui

and press again Configure and afterwards Generate.

>----------------Remark: ---------------------------------
Sometimes an error message pops up duing make file generation:

>   Could NOT find HDF5 (missing: HDF5_SUFFICIENT_VERSION)
> Call Stack (most recent call first):
>   /usr/share/cmake-2.8/Modules/FindPackageHandleStandardArgs.cmake:252
> (_FPHSA_FAILURE_MESSAGE)
>   cmake/modules/FindHDF5.cmake:63 (FIND_PACKAGE_HANDLE_STANDARD_ARGS)
>   CMakeLists.txt:177 (find_package)

To fix it in cmake/modules/FindHDF5.cmake in the line:

FIND_PACKAGE_HANDLE_STANDARD_ARGS(HDF5 DEFAULT_MSG HDF5_CORE_LIBRARY
        HDF5_HL_LIBRARY HDF5_ZLIB_OK HDF5_SZLIB_OK HDF5_INCLUDE_DIR HDF5_SUFFICIENT_VERSION)

the HDF5_SUFFICIENT_VERSION to be removed.
>------------------------------------------------------------

Now make it:

opengm> make

(you might run 
opengm> make -j4 
instead of the last command, if you have 4 cores - it speeds up building significantly)

The last installation command:

opengm> sudo make install


8) Check that python works with OpenGM. The command

> python -c "import opengm"

should not return any error (should not return basically anything).



