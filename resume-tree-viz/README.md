# Resume Experience Tree Visualization

A minimal, elegant timeline visualization for displaying programming experience on a resume. Features a refined modern design with left-aligned timeline, hue-based coloring, and smooth 2030-style aesthetics.

## Features

- **A4 Page Size**: Optimized for single-page resume printing (210mm × 297mm)
- **Left-Aligned Timeline**: Positioned to accommodate sidebars with minimal space for left events
- **Left/Right Separation**: Small events on left, main content on right
- **Refined Dots**: 5px dots with 2px white border and colored centers
- **Hue-Based Coloring**: Each event gets unique color based on timeline position
- **Modern Shadows**: Layered box-shadows instead of borders for depth
- **Thin Refined Lines**: 1.5px connection lines with smooth gradients
- **Smooth Animations**: Cubic-bezier transitions for professional feel
- **Responsive**: Adapts to different screen sizes while maintaining elegance
- **Print-Ready**: Optimized CSS for printing

## Design Philosophy

The visualization uses modern 2030-style design principles:

- **Refined**: Thin lines, elegant dots with white borders, subtle shadows
- **Smooth**: Cubic-bezier easing for natural interactions
- **Colorful**: Hue-based spectrum coloring for visual interest
- **Spaced**: Proper card spacing prevents visual clutter
- **Professional**: Typography and spacing optimized for readability
- **Modern**: Gradient backgrounds, layered shadows, drop-shadows on SVG

## Structure

- `index.html` - Main HTML structure
- `styles.css` - Modern refined styling with layered shadows
- `script.js` - Timeline rendering with hue-based coloring

## Layout Concept

```
Small Events (LEFT)    Timeline (LEFT-ALIGNED)    Main Content (RIGHT)

JS Canvas Library  ───●
                                                   ●─── Bachelor - IT
                                                        (full details, shadow)
Bash Utils Library ───●
                                                   
                                                   ●─── Full-time Frontend Dev
                                                        (full details, shadow)
Timesheet auto     ───●
```

## Color Modes

The visualization supports two color modes via the `colorMode` config:

### Hue Mode (Default)
Each event gets a unique hue based on its position in the timeline:
- Formula: `hue = (360 / total) * index`
- Creates a vibrant spectrum across the timeline
- Events are visually distinct

### Mono Mode
All events use the same base color:
- Consistent blue theme
- More subtle and traditional

To switch modes, edit `treeConfig.colorMode` in `script.js`:
```javascript
colorMode: 'hue'  // or 'mono'
```

## Content Types

The visualization supports two placement options via the `side` property:

### Right Side - Main Content
Major milestones like education and full-time work. Features:
- Title and year
- Description paragraph
- Technology stack tags with gradient backgrounds
- Layered box-shadows for depth
- 130px spacing between cards
- Hover effects with smooth transitions

### Left Side - Small Events
Side projects, certificates, libraries, interests. Features:
- Simple p tag for title (blue colored)
- p tag for year (gray)
- Minimal styling
- Right-aligned text

## Sample Data

The visualization includes five example experiences:

**Right Side (Main):**
1. **Bachelor - IT** (2016-2019)
   - Full card with description
   - Stack: Java, Python, SQL, Git, Linux, React, Node.js

2. **Full-time Frontend Dev** (2019-Present)
   - Full card with description
   - Stack: TypeScript, React, Vue.js, CSS3, Webpack, Jest, GraphQL

**Left Side (Small Events):**
3. **JS Canvas Projects Library** (2017-Present)
   - Simple text note

4. **Bash Utils Library** (2020-Present)
   - Simple text note

5. **Timesheet automation** (2021)
   - Simple text note

## Usage

Simply open `index.html` in a web browser. The visualization will render automatically with refined modern styling.

## Customization

To add your own experiences, edit the `experiences` array in `script.js`:

### Main Content (Right Side)
```javascript
{
    id: 'my-experience',
    title: 'My Role',
    year: '2020 - 2023',
    description: 'Detailed description of the role and achievements.',
    stack: ['Tech1', 'Tech2', 'Tech3'],
    side: 'right',
    timelinePos: 0  // Used for vertical ordering
}
```

### Small Event (Left Side)
```javascript
{
    id: 'side-project',
    title: 'My Side Project',
    year: '2021 - Present',
    side: 'left',
    timelinePos: 1
}
```

## Timeline Configuration

The timeline can be configured in `treeConfig`:

```javascript
const treeConfig = {
    timelineX: 180,           // Left-aligned position
    startY: 50,               // Starting Y position
    rowGap: 130,              // Spacing between main cards
    leftOffset: 150,          // Distance to left content
    rightOffset: 40,          // Distance to right content
    dotRadius: 5,             // Dot outer radius
    dotBorderWidth: 2,        // White border width
    lineWidth: 1.5,           // Connection line width
    timelineWidth: 2,         // Main timeline width
    baseColor: '#7fa8c4',     // Fallback color (mono mode)
    colorMode: 'hue'          // 'hue' or 'mono'
};
```

## Modern Design Elements

### Refined Dots
- 5px radius with 2px white border
- Colored inner circle (3px radius)
- Subtle drop-shadow for depth
- Hue-based or mono coloring

### Layered Shadows
Main cards use two shadow layers:
- Primary: `0 2px 12px rgba(0, 0, 0, 0.06)`
- Secondary: `0 1px 3px rgba(0, 0, 0, 0.04)`

Hover state enhances depth:
- Primary: `0 4px 20px rgba(0, 0, 0, 0.08)`
- Secondary: `0 2px 6px rgba(0, 0, 0, 0.06)`

### Smooth Transitions
All interactions use cubic-bezier easing:
```css
transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
```

### Gradient Backgrounds
Tech stack tags feature subtle linear gradients:
```css
background: linear-gradient(135deg, 
    rgba(127, 168, 196, 0.08) 0%, 
    rgba(127, 168, 196, 0.12) 100%
);
```

## Color Scheme

### Hue Mode Colors
Each event gets a unique hue:
- Event 0: Red (0°)
- Event 1: Orange (72°)
- Event 2: Yellow-Green (144°)
- Event 3: Cyan (216°)
- Event 4: Purple (288°)

Saturation: 45%, Lightness: 60%

### Mono Mode Color
- Base: `#7fa8c4` (soft blue)

### Supporting Colors
- Timeline: `#d5dfe6`
- Text Primary: `#2c3e50`
- Text Secondary: `#5a6b7a`
- Text Muted: `#8996a3`

## Design Notes

This design deliberately emphasizes modern refinement:
- No borders on cards (shadows only)
- Thin refined lines throughout
- Proper spacing between elements
- Hue-based coloring for visual interest
- Smooth transitions for professional feel
- Layered shadows for depth perception

The result is a clean, modern timeline that clearly shows career progression with appropriate emphasis on major milestones while keeping smaller events visible but minimal. Perfect for a contemporary resume that stands out without being overwhelming.
