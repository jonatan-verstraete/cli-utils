# Resume Experience Tree Visualization

A minimal, elegant tree-view visualization for displaying programming experience on a resume. Designed to be subtle, professional, and ambient - providing visual interest without stealing attention from the content.

## Features

- **A4 Page Size**: Optimized for single-page resume printing (210mm × 297mm)
- **Minimal Design**: Hyper-minimalist with subtle lines and soft shadows
- **Git-like Branching**: Concurrent branches with curved connections similar to GitKraken
- **Multiple Concurrent Branches**: Show parallel career paths (work vs personal projects)
- **Sub-branches**: Minimal notes for smaller projects
- **Subtle Color Palette**: Single-color pattern using subtle blue tints
- **Responsive**: Adapts to different screen sizes while maintaining elegance
- **Print-Ready**: Optimized CSS for printing

## Design Philosophy

The visualization occupies approximately 60% of the page content, serving as an elegant backdrop to the raw statistics and experience details. The design is:

- **Slick**: Clean lines with subtle Bézier curves
- **Subtle**: Faded lines and minimal shadows that don't demand attention
- **Minimal**: Grayscale with subtle blue accents
- **Professional**: Typography and spacing optimized for readability
- **Intuitive**: Visual separation of professional work and personal projects

## Structure

- `index.html` - Main HTML structure
- `styles.css` - Minimal, elegant styling with subtle blue color scheme
- `script.js` - JavaScript for rendering the tree structure and experience nodes

## Sample Data

The visualization includes five example experiences across multiple branches:

### Main Branch (Education → Professional)
1. **Bachelor - IT** (2016-2019)
   - Education branch
   - Stack: Java, Python, SQL, Git, Linux, React, Node.js

2. **Full-time Frontend Dev** (2019-Present)
   - Professional work branch
   - Stack: TypeScript, React, Vue.js, CSS3, Webpack, Jest, GraphQL

### Personal Projects Branches
3. **JS Canvas Projects Library** (2017-Present)
   - Branches from education
   - Stack: JavaScript, Canvas API, WebGL

4. **Bash Utils Library** (2020-Present)
   - Branches from professional work
   - Stack: Bash, Shell Scripting, CLI Tools

5. **Timesheet automation** (Sub-branch)
   - Small project note under Bash Utils
   - Minimal display: "vibe coding"

## Usage

Simply open `index.html` in a web browser. The visualization will render automatically.

## Customization

To add your own experiences, edit the `experiences` array in `script.js`:

```javascript
const experiences = [
    {
        id: 'your-experience',
        title: 'Your Title',
        year: 'Year Range',
        description: 'Description of the experience',
        stack: ['Tech1', 'Tech2', 'Tech3'],
        type: 'main',           // 'main' for full cards, 'sub' for minimal notes
        branch: 'branch-name',  // Unique branch identifier
        branchLane: 0,          // Horizontal position (0, 1, 2...)
        timelinePos: 0,         // Vertical position (0, 1, 2...)
        parentBranch: 'parent'  // Optional: branch this splits from
    }
];
```

### For Sub-branches (Small Notes)
```javascript
{
    id: 'small-project',
    title: 'Project Name',
    note: 'additional detail',
    type: 'sub',
    branch: 'parent-branch',
    branchLane: 2,
    timelinePos: 4,
    parentId: 'parent-experience-id'
}
```

## Color Scheme

The visualization uses a subtle blue color palette with different tints per branch:
- Education: `#7fa8c4`
- Professional: `#6b92ab`
- Personal Creative: `#8eb3c9`
- Personal Tools: `#9fb8cc`
- Main Line: `#b8d0e0`
- Very Light: `#d5e3ed`

All colors are chosen to be subtle and professional, supporting readability while adding visual elegance.
