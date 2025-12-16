---
title: Chapter 2 - Nodes and Topics
description: Deep dive into ROS 2 nodes, topics, and message passing
---

# Chapter 2: Nodes and Topics in Depth

## Concepts

### ROS 2 Nodes

**Nodes** are the building blocks of ROS 2 applications. Each node should have a single, well-defined purpose.

**Node Characteristics:**
- **Independent processes**: Can run on different machines
- **Isolated**: Node crash doesn't affect others
- **Composable**: Can be combined in different ways
- **Language-agnostic**: Python, C++, or other client libraries

### Topics and Message Passing

**Topics** enable asynchronous, many-to-many communication between nodes.

**Key Features:**
- **Decoupled**: Publishers don't know subscribers
- **Scalable**: Add nodes without changing existing code
- **Typed**: Each topic has a specific message type

## Architectures

### Node Design Patterns

**1. Single Responsibility**
```
❌ Bad: mega_node (does everything)
✅ Good: camera_node, detector_node, planner_node
```

**2. Layered Architecture**
```
Sensors → Perception → Planning → Control → Actuators
```

**3. Hierarchical Organization**
```
/robot/
  ├─ /sensors/camera
  ├─ /sensors/lidar
  ├─ /control/arm
  └─ /control/base
```

## Algorithms

### Creating a Node (Python)

```python
import rclpy
from rclpy.node import Node

class MinimalNode(Node):
    def __init__(self):
        super().__init__('minimal_node')
        self.get_logger().info('Node initialized')

def main():
    rclpy.init()
    node = MinimalNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

### Publisher-Subscriber Pattern

**Publisher:**
```python
class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher')
        self.publisher = self.create_publisher(String, 'topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World'
        self.publisher.publish(msg)
```

**Subscriber:**
```python
class SubscriberNode(Node):
    def __init__(self):
        super().__init__('subscriber')
        self.subscription = self.create_subscription(
            String, 'topic', self.listener_callback, 10)

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: {msg.data}')
```

## Real-World Considerations

### Topic Naming Conventions

**Best Practices:**
- Use lowercase with underscores: `robot_state`
- Namespace by function: `/sensors/camera/image`
- Avoid generic names like `data` or `output`
- Be consistent across your project

### Message Design Tips

**Keep messages:**
- **Small**: Reduce network overhead
- **Self-contained**: Include timestamp and frame_id
- **Versioned**: Plan for future changes

**Example:**
```python
std_msgs/Header header  # Always include
geometry_msgs/Pose pose
float64 confidence
```

### Monitoring and Debugging

```bash
# Monitor topic frequency
ros2 topic hz /camera/image

# Monitor bandwidth
ros2 topic bw /camera/image

# View message in terminal
ros2 topic echo /camera/image --once

# Graph nodes and topics
ros2 run rqt_graph rqt_graph
```

### Common Pitfalls

1. **Too many topics**: Leads to complexity
2. **Too few topics**: Tight coupling
3. **Wrong QoS**: Messages dropped or latency issues
4. **Forgetting namespaces**: Topic name collisions

---

**Next Chapter**: Learn URDF for robot description and visualization
