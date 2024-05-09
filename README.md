# pysyscalls
Script for adding direct or indirect syscalls for NtOpenProcess, NtAllocateVirtualMemory, NtProtectVirtualMemory, NtWriteVirtualMemory, NtReadVirtualMemory, and NtFreeVirtualMemory as winfunctype functions

## Examples

### Add Direct Syscalls

```python
import syscalls, ctypes, ctypes.wintypes
syscall.create_syscalls()
oa = syscall.OBJECT_ATTRIBUTES()
oa.Length = ctypes.sizeof(oa)
cid = syscall.CLIENT_ID()
pHandle = ctypes.wintypes.HANDLE(0)
cid.UniqueProcess = 508
syscall.NtOpenProcess(ctypes.byref(pHandle), syscalls.VmRead | syscalls.VmWrite | syscalls.VmOperation, ctypes.byref(oa), ctypes.byref(cid))
```

### Add Indirect syscalls

```python
import syscalls, ctypes, ctypes.wintypes
syscall.create_syscalls(indirect=True)
oa = syscall.OBJECT_ATTRIBUTES()
oa.Length = ctypes.sizeof(oa)
cid = syscall.CLIENT_ID()
pHandle = ctypes.wintypes.HANDLE(0)
cid.UniqueProcess = 508
syscall.NtOpenProcess(ctypes.byref(pHandle), syscalls.VmRead | syscalls.VmWrite | syscalls.VmOperation, ctypes.byref(oa), ctypes.byref(cid))
```
