import ctypes
import ctypes.wintypes

ntdll = ctypes.windll.ntdll
kernel32 = ctypes.windll.kernel32

VmRead = 0x0010
VmWrite = 0x0020
VmOperation = 0x0008
MemCommit = 0x00001000
MemReserve = 0x00002000
MemRelease = 0x00008000
PageExecuteRead = 0x20
PageExecuteReadWrite = 0x40
PageReadWrite = 0x04

kernel32.GetProcAddress.restype = ctypes.wintypes.HMODULE
kernel32.GetProcAddress.argtypes = [
    ctypes.wintypes.HMODULE, 
    ctypes.wintypes.LPCSTR
]

class UNICODE_STRING(ctypes.Structure):
    _fields_ = [
        ('Length', ctypes.wintypes.USHORT),
        ('MaximumLength', ctypes.wintypes.USHORT),
        ('Buffer', ctypes.wintypes.LPWSTR),
    ]

class OBJECT_ATTRIBUTES(ctypes.Structure):
    _fields_ = [
        ('Length', ctypes.wintypes.ULONG),
        ('RootDirectory', ctypes.wintypes.HANDLE),
        ('ObjectName', UNICODE_STRING),
        ('Attributes', ctypes.wintypes.ULONG)
    ]

class CLIENT_ID(ctypes.Structure):
    _fields_ = [
        ("UniqueProcess", ctypes.wintypes.HANDLE),
        ("UniqueThread", ctypes.wintypes.HANDLE)
    ]

def create_syscalls(indirect=False):

    sysAddrNtOpenProcess = kernel32.GetProcAddress(ntdll._handle, "NtOpenProcess".encode())
    sysAddrNtAllocateVirtualMemory = kernel32.GetProcAddress(ntdll._handle, "NtAllocateVirtualMemory".encode())
    sysAddrNtProtectVirtualMemory = kernel32.GetProcAddress(ntdll._handle, "NtProtectVirtualMemory".encode())
    sysAddrNtWriteVirtualMemory = kernel32.GetProcAddress(ntdll._handle, "NtWriteVirtualMemory".encode())
    sysAddrNtReadVirtualMemory = kernel32.GetProcAddress(ntdll._handle, "NtReadVirtualMemory".encode())
    sysAddrNtFreeVirtualMemory = kernel32.GetProcAddress(ntdll._handle, "NtFreeVirtualMemory".encode())

    if indirect:
        sysAddrNtOpenProcess += 0x12
        sysAddrNtAllocateVirtualMemory += 0x12
        sysAddrNtProtectVirtualMemory += 0x12
        sysAddrNtWriteVirtualMemory += 0x12
        sysAddrNtReadVirtualMemory += 0x12
        sysAddrNtFreeVirtualMemory += 0x12

    NtOpenProcessPrototype = ctypes.WINFUNCTYPE(
        ctypes.wintypes.HANDLE,
        ctypes.POINTER(ctypes.wintypes.HANDLE),
        ctypes.wintypes.ULONG,
        ctypes.c_void_p, # We have to use this because of a python ctypes bug ctypes.POINTER(OBJECT_ATTRIBUTES),
        ctypes.c_void_p, # We have to use this because of a python ctypes bug ctypes.POINTER(CLIENT_ID)
    )

    NtAllocateVirtualMemoryPrototype = ctypes.WINFUNCTYPE(
        ctypes.wintypes.HANDLE, 
        ctypes.wintypes.HANDLE,
        ctypes.POINTER(ctypes.wintypes.HANDLE), 
        ctypes.wintypes.HANDLE, 
        ctypes.POINTER(ctypes.wintypes.HANDLE), 
        ctypes.wintypes.ULONG, 
        ctypes.wintypes.ULONG
    )

    NtProtectVirtualMemoryPrototype = ctypes.WINFUNCTYPE(
        ctypes.wintypes.HANDLE,
        ctypes.wintypes.HANDLE,
        ctypes.POINTER(ctypes.wintypes.HANDLE),
        ctypes.POINTER(ctypes.wintypes.HANDLE),
        ctypes.wintypes.ULONG,
        ctypes.POINTER(ctypes.wintypes.ULONG)
    )

    NtWriteVirtualMemoryPrototype = ctypes.WINFUNCTYPE(
        ctypes.wintypes.HANDLE,
        ctypes.wintypes.HANDLE,
        ctypes.wintypes.HANDLE,
        ctypes.c_void_p,
        ctypes.c_uint32,
        ctypes.POINTER(ctypes.c_uint32)
    )

    NtReadVirtualMemoryPrototype = ctypes.WINFUNCTYPE(
        ctypes.wintypes.HANDLE,
        ctypes.wintypes.HANDLE,
        ctypes.wintypes.HANDLE,
        ctypes.c_void_p,
        ctypes.c_uint32,
        ctypes.POINTER(ctypes.c_uint32)
    )

    NtFreeVirtualMemoryPrototype = ctypes.WINFUNCTYPE(
        ctypes.wintypes.HANDLE,
        ctypes.wintypes.HANDLE,
        ctypes.POINTER(ctypes.wintypes.HANDLE),
        ctypes.POINTER(ctypes.wintypes.HANDLE),
        ctypes.wintypes.ULONG
    )

    globals()['NtOpenProcess'] = NtOpenProcessPrototype(sysAddrNtOpenProcess)
    globals()['NtAllocateVirtualMemory'] = NtAllocateVirtualMemoryPrototype(sysAddrNtAllocateVirtualMemory)
    globals()['NtProtectVirtualMemory'] = NtProtectVirtualMemoryPrototype(sysAddrNtProtectVirtualMemory)
    globals()['NtWriteVirtualMemory'] = NtWriteVirtualMemoryPrototype(sysAddrNtWriteVirtualMemory)
    globals()['NtReadVirtualMemory'] = NtReadVirtualMemoryPrototype(sysAddrNtReadVirtualMemory)
    globals()['NtFreeVirtualMemory'] = NtFreeVirtualMemoryPrototype(sysAddrNtFreeVirtualMemory)
