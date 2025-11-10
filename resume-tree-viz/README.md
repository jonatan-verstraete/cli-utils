# Resume Experience Tree Visualization

A minimal, elegant tree-view visualization for displaying programming experience on a resume. Designed to be subtle, professional, and ambient - providing visual interest without stealing attention from the content.

## Features

- **A4 Page Size**: Optimized for single-page resume printing (210mm × 297mm)
- **Minimal Design**: Hyper-minimalist with subtle lines and soft shadows
- **Tree Structure**: Git-like branching visualization showing career progression
- **Subtle Color Palette**: Single-color pattern using subtle blue tints
- **Responsive**: Adapts to different screen sizes while maintaining elegance
- **Print-Ready**: Optimized CSS for printing

## Design Philosophy

The visualization occupies approximately 60% of the page content, serving as an elegant backdrop to the raw statistics and experience details. The design is:

- **Slick**: Clean lines with subtle curves
- **Subtle**: Faded lines and minimal shadows that don't demand attention
- **Minimal**: Grayscale with subtle blue accents
- **Professional**: Typography and spacing optimized for readability

## Structure

- `index.html` - Main HTML structure
- `styles.css` - Minimal, elegant styling with subtle blue color scheme
- `script.js` - JavaScript for rendering the tree structure and experience nodes

## Sample Data

The visualization includes two example experiences:

1. **Bachelor - IT** (2016-2019)
   - Education branch
   - Stack: Java, Python, SQL, Git, Linux, React, Node.js

2. **Full-time Frontend Dev** (2019-Present)
   - Professional work branch
   - Stack: TypeScript, React, Vue.js, CSS3, Webpack, Jest, GraphQL

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
        branch: 'education' or 'professional',
        position: { x: 150, y: 50 }
    }
];
```

## Color Scheme

The visualization uses a subtle blue color palette:
- Primary: `#4a7c9e`
- Accent: `#7fa8c4`
- Light: `#b8d0e0`
- Very Light: `#d5e3ed`

All colors are chosen to be subtle and professional, supporting readability while adding visual elegance.
