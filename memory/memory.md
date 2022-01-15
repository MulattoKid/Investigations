# Memory

## Physical Memory
This is the physical memory installed in your system, typically at least 4 GiB in most modern non-embedded systems (mobile devices, laptops, PCs, consoles etc.).

The amount of physical memory a system can support is limited by the bitness of the CPU and OS. The maximums are as follows:
- 16-bit = 2^16 = 65536 bytes = 64 KiB
- 32-bit = 2^32 = 4294967296 bytes = 4 GiB
- 64-bit = 2^64 = 1.8446744e+19 bytes = 16777216 TiB

## Virtual Memory
In a system without virtual memory, a process' addresses would point directly to physical memory addresses. And in the case of all the processes running on a system requiring more than the available physical memory, the system would crash. To avoid this problem (and others), virtual memory (addressing) is used. To understand how it works we start from the bottom and work our way up.

### Physical Memory Frames
The physical memory, say 1024 bytes, is split into several frames, each of say 128 bytes. This gives us 8 frames with a address range of 128 bytes. Each of these address ranges is called a frame, and corresponds to a physical address region in physical memory.

### Virtual Address
Each process has a given size of memory it can use, it's virtual memory. This virtual memory doesn't necessarily correspond to some address in physical memory. When a process want to access virtual address 0x1, a page number and page offset are generated from the virtual address.

The page number and offset are generated based on the virtual address space and the frame/page size. E.g. if the virtual address space is 32-bit, and the frame/page size is 8-bit (256 bytes per frame/page), then the first 24 bits of a virtual address will be the page number, and the last 8 bits will be the page offset.

Since each process has the same virtual address space, they can all generate the same page numbers, which in theory would map to the same frame. To avoid this issue, each process has its own page table.

### Page Table
The page table is responsible for mapping a requested page to the corresponding frame it's located in. Let's say that virtual addres 0x1 generates page number 0 and page offset 1. If page 0 is located in physical memory, the corresponding frame is accessed at the page offset.

### Page Fault
If page 0 isn't located in physical memory (i.e. it's paged out to disk), a page fault is generated. This will page in a data range (the size of a frame) from disk to a frame. The data which was already in the frame is conversely paged out.

### Translation Look Aside Buffer
The page table itself resides in physical memory, and can in cases with many running processes that allocate a lot of memory become quite large. So, to speed up page table look-ups a cache (TLB) is used. It works as any other cache, by checking if the mapping from page number to frame is present. If it is, we can access the frame at the page offset directly. If the page number isn't present, we must go through the page table.