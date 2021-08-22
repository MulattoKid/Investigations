# Vulkan Windowing System
The Vulkan WSI (Window System Integration) allows the Vulkan core API to interface with an OS' windowing system to display the results of computations. The result of computations performed through Vulkan aren't necessarily going to be shown graphically, so the WSI is not part of the core API. Instead it's support comes through an extension that the Vulkan driver for an OS must support.

The basis of the WSI is the *VK_KHR_surface* extension which has been a part of Vulkan since its initial version, 1.0. It defines an object, *VKSurfaceKHR*, which is "connected" to an actual window created on the platform through the appropriate *vkCreate<Platform>SurfaceKHR* function call.

The surface can then be queried about its properties, e.g. color format. Using this info a *VkSwapchainKHR* object can be created, which is what will be used to aqcuire new images to render/put computational results into and shown. Note that this requires another extension to be supported by the Vulkan driver: *VK_KHR_swapchain*.

Links:
- https://github.com/KhronosGroup/Vulkan-Guide/blob/master/chapters/wsi.md
- https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#wsi
- https://www.khronos.org/registry/vulkan/specs/1.2-extensions/man/html/VK_KHR_surface.html
- https://www.khronos.org/registry/vulkan/specs/1.2-extensions/html/vkspec.html#boilerplate-wsi-header-table
