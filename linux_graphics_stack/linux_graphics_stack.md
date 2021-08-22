# Linux Graphics Stack

## fbdev
The Linux Framebuffer (fbdev) is a HW independent abstraction layer to show graphics on a computer monitor. It is much simpler than other ways of showing graphics, as it allows direct access to the framebuffer using the kernel and the associated device file system interface. fbdev has three main applications:
- A text console that doesn't use HW text mode
- Output for a display server, e.g. X (descriped below)
- Other graphics programs circumventing the display server

It sees quite a bit of use in embedded system that don't necessarily have grahpics HW, or decides to not use it for some reason.

Links:
- https://en.wikipedia.org/wiki/Linux_framebuffer

## X Windowing System
Jargon:
- X Windowing System: the entire framework
- X: the entire framework
- X11: the X communiation protocol has been at version *11* since 1987
- Xorg: the reference X Server implementation developed and maintained by the X.org Foundation
- Xlib: the client implementation of X11
- XCB: an alternative client implementation of X11
- DDX: Device Dependent X driver (drivers written for specific HW)
- GLX: an extension to X which added support for OpenGL

The design of X is a server-client model. The X Server (Xorg) runs and is connected to both IO peripherals (e.g. mouse,keyboard, screen), and a number of X clients (applications with a GUI). The clients communicate with the server to
update the screen, and the server communicates with the clients to share e.g. mouse updates.

The protocol by which the server and clients communicate (X11) is network transparent, meaning the server and clients can either run on the same machine, or on different machines connected over a network.

Ignoring the remote option, let's focus on the local scenario. The Xorg server will be running on the machine, and applications will make use of the X11 protocol to communicate with Xorg. To do this they will include the necessary headers (<X11/Xlib.h>), and link against *Xlib* (-lX11); that's it. There is also an alternative to Xlib: XCB. It also implements the X11 protocol, and aims to be smaller and less complex than Xlib.

The way X worked is kind of similar to how I envision modern graphics APIs work: the application makes various API calls which are received by the graphics driver, and translated into commands the GPU will execute (very simplified). With X, applications send rendering commands via X11 to Xorg, which translates these into commands the graphics HW will execute. Xorg therefore acts as a modern graphics driver. However, Xorg doesn't know which graphics HW it may be connected to, so how can it possibly translate the X commands into correct HW commands? Well, all graphics HW that wanted to support X needed an X driver specifically written for its HW (DDX). These HW drivers became modules in Xorg, running "inside" Xorg.

So, an applications makes an X API call, which is sent over X11 to Xorg. Xorg then shares this API call with the HW specific driver which executes the command on the HW.

However, with the introduction of specific 3D rendering APIs, such as OpenGL, this changed. OpenGL is designed to communicate "directly" with the graphics HW through a *libGL* (as described above). However, since all rendering communication is going through X, so must OpenGL. The solution to this was to create GLX, an extension to X. GLX added support for sending OpenGL commands from clients over X11 to Xorg. It also added an extension to Xorg for relaying these commands to the OpenGL driver (libGL). This is referred to as indirect rendering, and it has a potential issue: with highly intensive graphics applications, the communication going through Xorg might end up becoming a bottleneck.

The solution was to circumvent Xorg, and let the X clients (the applications) communicate directly with the graphics driver (libGL). This approach is called Direct Rendering Infrastructure, and is described below.

Links:
- https://en.wikipedia.org/wiki/X_Window_System
- https://en.wikipedia.org/wiki/Xlib
- https://en.wikipedia.org/wiki/XCB
- https://en.wikipedia.org/wiki/GLX
- https://blogs.igalia.com/itoral/2014/07/29/a-brief-introduction-to-the-linux-graphics-stack/

## Wayland Display Server Protocol
TODO

Links:
- https://en.wikipedia.org/wiki/Wayland_(display_server_protocol)

## Direct Rendering Infrastructure
The Direct Rendering Infrastructure (DRI) is a way for X clients (applications) to circumvent the Xorg server, and directly communicate with graphics HW.

The DRI client (an X client doing direct rendering) needs a HW specific driver that allows it to communicate with the available GPU. This driver is usually provided as a shared library (e.g. *libGL.so*), which the client application dynamically links to. This driver is provided by the GPU vendor, or by third parties such as Mesa.

Xorg provides an X11 protocol extension (the DRI extension) through which the DRI clients coordinate with both the windowing system and the (DDX) driver.

To actually access the GPU HW, the driver must go through the kernel component called Direct Rendering Manager (as described below).

Links:
- https://en.wikipedia.org/wiki/Direct_Rendering_Infrastructure

## Direct Rendering Manager
The Direct Rendering Manager (DRM) is a subsystem in the kernel that's responsible for interfacing with GPUs. The DRM exposes an API which user-space programs (the GPU driver) can use to send commands and data to the GPU, and also configure the display settings.

Links:
- https://en.wikipedia.org/wiki/Direct_Rendering_Manager
