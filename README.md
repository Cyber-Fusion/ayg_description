# Ayg Robot Description (URDF)

## Overview

This package contains Ayg's robot description (URDF) developed by [Cyber-Fusion](https://github.com/Cyber-Fusion).
The Ayg 1.2 model is on the `ayg-1.2` branch.

## License

This software is released under a [BSD-3-Clause license](LICENSE).

## Layout

```
urdf/
  ayg.xacro                       # the root: arguments, Base, IMU, and the includes below
  legs.xacro                      # the four legs
  lidar.xacro                     # the front head and the LiDAR frame
  initial_configuration.xacro     # simulation start poses
  sim_ros2_control.xacro          # ros2_control/Gazebo/MuJoCo block (sim:=True)
  ayg.urdf                        # generated + committed flat URDF
meshes/
mujoco/ayg.xml
config/config.rviz
```

## Usage

The `.xacro` file accepts the following arguments:
- `lidar`: `Bool` (default: `True`). If `True`, the robot has the `lidar_link` sensor frame (the HESAI JT128). The head/mount itself is always present.
- `payload_mass`: kg carried on Base (default: `0.0`), for testing a policy under load in simulation.
- `sim`: `Bool` (default: `False`). If `True`, the URDF is augmented with Gazebo (not Gazebo Classic) tags for the robot's sensors and actuators.
- `initial_configuration`: {`lying_down`, `standing`} (default: `lying_down`). Sets the initial configuration of the robot in Gazebo (requires `sim` to be `True`).
- `sim_backend`: {`gazebo`, `mujoco`} (default: `gazebo`). The simulator the `sim` block targets: Gazebo's ros2_control plugin and sensors, or the MuJoCo system with `mujoco/ayg.xml` (requires `sim` to be `True`). Gazebo loads its controllers from the [main repo](https://github.com/Cyber-Fusion/Ayg)'s `ayg_control`.
- `use_csp`: `Bool` (default: `False`). Selects the debug hardware interface `RobstrideSystemDual` (MIT mode in walking, Robstride's CSP position mode in the other phases) instead of `RobstrideSystem` (requires `sim` to be `False`).
- `default_kp`, `default_kd`: the MIT gains the hardware interface applies until a controller claims the gain interfaces (defaults: `40.0`, `1.0`; requires `sim` to be `False`). `default_kp:=0` leaves the motors torque-free, for moving the joints by hand during calibration.

The pure `.urdf` file is committed (`urdf/ayg.urdf`) and can be regenerated with:
```shell
ros2 run xacro xacro urdf/ayg.xacro sim:=False > urdf/ayg.urdf
```
These can be useful with certain libraries or tools (e.g. [Pinocchio](https://github.com/stack-of-tasks/pinocchio)).

### Launch Files

To visualize the robot model in RViz, run
```shell
ros2 launch ayg_description rviz.launch.py
```

This launch file starts the robot state publisher, the joint state publisher GUI, and RViz.
