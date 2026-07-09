# Robot Learning Deep Dive #2: I Built A Mini Inspection Station In ROS 2

I just completed the next project in my Robot Learning Deep Dive series: a small ROS 2 inspection station.

The project is simple on purpose. It has four nodes:

```text
Camera
PLC
Conveyor
Logger
```

But the point was not to make something visually impressive. The point was to make the architecture visible.

In robotics, the hard part is often not writing one clever function. It is understanding what information exists, where it should flow, who should decide, who should act, and what should be logged. This project helped me practice exactly that.

## The System I Built

The inspection station behaves like a tiny industrial cell.

A camera inspects parts. A PLC receives the camera result and decides whether to accept or reject the part. A conveyor receives the PLC command and acts on it. A logger watches the system and records what happened.

The ROS 2 graph looks like this:

```text
camera_node
  publishes /inspection/camera/result
        |
        v
plc_node
  subscribes /inspection/camera/result
  publishes  /inspection/plc/command
        |
        v
conveyor_node
  subscribes /inspection/plc/command

logger_node
  subscribes to the inspection topics
```

That little chain is the first time the project started feeling like a real robotics system instead of isolated tutorial commands.

## What I Practiced

This project covered four ROS 2 fundamentals:

```text
Publishers
Subscribers
Services
Parameters
```

The camera node was my first sensor-style publisher. It produced fake inspection messages like:

```text
part_id=703, result=PASS
```

Then the PLC node subscribed to those messages, interpreted them, and published a new command:

```text
part_id=703, result=PASS, COMMAND=ACCEPT
```

That was the key moment. The PLC was not just receiving data. It was transforming information and publishing a decision.

## The Mental Model That Clicked

The important idea is that ROS 2 nodes do not need to know each other directly.

The camera does not call the PLC.

The PLC does not call the conveyor.

They meet through topics.

```text
Camera publishes facts.
PLC subscribes to facts and publishes decisions.
Conveyor subscribes to decisions and acts.
Logger observes everything.
```

This is the beginning of robotics software architecture.

## What Debugging Taught Me

I also ran into a very practical Windows lesson.

At one point, `colcon build` failed because Windows could not overwrite:

```text
camera_node.exe
```

The reason was simple: the node was still running in another terminal. Windows had locked the executable.

So the debugging lesson was:

```text
Stop running ROS 2 nodes before rebuilding the package.
```

This is the kind of small operational detail that makes learning robotics feel real. The problem is not always the code. Sometimes the system is still alive somewhere.

## Why This Matters

This project is small, but the pattern scales.

A real robotic workcell may have cameras, PLCs, conveyors, robot arms, alarms, databases, dashboards, and safety systems. The same questions keep coming back:

```text
Who publishes?
Who subscribes?
Who owns the decision?
Who exposes a service?
What should be a parameter?
What needs to be logged?
```

That is why I like this project. It is not just a ROS 2 exercise. It is a tiny version of systems thinking.

## What I Understand Now

I now understand ROS 2 publishers and subscribers less as syntax and more as a design language.

The syntax matters:

```python
self.create_publisher(...)
self.create_subscription(...)
```

But the deeper idea is the architecture:

```text
Separate the sensor, controller, actuator, and observer.
Let them communicate through typed channels.
Keep each node responsible for one job.
```

That is the robot generalist muscle I am trying to keep alive.

Next, I want to add services and parameters more deliberately: resetting PLC counts, enabling or disabling the conveyor, tuning defect rates, and making the system configurable without rewriting code.

Small station. Real pattern.
