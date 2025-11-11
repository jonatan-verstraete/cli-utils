# Resume Experience Tree Visualization

A minimal, elegant timeline visualization for displaying programming experience on a resume. Features a left-aligned timeline with dates displayed directly on the SVG line, flowing content without card boxes, and easy-to-customize separate configuration.

## Features

- **A4 Page Size**: Optimized for single-page resume printing (210mm × 297mm)
- **Left-Aligned Timeline**: Positioned at 120px with minimal space for left events
- **Dates on Timeline**: Years displayed directly on SVG connection lines
- **Flowing Content**: No card boxes - content flows naturally with the page
- **Separate Config File**: Easy-to-edit `timeline-data.js` for managing events
- **No Overlapping**: Proper spacing prevents content collision
- **Hue-Based Coloring**: Each event gets unique color based on position
- **No-Wrap Small Events**: Left side events don't wrap, use ellipsis for overflow
- **Responsive**: Adapts to different screen sizes
- **Print-Ready**: Optimized CSS for printing

## Design Philosophy

The visualization uses a clean, flowing design:

- **No cards**: Content flows with the page instead of being boxed
- **Dates on line**: Years positioned directly on connection lines
- **Natural flow**: Title at line height, content below
- **Left-aligned**: Timeline positioned to accommodate sidebars
- **Minimal**: Clean typography without unnecessary decoration
- **Easy to customize**: Separate config file with clear examples

## Structure

```
resume-tree-viz/
├── index.html          # Page container with SVG canvas
├── styles.css          # Minimal flowing styles
├── timeline-data.js    # ⭐ Event data and configuration
├── script.js           # Rendering logic
└── README.md           # This file
```

## Quick Start

1. Open `timeline-data.js`
2. Add your events to the `timelineData` array
3. Adjust `timelineConfig` if needed
4. Open `index.html` in a browser

## Configuration

All configuration is in `timeline-data.js`:

### Adding Events

```javascript
const timelineData = [
    {
        // Unique identifier
        id: 'my-event',
        
        // Event title
        title: 'My Position',
        
        // Year or date range
        year: '2020 - 2023',
        
        // Side: 'left' for small events, 'right' for main content
        side: 'right',
        
        // For 'right' side events - full description
        description: 'Detailed description of the role...',
        
        // For 'right' side events - technology stack
        stack: ['Tech1', 'Tech2', 'Tech3']
    },
    {
        // Small event on left side
        id: 'side-project',
        title: 'Side Project Name',
        year: '2021 - Present',
        side: 'left'
        // No description or stack for left side
    }
];
```

### Timeline Configuration

```javascript
const timelineConfig = {
    timelineX: 120,        // Timeline position from left (pixels)
    startY: 50,            // Starting Y position (pixels)
    eventSpacing: 100,     // Vertical spacing between events (pixels)
    leftOffset: 100,       // Distance from timeline to left events (pixels)
    rightOffset: 60,       // Distance from timeline to right events (pixels)
    dotRadius: 5,          // Dot outer radius (pixels)
    dotBorderWidth: 2,     // White border width (pixels)
    lineWidth: 1.5,        // Connection line width (pixels)
    timelineWidth: 2,      // Main timeline width (pixels)
    colorMode: 'hue',      // 'hue' for spectrum, 'mono' for single color
    baseColor: '#7fa8c4'   // Used in mono mode
};
```

## Layout Design

```
Small Events (LEFT)         Timeline          Main Content (RIGHT)
  (no-wrap)              (with dates)         (flowing, no cards)

JS Canvas Library  ─── 2017-Present ●
                                              ● 2016-2019 ─── Bachelor - IT
                                                              Description text...
Bash Utils Lib     ─── 2020-Present ●                        Tech tags...

                                              ● 2019-Present ─── Full-time Frontend Dev
Timesheet auto     ─── 2021 ●                                Description text...
                                                              Tech tags...
```

## Content Types

### Right Side - Main Content
- Full position titles (education, work experience)
- Year displayed on SVG line
- Title (h3) at line height
- Description paragraph below
- Technology stack tags at bottom
- No card box - flows with page

### Left Side - Small Events
- Side projects, certificates, libraries
- Year displayed on SVG line
- Single line title (no-wrap, ellipsis)
- No description or tags
- Minimal, unobtrusive

## Color Modes

### Hue Mode (Default)
Each event gets a unique color based on position:
- Formula: `hsl((360/total) * index, 45%, 60%)`
- Creates vibrant spectrum across timeline
- Visually distinct events

### Mono Mode
All events use the same color:
- Consistent traditional look
- Uses `timelineConfig.baseColor`

Switch modes by editing `colorMode` in `timeline-data.js`.

## Design Details

### Dates on Timeline
- SVG text elements positioned on connection lines
- Small, subtle gray text (10px, #95a5a6)
- Positioned above the line
- Text-anchor depends on side (start for right, end for left)

### Flowing Content
- No card boxes or shadows
- Content positioned relative to line
- Title (h3) at line height for visual intersection
- Description flows naturally below
- Tech tags at bottom with minimal styling

### Left Events
- `white-space: nowrap` prevents wrapping
- `text-overflow: ellipsis` for long titles
- Maximum width 100px
- Right-aligned text

### No Overlapping
- 100px vertical spacing between events
- Content positioned to avoid collision
- Clean, organized layout

## Sample Data

The included sample shows:

**Right Side:**
1. Bachelor - IT (2016-2019) - Full details with stack
2. Full-time Frontend Dev (2019-Present) - Full details with stack

**Left Side:**
3. JS Canvas Projects Library (2017-Present)
4. Bash Utils Library (2020-Present)
5. Timesheet automation (2021)

## Styling

### Typography
- Titles: 16px, medium weight, dark gray
- Description: 13px, lighter weight, readable
- Tech tags: 10px with gradient background
- Left events: 11px, blue color, no-wrap

### Colors
- Timeline: #d5dfe6 (light gray)
- Dots: White border with colored center
- Lines: Event color at 30% opacity
- Text: Various grays for hierarchy

### No Cards
- Content flows directly on page
- No backgrounds or borders
- Minimal shadows removed
- Clean, professional appearance

## Customization Tips

### Adding More Events
1. Open `timeline-data.js`
2. Add new object to `timelineData` array
3. Follow the structure shown in comments
4. Reload page to see changes

### Adjusting Spacing
- Increase `eventSpacing` for more vertical space
- Adjust `leftOffset` to move left events
- Adjust `rightOffset` to move main content
- Change `timelineX` to shift entire timeline

### Changing Colors
- Set `colorMode: 'mono'` for single color
- Adjust `baseColor` for different hue
- Or keep `colorMode: 'hue'` for spectrum

### Positioning
- Timeline positioned at 120px from left
- Leaves room for sidebar (0-120px)
- Small events use 100px space (20-120px)
- Main content starts at 180px (120 + 60)

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge
- Firefox
- Safari
- Opera

Uses standard SVG and CSS - no special features required.

## Print Optimization

- A4 size (210mm × 297mm)
- Clean layout prints well
- No backgrounds to waste ink
- Dates on line save vertical space

## Design Notes

This design emphasizes:
- **Clarity**: Dates on timeline, content flows clearly
- **Simplicity**: No card boxes, minimal decoration
- **Organization**: Separate config file, clear structure
- **Efficiency**: Easy to add/edit events
- **Professional**: Clean, modern appearance

Perfect for a contemporary resume that's easy to read and maintain.
