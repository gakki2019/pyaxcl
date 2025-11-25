@echo off
REM ******************************************************************************
REM
REM  Copyright (c) 2019-2024 Axera Semiconductor Co., Ltd. All Rights Reserved.
REM
REM  This source file is the property of Axera Semiconductor Co., Ltd. and
REM  may not be copied or distributed in any isomorphic form without the prior
REM  written consent of Axera Semiconductor Co., Ltd.
REM
REM ******************************************************************************

setlocal

cd /d "%~dp0"

if exist "dist" (
    rmdir /s /q "dist"
)

if exist "build" (
    rmdir /s /q "build"
)

if exist "pyAXCL.egg-info" (
    rmdir /s /q "pyAXCL.egg-info"
)

REM 确保 wheel 包已安装
python -m pip install --upgrade pip wheel setuptools

python setup.py bdist_wheel --dist-dir ..\out\python

if exist "build" (
    rmdir /s /q "build"
)

if exist "pyAXCL.egg-info" (
    rmdir /s /q "pyAXCL.egg-info"
)

endlocal

