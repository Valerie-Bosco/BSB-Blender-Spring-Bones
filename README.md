# BSB - Blender Spring Bones

ℹ️NOTE: <br>
**THERE IS ONLY ONE RELEASE <br>
IT'S DATE DOES NOT REFLECT THE VERSION AND FILES ARE BEING UPDATED OVER IT TO KEEP LINK INTEGRITY OUTSIDE OF GITHUB**


### Patched and improved to support 3.6 - 4.5 <br>
**[ The Original version has been fully discontinued by it's developer ]** <br>
**[Only Blender Releases are supported, alpha/beta versions of Blender are not and will not be supported]**

<br>

Check out [Issues](https://github.com/Valerie-Bosco/BSB-Blender-Spring-Bones/issues) and [Discussions](https://github.com/Valerie-Bosco/BSB-Blender-Spring-Bones/discussions) for bug reports or feedback/feature requests <br>
Discord Server: https://discord.gg/44fSbYrzZd

<br>

### Installation:
- Download the [BSB-Blender-Spring-Bones.zip ](https://github.com/Valerie-Bosco/BSB-Blender-Spring-Bones/releases/download/main_branch_latest/BSB-Blender-Spring-Bones.zip) available from the [releases](https://github.com/Valerie-Bosco/BSB-Blender-Spring-Bones/releases/tag/main_branch_latest) page, 
- In blender [4.1-]: preferences -> addons -> install addon -> select the [BSB-Blender-Spring-Bones.zip] -> click install 
- In blender [4.2+]: preferences -> addons -> top right dropdown -> install from disk -> select the [BSB-Blender-Spring-Bones.zip] -> click install from disk

<br>

### Features:
Spring-like bone physics simulation for dynamic bounce effects

![alt text](https://github.com/artellblender/springbones/blob/master/bbones_chain.gif)

- spring simulation [rotation mode] [child bones only]
  - bone spring physics are rotational only grounding the bone to it's head position, can still be moved by anything but it won't be moved by the simulation

- spring simulation [movement mode] [child bones only]
  - bone spring physics are simulated both positionally and rotationally, the bone will move and rotate acting with a spring-like movement and spring like rotation **requires the bone to not be connected if parented, or movement will not be applied (can still be parented)**

- interactive mode [frame/playback independant] [does not allow baking]
  - allows for real time interaction without the need to start the timeline playback, identical to frame mode but does not support baking, mainly for testing parameters and rig setups
 
- animation mode [frame/playback dependant] [allows baking]
  - allows for real time interaction tied to the timeline playback, allows for baking and simulation during animation playback, intended for animations/baking/rendering and final workflows requiring it
  - baking steps: F3 (search bar) -> Bake Action (nla.bake)

- simulation parameters
  - gravity, stiffness, dampening strength, influence percentage (% effect of sim, 50% means: 50% pose-controlled 50% sim-controlled for manual+sim hybrid animations)

- bone collision/mesh collision/intra-bones collision
    - bones can be enabled to collide, collide with other bones marked as colliders and to collide with meshes
