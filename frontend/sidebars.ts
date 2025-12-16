import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

/**
 * Sidebar structure for Physical AI & Humanoid Robotics textbook
 * 12 modules organized by learning progression
 */
const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Introduction',
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'module-01-ros2/index',
        'module-01-ros2/chapter-01-fundamentals',
        'module-01-ros2/chapter-02-nodes-topics',
        'module-01-ros2/chapter-03-urdf',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'module-02-simulation/index',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
      items: [
        'module-03-isaac/index',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'module-04-vla/index',
      ],
    },
    {
      type: 'category',
      label: 'Module 5: Sensor Systems',
      items: [
        'module-05-sensors/index',
      ],
    },
    {
      type: 'category',
      label: 'Module 6: Locomotion',
      items: [
        'module-06-locomotion/index',
      ],
    },
    {
      type: 'category',
      label: 'Module 7: Manipulation',
      items: [
        'module-07-manipulation/index',
      ],
    },
    {
      type: 'category',
      label: 'Module 8: Perception',
      items: [
        'module-08-perception/index',
      ],
    },
    {
      type: 'category',
      label: 'Module 9: Control Systems',
      items: [
        'module-09-control-systems/index',
      ],
    },
    {
      type: 'category',
      label: 'Module 10: Human-Robot Interaction',
      items: [
        'module-10-hri/index',
      ],
    },
    {
      type: 'category',
      label: 'Module 11: Deployment',
      items: [
        'module-11-deployment/index',
      ],
    },
    {
      type: 'category',
      label: 'Module 12: Advanced Topics',
      items: [
        'module-12-advanced-topics/index',
      ],
    },
  ],
};

export default sidebars;
