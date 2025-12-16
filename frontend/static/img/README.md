# Static Images Directory

This directory contains static assets for the Physical AI & Humanoid Robotics textbook:

- **Diagrams**: Architecture diagrams, workflow charts, system illustrations
- **Photos**: Robot hardware photos, sensor images, component pictures
- **Icons**: UI icons, navigation elements, branding assets
- **Screenshots**: Software interface captures, simulation screenshots

## Organization

- Place module-specific images in subdirectories (e.g., `ros2/`, `isaac/`, `vla/`)
- Use descriptive filenames: `bipedal-walking-diagram.png`, `lidar-sensor-photo.jpg`
- Optimize images for web (compress, appropriate dimensions)
- Prefer SVG for diagrams when possible

## Usage in Markdown

```markdown
![Alt text](</img/your-image.png>)
```

## Supported Formats

- PNG (diagrams, screenshots)
- JPEG (photos)
- SVG (vector graphics, preferred for diagrams)
- GIF (animations, use sparingly)
