# Ayg Robot Description (URDF)

For the USD description, see the [`usd`](https://github.com/Cyber-Fusion/ayg_description/tree/usd) branch.

## Overview

This package contains Ayg's robot description (URDF) developed by [Cyber-Fusion](https://github.com/Cyber-Fusion).
It carries both Ayg model generations, 1.2 and 1.3, side by side, selected with the `version` xacro arg.

## License

This software is released under a [BSD-3-Clause license](LICENSE).

## Layout

```
urdf/
  ayg.xacro                       # thin dispatcher + everything genuinely shared
  ayg1.2.xacro   ayg1.3.xacro     # per-version roots (Base, IMU; battery macro on 1.2 only)
  sim_ros2_control.xacro          # shared ros2_control/Gazebo block
  1.2/{legs,camera,initial_configuration}.xacro
  1.3/{legs,lidar,initial_configuration}.xacro
  ayg1.2.urdf   ayg1.3.urdf       # generated + committed flat URDFs
meshes/1.2/...  meshes/1.3/...
mujoco/1.2/ayg.xml   mujoco/1.3/ayg.xml
config/1.2/config.rviz   config/1.3/config.rviz
```

Ayg 1.2 and 1.3 share filenames for a few meshes (`Base`, `L_Thigh`, `R_Thigh`) whose content
differs between versions, so each version keeps its own mesh directory rather than a shared one.

## Usage

The `.xacro` file accepts the following arguments:
- `version`: {`1.2`, `1.3`} (default: `1.2`, mirroring `ayg_utils.robot_version.DEFAULT` in the Ayg repo). Selects the whole per-version subtree (root xacro, legs, meshes, mujoco/rviz configs).
- `camera`: `Bool` (default: `True`). If `True`, an Ayg 1.2 robot also has the RealSense D555 depth camera link. Harmless no-op on `version:=1.3`.
- `lidar`: `Bool` (default: `True`). If `True`, an Ayg 1.3 robot also has the `lidar_link` sensor frame (Ayg 1.3 replaced the D555 depth camera with a HESAI JT128). The head/mount itself is always present. Harmless no-op on `version:=1.2`.
- `sim`: `Bool` (default: `False`). If `True`, the URDF is augmented with Gazebo (not Gazebo Classic) tags for the robot's sensors and actuators.
- `initial_configuration`: {`lying_down`, `standing`} (default: `lying_down`). Sets the initial configuration of the robot in Gazebo (requires `sim` to be `True`). The joint values differ between 1.2 and 1.3 (different leg geometry).
- `controller`: {`default`, `ddb`} (default: `default`). Sets the controller to be used in Gazebo (requires `sim` to be `True`). These controllers are from the [main repo](https://github.com/Cyber-Fusion/Ayg).

The pure `.urdf` files are committed (`urdf/ayg1.2.urdf`, `urdf/ayg1.3.urdf`) and can be regenerated with:
```shell
ros2 run xacro xacro urdf/ayg.xacro version:=1.2 sim:=False > urdf/ayg1.2.urdf
ros2 run xacro xacro urdf/ayg.xacro version:=1.3 sim:=False > urdf/ayg1.3.urdf
```
These can be useful with certain libraries or tools (e.g. [Pinocchio](https://github.com/stack-of-tasks/pinocchio)).

### Launch Files

To visualize the robot model in RViz, run
```shell
ros2 launch ayg_description rviz.launch.py version:=1.2
```

This launch file starts the robot state publisher, the joint state publisher GUI, and RViz.
