@echo off

set SOFTWARE_FOLDER=.cuprocell
set CUPROCELL_ROOT=%localappdata%\%SOFTWARE_FOLDER%
set CUPROCELL_URL=https://github.com/ericniso/cuda-pro-cell.git
set CUPROCELL=cuprocell
set GPU_ARCH=sm_35
set SOLUTION_NAME=procell.sln

if exist %CUPROCELL_ROOT% (
    rmdir %CUPROCELL_ROOT% /s /q
)

echo Creating %CUPROCELL_ROOT% directory...

mkdir %CUPROCELL_ROOT%

echo Entering %CUPROCELL_ROOT% directory...

cd %CUPROCELL_ROOT%

git clone %CUPROCELL_URL% %CUPROCELL%

cd %CUPROCELL%

mkdir build

cd build

cmake -DCMAKE_CUDA_FLAGS="-arch="%GPU_ARCH% -DCMAKE_GENERATOR_PLATFORM=x64 ..