# ******************************************************************************
#
#  Copyright (c) 2019-2024 Axera Semiconductor Co., Ltd. All Rights Reserved.
#
#  This source file is the property of Axera Semiconductor Co., Ltd. and
#  may not be copied or distributed in any isomorphic form without the prior
#  written consent of Axera Semiconductor Co., Ltd.
#
# ******************************************************************************

$ErrorActionPreference = "Stop"

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}

if (Test-Path "pyAXCL.egg-info") {
    Remove-Item -Recurse -Force "pyAXCL.egg-info"
}

# 确保 wheel 包已安装
python -m pip install --upgrade pip wheel setuptools

python setup.py bdist_wheel --dist-dir ..\out\python

if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}

if (Test-Path "pyAXCL.egg-info") {
    Remove-Item -Recurse -Force "pyAXCL.egg-info"
}

