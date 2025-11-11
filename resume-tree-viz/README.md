# Resume Experience Tree Visualization

A minimal, elegant tree-view visualization for displaying programming experience on a resume. Designed with clean parallel timelines, harmonious layout, and subtle styling that provides visual interest without stealing attention from the content.

## Features

- **A4 Page Size**: Optimized for single-page resume printing (210mm × 297mm)
- **Clean Parallel Timelines**: Main and personal project timelines run side-by-side
- **No Overlapping**: Dynamic layout with content-aware positioning
- **Multiple Card Types**: Full cards, simple title cards, and minimal notes
- **Curved Slope Connections**: Gentle Bézier curves (not arcs) between branches
- **Harmonious Flow**: Cards flex dynamically based on content height
- **Subtle Color Palette**: Single-color pattern using subtle blue tints
- **Responsive**: Adapts to different screen sizes while maintaining elegance
- **Print-Ready**: Optimized CSS for printing

## Design Philosophy

The visualization occupies approximately 60% of the page content, serving as an elegant backdrop to the raw statistics and experience details. The design is:

- **Clean**: Two parallel timelines with no overlapping elements
- **Harmonious**: Dynamic spacing that flows naturally with content
- **Subtle**: Faded lines and minimal shadows that don't demand attention
- **Minimal**: Simple cards for side projects, detailed cards for major milestones
- **Professional**: Typography and spacing optimized for readability
- **Intuitive**: Clear visual separation of professional work and personal projects

## Structure

- `index.html` - Main HTML structure
- `styles.css` - Minimal, elegant styling with three card types
- `script.js` - JavaScript for rendering timelines with dynamic positioning

## Card Types

The visualization supports three display types:

### Full Cards (`displayType: 'full'`)
For major milestones like education and full-time work. Includes:
- Title and year
- Description paragraph
- Technology stack tags

### Simple Cards (`displayType: 'simple'`)
For side projects and ongoing work. Includes:
- Title and year only
- Smaller, more subtle appearance

### Minimal Notes (`displayType: 'note'`)
For small sub-projects. Includes:
- Brief title
- Optional detail note
- Tiny, unobtrusive display

## Sample Data

The visualization includes five example experiences:

### Main Timeline
1. **Bachelor - IT** (2016-2019) - Full card
   - Stack: Java, Python, SQL, Git, Linux, React, Node.js

2. **Full-time Frontend Dev** (2019-Present) - Full card
   - Stack: TypeScript, React, Vue.js, CSS3, Webpack, Jest, GraphQL

### Personal Timeline (branches from main)
3. **JS Canvas Projects Library** (2017-Present) - Simple card
   - Branches from Bachelor education

4. **Bash Utils Library** (2020-Present) - Simple card
   - Branches from Frontend Dev work

5. **Timesheet automation** - Minimal note
   - Sub-project under Bash Utils
   - Note: "vibe coding"

## Usage

Simply open `index.html` in a web browser. The visualization will render automatically with dynamic positioning to prevent overlaps.

## Customization

To add your own experiences, edit the `experiences` array in `script.js`:

### Full Card Example
```javascript
{
    id: 'my-experience',
    title: 'My Role',
    year: '2020 - 2023',
    description: 'Detailed description of the role and achievements.',
    stack: ['Tech1', 'Tech2', 'Tech3'],
    displayType: 'full',
    branch: 'main',
    timelinePos: 0
}
```

### Simple Card Example
```javascript
{
    id: 'side-project',
    title: 'My Side Project',
    year: '2021 - Present',
    displayType: 'simple',
    branch: 'personal',
    timelinePos: 1,
    parentId: 'my-experience',  // Branch from this item
    parentBranch: 'main'
}
```

### Minimal Note Example
```javascript
{
    id: 'small-task',
    title: 'Quick Project',
    note: 'weekend hack',
    displayType: 'note',
    branch: 'personal',
    timelinePos: 2,
    parentId: 'side-project'
}
```

## Timeline Branches

- **main**: Primary career path (education, professional work)
- **personal**: Side projects and personal work

The visualization automatically creates clean parallel lines for each branch with different styling:
- Main: Thicker line (#b8d0e0, 2px, 0.6 opacity)
- Personal: Thinner line (#d0dce5, 1.5px, 0.5 opacity)

## Color Scheme

The visualization uses a subtle blue color palette:
- Main branch: `#7fa8c4`
- Personal branch: `#9fb8cc`
- Main timeline: `#b8d0e0`
- Personal timeline: `#d0dce5`

All colors are chosen to be subtle and professional, supporting readability while adding visual elegance.

## Dynamic Layout

The layout system automatically:
- Calculates card heights based on content
- Positions cards to avoid overlaps
- Creates harmonious vertical flow
- Adjusts spacing dynamically

This ensures that if one card has more content, subsequent cards flow naturally beneath it without collision.
