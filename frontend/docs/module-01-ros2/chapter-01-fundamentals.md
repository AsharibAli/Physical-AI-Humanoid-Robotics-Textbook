---
title: Chapter 1 - ROS 2 Fundamentals
description: Introduction to ROS 2 architecture, core concepts, and your first node
---

# Chapter 1: ROS 2 Fundamentals

## Concepts

### What is ROS 2?

**ROS 2** (Robot Operating System 2) is an open-source framework for building robot applications. Unlike ROS 1, ROS 2 is built on **DDS** (Data Distribution Service), making it more reliable and suitable for production environments.

**Key Improvements over ROS 1:**
- **Real-time capable**: Better timing guarantees
- **Multi-robot support**: Native distributed systems
- **Security**: Built-in encryption and authentication
- **Cross-platform**: Works on Linux, Windows, and macOS

### Core Concepts

**1. Nodes**
- Independent processes that perform computation
- Communicate via topics, services, or actions
- Example: camera_node, motion_planner_node

**2. Topics**
- Named buses for asynchronous message passing
- Publishers send messages, subscribers receive them
- Many-to-many communication pattern

**3. Messages**
- Data structures sent over topics
- Defined in `.msg` files
- Built-in types: std_msgs, sensor_msgs, geometry_msgs

**4. Services**
- Synchronous request-response communication
- Used for one-time operations
- Example: reset_simulation, get_robot_state

## Architectures

### ROS 2 System Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Camera    │────→│   Vision    │────→│  Planning   │
│    Node     │     │    Node     │     │    Node     │
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │                    │
       └────────────────────┴────────────────────┘
                          DDS Layer
```

**DDS Middleware:**
- Handles discovery (nodes find each other automatically)
- Manages QoS (Quality of Service) settings
- Provides reliability and fault tolerance

### Node Communication Patterns

**1. Publisher-Subscriber (Topics)**
```python
# Publisher
publisher = node.create_publisher(String, 'chatter', 10)
publisher.publish(msg)

# Subscriber
subscription = node.create_subscription(String, 'chatter', callback, 10)
```

**2. Service Client-Server**
```python
# Server
service = node.create_service(AddTwoInts, 'add_two_ints', handle_request)

# Client
client = node.create_client(AddTwoInts, 'add_two_ints')
response = client.call(request)
```

## Algorithms

### Message Passing Algorithm

**1. Discovery Phase:**
- Nodes announce their topics/services
- DDS maintains a global directory
- Matching publishers and subscribers connect

**2. Communication Phase:**
- Publisher serializes message
- DDS transmits over network
- Subscriber deserializes and processes

### QoS (Quality of Service) Matching

**QoS Policies:**
- **Reliability**: BEST_EFFORT vs RELIABLE
- **Durability**: VOLATILE vs TRANSIENT_LOCAL
- **History**: KEEP_LAST(n) vs KEEP_ALL

**Example:**
```python
qos_profile = QoSProfile(
    reliability=QoSReliabilityPolicy.RELIABLE,
    durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
    history=QoSHistoryPolicy.KEEP_LAST,
    depth=10
)
```

## Real-World Considerations

### Production Deployment

**1. Launch Files:**
- Use Python launch files (not XML)
- Group related nodes
- Set parameters and remapping

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_package',
            executable='my_node',
            name='my_node',
            parameters=[{'param1': 'value1'}]
        )
    ])
```

**2. Logging Best Practices:**
- Use ROS 2 logging (not print)
- Set appropriate log levels (DEBUG, INFO, WARN, ERROR)
- Filter logs for production

```python
self.get_logger().info('Node started')
self.get_logger().warn('Low battery')
```

### Performance Tuning

**1. Reduce Latency:**
- Use BEST_EFFORT reliability for high-frequency data
- Optimize message sizes
- Run nodes on same machine when possible

**2. Increase Throughput:**
- Use larger QoS queue depths
- Batch messages when appropriate
- Profile with ros2 topic hz/bw

### Debugging Strategies

**Essential Commands:**
```bash
# List active nodes
ros2 node list

# Inspect node info
ros2 node info /my_node

# Echo topic data
ros2 topic echo /my_topic

# View message structure
ros2 interface show std_msgs/msg/String

# Record data
ros2 bag record -a
```

**Common Issues:**
- **Nodes don't discover each other**: Check RMW_IMPLEMENTATION and network
- **Message drops**: Increase QoS depth or use RELIABLE
- **High latency**: Reduce message rate or optimize network

### Next Steps

- **Chapter 2**: Dive deeper into topics and message types
- **Chapter 3**: Learn URDF for robot description
- **Practice**: Build a simple publisher-subscriber pair
