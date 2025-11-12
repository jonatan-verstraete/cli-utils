// Timeline Experience Data Configuration
// 
// Add your experiences here in chronological order.
// Each event should have the following structure:

const timelineData = [
    {
        // Unique identifier
        id: 'bachelor',
        
        // Event title
        title: 'Bachelor - IT',
        
        // Year or date range
        year: '2016 - 2019',
        
        // Side of timeline: 'left' for small events, 'right' for main content
        side: 'right',
        
        // Optional: Full description (only for 'right' side events)
        description: 'Comprehensive computer science education focusing on software engineering principles, algorithms, and modern web technologies.',
        
        // Optional: Technology stack (only for 'right' side events)
        stack: ['Java', 'Python', 'SQL', 'Git', 'Linux', 'React', 'Node.js']
    },
    {
        id: 'canvas-lib',
        title: 'JS Canvas Projects Library',
        year: '2017',
        side: 'left'
    },
    {
        id: 'frontend-dev',
        title: 'Full-time Frontend Engineer',
        year: '2019-2025',
        side: 'right',
        description: 'Building scalable, performant web applications with modern JavaScript frameworks. Focus on user experience and clean code architecture.',
        stack: ['TypeScript', 'React', 'Vue.js', 'CSS3', 'Webpack', 'Jest', 'GraphQL']
    },
    {
        id: 'bash-utils',
        title: 'Bash Utils Library',
        year: '2020',
        side: 'left'
    },
    {
        id: 'timesheet-auto',
        title: 'Timesheet automation',
        year: '2021',
        side: 'left'
    }
];

// Timeline Configuration
const timelineConfig = {
    // Timeline position from left edge
    timelineX: 120,
    
    // Starting Y position
    startY: 50,
    
    // Vertical spacing between events
    eventSpacing: 100,
    
    // Dot styling
    dotRadius: 5,
    dotBorderWidth: 2,
    
    // Color mode: 'hue' for spectrum colors, 'mono' for single color, 'blueGradient' for grayscale blue gradient
    colorMode: 'blueGradient',
    baseColor: '#7fa8c4'
};
