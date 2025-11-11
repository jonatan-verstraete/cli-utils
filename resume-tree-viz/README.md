# Resume Experience Tree Visualization

A minimal, elegant timeline visualization for displaying programming experience on a resume. Features a clean single-line timeline with events branching left (small notes) and right (main content).

## Features

- **A4 Page Size**: Optimized for single-page resume printing (210mm × 297mm)
- **Single Center Timeline**: One clean vertical line as the main thread
- **Left/Right Separation**: Small events on left, main content on right
- **Simple Horizontal Lines**: No curves - just clean connections
- **Minimal Styling**: Text notes for small events, detailed cards for milestones
- **Subtle Color Palette**: Single-color pattern using subtle blue tints
- **Responsive**: Adapts to different screen sizes while maintaining elegance
- **Print-Ready**: Optimized CSS for printing

## Design Philosophy

The visualization occupies approximately 60% of the page content, serving as a clean timeline backdrop. The design is:

- **Simple**: Single timeline with straight horizontal connections
- **Clean**: Clear left/right separation for different content types
- **Subtle**: Minimal styling that doesn't demand attention
- **Professional**: Typography and spacing optimized for readability
- **Intuitive**: Small events left, major milestones right

## Structure

- `index.html` - Main HTML structure
- `styles.css` - Minimal styling with two content types
- `script.js` - JavaScript for rendering timeline and events

## Layout Concept

```
Small Events (LEFT)         Timeline (CENTER)      Main Content (RIGHT)

JS Canvas Library    ────●                           ●──── Bachelor - IT
                                                            (full details)
Bash Utils Library   ────●

                                                     ●──── Full-time Frontend Dev
                                                            (full details)
Timesheet automation ────●
```

## Content Types

The visualization supports two placement options via the `side` property:

### Right Side - Main Content
Major milestones like education and full-time work. Includes:
- Title and year
- Description paragraph
- Technology stack tags
- Full card styling

### Left Side - Small Events
Side projects, certificates, libraries, interests. Includes:
- Title and year only
- Simple text styling
- Minimal, unobtrusive display

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

Simply open `index.html` in a web browser. The visualization will render automatically with clean left/right separation.

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
    timelinePos: 0
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
- `centerLineX`: X position of the central timeline (default: 300)
- `startY`: Starting Y position (default: 50)
- `rowGap`: Vertical spacing between events (default: 100)
- `leftOffset`: Distance from timeline to left content (default: 250)
- `rightOffset`: Distance from timeline to right content (default: 40)

## Color Scheme

The visualization uses a subtle blue color palette:
- Timeline: `#b8d0e0`
- Dots: `#7fa8c4`
- Main titles: `#4a7c9e`
- Text: `#5a6b7a` / `#6b92ab`

All colors are chosen to be subtle and professional, supporting readability while adding visual elegance.

## Design Notes

This design deliberately simplifies complex branching structures:
- No curved lines (too complex to maintain)
- No concurrent timelines (not needed for clarity)
- Simple horizontal connections for easy reading
- Clear left/right separation for content hierarchy

The result is a clean, professional timeline that clearly shows your career progression with appropriate emphasis on major milestones while keeping smaller events visible but unobtrusive.
