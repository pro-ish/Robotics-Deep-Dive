# Inspection Station

This is a ROS 2 learning project for building an industrial-style inspection station.

You will practice:

- Publishers
- Subscribers
- Services
- Parameters
- Launch files
- Multi-node system thinking

## System Story

A part moves down a conveyor. A camera inspects it. A PLC decides whether to accept or reject it. A conveyor node receives the PLC command. A logger records everything.

```text
camera_node
  publishes /inspection/camera/result
        |
        v
plc_node
  subscribes /inspection/camera/result
  publishes /inspection/plc/command
  serves    /inspection/plc/reset_counts
        |
        v
conveyor_node
  subscribes /inspection/plc/command
  publishes /inspection/conveyor/state
  serves    /inspection/conveyor/enable

logger_node
  subscribes to all inspection topics
  writes inspection_log.csv
```

## Nodes

- `camera_node`: fake camera inspection publisher
- `plc_node`: decision logic subscriber/publisher with reset service
- `conveyor_node`: conveyor command subscriber with enable service
- `logger_node`: observer that writes inspection events to CSV

## Build

```cmd
cd /d C:\Users\DELL\ros2_ws
pixi run -m C:\pixi_ws colcon build --packages-select inspection_station
```

## Run

```cmd
cd /d C:\pixi_ws
pixi shell
cd /d C:\Users\DELL\ros2_ws
call C:\pixi_ws\ros2-windows\setup.bat
call install\setup.bat
ros2 launch inspection_station inspection_station.launch.py
```

## Inspect

```cmd
ros2 topic list
ros2 topic echo /inspection/camera/result
ros2 topic echo /inspection/plc/command
ros2 service call /inspection/plc/reset_counts std_srvs/srv/Trigger "{}"
ros2 service call /inspection/conveyor/enable std_srvs/srv/SetBool "{data: false}"
```
