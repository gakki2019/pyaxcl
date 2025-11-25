# !/usr/bin/env python
# -*- coding:utf-8 -*-
# ******************************************************************************
#
#  Copyright (c) 2019-2024 Axera Semiconductor Co., Ltd. All Rights Reserved.
#
#  This source file is the property of Axera Semiconductor Co., Ltd. and
#  may not be copied or distributed in any isomorphic form without the prior
#  written consent of Axera Semiconductor Co., Ltd.
#
# ******************************************************************************

import threading
import ctypes
import os
import sys
import platform
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(BASE_DIR, '..', '..')
sys.path.append(BASE_DIR)

from axcl.lib.config import *


def check_architecture():
    if platform.architecture()[0] != "64bit":
        print("pyAXCL requires a 64-bit Python interpreter.")
        sys.exit(1)


def _load_lib_axcl():
    lib = None
    lib_dir = get_axcl_lib_path()
    sys.path.append(lib_dir)

    is_windows = platform.system() == 'Windows'

    if is_windows:
        def load_dll(lib_name, optional=False):
            lib_full_name = f'{lib_name}.dll'
            try:
                return ctypes.CDLL(lib_full_name)
            except OSError:
                pass

            lib_dir_env = os.getenv('AXCL_LIB_PATH')
            if lib_dir_env:
                lib_path = os.path.join(lib_dir_env, lib_full_name)
                try:
                    return ctypes.CDLL(lib_path)
                except OSError as e:
                    if optional:
                        return None
                    raise OSError(f"Failed to load '{lib_full_name}' from AXCL_LIB_PATH: {lib_path}\n"
                                 f"Set AXCL_LIB_PATH or add DLL directory to PATH") from e

            if optional:
                return None
            raise OSError(f"Failed to load '{lib_full_name}': Not found in PATH and AXCL_LIB_PATH not set")

        for lib in ['libspdlog', 'libaxcl_logger', 'libaxcl_token', 'libaxcl_pcie_msg', 
                    'libaxcl_pcie_dma', 'libaxcl_comm']:
            load_dll(lib)
        load_dll('libaxcl_pkg', optional=True)

        lib_rt = load_dll('libaxcl_rt')
        lib_sys = load_dll('libaxcl_sys')
        lib_dmadim = load_dll('libaxcl_dmadim')
        lib_ivps = load_dll('libaxcl_ivps')
        lib_ive = load_dll('libaxcl_ive')
        lib_venc = load_dll('libaxcl_venc')
        lib_vdec = load_dll('libaxcl_vdec')
        lib_npu = load_dll('libaxcl_npu')

        if AXCL_USE_TEST_LIB:
            lib_stub = load_dll('libaxcl_stub')
            return (lib_stub,) * 8

        return lib_rt, lib_sys, lib_dmadim, lib_ivps, lib_ive, lib_venc, lib_vdec, lib_npu
    else:
        ld_libray_path = os.environ.get('LD_LIBRARY_PATH')
        if ld_libray_path:
            if ld_libray_path.find(lib_dir) == -1:
                ld_libray_path = f'{ld_libray_path}:{lib_dir}'
        else:
            ld_libray_path = f'{lib_dir}'

        os.environ['LD_LIBRARY_PATH'] = ld_libray_path

        _ = ctypes.CDLL(os.path.join(lib_dir, 'libspdlog.so'), mode=os.RTLD_LAZY)
        _ = ctypes.CDLL(os.path.join(lib_dir, 'libaxcl_logger.so'), mode=os.RTLD_LAZY)
        _ = ctypes.CDLL(os.path.join(lib_dir, 'libaxcl_token.so'), mode=ctypes.RTLD_GLOBAL)
        _ = ctypes.CDLL(os.path.join(lib_dir, 'libaxcl_pcie_msg.so'), mode=ctypes.RTLD_GLOBAL)
        _ = ctypes.CDLL(os.path.join(lib_dir, 'libaxcl_pcie_dma.so'), mode=ctypes.RTLD_GLOBAL)
        _ = ctypes.CDLL(os.path.join(lib_dir, 'libaxcl_comm.so'), mode=ctypes.RTLD_GLOBAL)
        _ = ctypes.CDLL(os.path.join(lib_dir, 'libaxcl_pkg.so'), mode=ctypes.RTLD_GLOBAL)


        lib_rt = ctypes.CDLL(os.path.join(lib_dir, 'libaxcl_rt.so'), mode=ctypes.RTLD_GLOBAL)
        lib_sys = ctypes.CDLL(os.path.join(lib_dir, 'libaxcl_sys.so'), mode=ctypes.RTLD_GLOBAL)
        lib_dmadim = ctypes.CDLL(os.path.join(lib_dir, 'libaxcl_dmadim.so'), mode=ctypes.RTLD_GLOBAL)
        lib_ivps = ctypes.CDLL(os.path.join(lib_dir, 'libaxcl_ivps.so'), mode=ctypes.RTLD_GLOBAL)
        lib_ive = ctypes.CDLL(os.path.join(lib_dir, 'libaxcl_ive.so'), mode=ctypes.RTLD_GLOBAL)
        lib_venc = ctypes.CDLL(os.path.join(lib_dir, 'libaxcl_venc.so'), mode=ctypes.RTLD_GLOBAL)
        lib_vdec = ctypes.CDLL(os.path.join(lib_dir, 'libaxcl_vdec.so'), mode=ctypes.RTLD_GLOBAL)
        lib_npu = ctypes.CDLL(os.path.join(lib_dir, 'libaxcl_npu.so'), mode=ctypes.RTLD_GLOBAL)

        if AXCL_USE_TEST_LIB:
            lib_stub = ctypes.CDLL(os.path.join(lib_dir, 'libaxcl_stub.so'), mode=ctypes.RTLD_GLOBAL)
            lib_rt = lib_stub
            lib_sys = lib_stub
            lib_dmadim = lib_stub
            lib_ivps = lib_stub
            lib_ive = lib_stub
            lib_venc = lib_stub
            lib_vdec = lib_stub
            lib_npu = lib_stub

        return lib_rt, lib_sys, lib_dmadim, lib_ivps, lib_ive, lib_venc, lib_vdec, lib_npu


class _AxclLib(object):
    check_architecture()

    _instance_lock=threading.Lock()
    lib_rt, lib_sys, lib_dmadim, lib_ivps, lib_ive, lib_venc, lib_vdec, lib_npu = _load_lib_axcl()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(_AxclLib, "_instance"):
            with _AxclLib._instance_lock:
                if not hasattr(_AxclLib, "_instance"):
                    _AxclLib._instance=object.__new__(
                        cls, *args, **kwargs)
        return _AxclLib._instance

libaxcl_rt = _AxclLib.lib_rt
libaxcl_sys = _AxclLib.lib_sys
libaxcl_dmadim = _AxclLib.lib_dmadim
libaxcl_ivps = _AxclLib.lib_ivps
libaxcl_ive = _AxclLib.lib_ive
libaxcl_venc = _AxclLib.lib_venc
libaxcl_vdec = _AxclLib.lib_vdec
libaxcl_npu = _AxclLib.lib_npu
