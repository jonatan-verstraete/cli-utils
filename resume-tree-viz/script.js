// Experience data structure - simplified
const experiences = [
    {
        id: 'bachelor',
        title: 'Bachelor - IT',
        year: '2016 - 2019',
        description: 'Comprehensive computer science education focusing on software engineering principles, algorithms, and modern web technologies.',
        stack: ['Java', 'Python', 'SQL', 'Git', 'Linux', 'React', 'Node.js'],
        side: 'right', // 'left' for small events/notes, 'right' for main content
        timelinePos: 0
    },
    {
        id: 'canvas-lib',
        title: 'JS Canvas Projects Library',
        year: '2017 - Present',
        side: 'left',
        timelinePos: 1
    },
    {
        id: 'frontend-dev',
        title: 'Full-time Frontend Dev',
        year: '2019 - Present',
        description: 'Building scalable, performant web applications with modern JavaScript frameworks. Focus on user experience and clean code architecture.',
        stack: ['TypeScript', 'React', 'Vue.js', 'CSS3', 'Webpack', 'Jest', 'GraphQL'],
        side: 'right',
        timelinePos: 2
    },
    {
        id: 'bash-utils',
        title: 'Bash Utils Library',
        year: '2020 - Present',
        side: 'left',
        timelinePos: 3
    },
    {
        id: 'timesheet-auto',
        title: 'Timesheet automation',
        year: '2021',
        side: 'left',
        timelinePos: 4
    }
];

// Tree configuration - left-aligned with hue coloring
const treeConfig = {
    timelineX: 180,      // Left-aligned timeline (minimal space for left events)
    startY: 50,
    rowGap: 130,         // Spacing between main cards
    leftOffset: 150,     // Space for left events
    rightOffset: 40,     // Space to right cards
    dotRadius: 5,
    dotBorderWidth: 2,
    lineWidth: 1.5,
    timelineWidth: 2,
    baseColor: '#7fa8c4',
    colorMode: 'hue'     // 'hue' or 'mono'
};

// Get color based on timeline position
function getEventColor(index, total) {
    if (treeConfig.colorMode === 'mono') {
        return treeConfig.baseColor;
    } else {
        // Hue-based color: rotate through hue spectrum
        const hue = (360 / total) * index;
        return `hsl(${hue}, 45%, 60%)`;
    }
}

// Initialize the visualization
function init() {
    const canvas = document.getElementById('treeCanvas');
    const container = document.getElementById('experiences');
    const containerRect = document.querySelector('.timeline-container').getBoundingClientRect();
    
    // Calculate positions
    calculatePositions();
    
    // Calculate SVG height
    const maxY = Math.max(...experiences.map(e => e.calculatedY || 0)) + 100;
    canvas.setAttribute('width', containerRect.width);
    canvas.setAttribute('height', maxY);
    
    // Draw tree structure
    drawTree(canvas);
    
    // Render experience nodes
    renderExperiences(container);
}

// Calculate positions - simple vertical spacing with gaps for main cards
function calculatePositions() {
    let currentY = treeConfig.startY;
    
    experiences.forEach((exp, index) => {
        exp.calculatedY = currentY;
        exp.calculatedX = treeConfig.timelineX;
        exp.eventIndex = index;
        
        // Add larger spacing after main content cards
        if (exp.side === 'right') {
            currentY += treeConfig.rowGap;
        } else {
            currentY += 60; // Smaller spacing for left events
        }
    });
}

// Draw the tree structure - refined modern design
function drawTree(svg) {
    svg.innerHTML = '';
    
    const totalEvents = experiences.length;
    
    // Draw single vertical timeline (thin, refined)
    const startY = treeConfig.startY - 20;
    const endY = experiences[experiences.length - 1].calculatedY + 50;
    
    const timeline = createPath([
        `M ${treeConfig.timelineX} ${startY}`,
        `L ${treeConfig.timelineX} ${endY}`
    ]);
    timeline.style.stroke = '#d5dfe6';
    timeline.style.strokeWidth = treeConfig.timelineWidth;
    timeline.style.opacity = '0.5';
    svg.appendChild(timeline);
    
    // Draw dots and horizontal lines for each event
    experiences.forEach((exp, index) => {
        const x = exp.calculatedX;
        const y = exp.calculatedY;
        const eventColor = getEventColor(index, totalEvents);
        
        // Draw refined dot with white border (5px with 2px white border)
        const dotOuter = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        dotOuter.setAttribute('cx', x);
        dotOuter.setAttribute('cy', y);
        dotOuter.setAttribute('r', treeConfig.dotRadius);
        dotOuter.style.fill = '#ffffff';
        dotOuter.style.filter = 'drop-shadow(0 1px 2px rgba(0,0,0,0.1))';
        svg.appendChild(dotOuter);
        
        const dotInner = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        dotInner.setAttribute('cx', x);
        dotInner.setAttribute('cy', y);
        dotInner.setAttribute('r', treeConfig.dotRadius - treeConfig.dotBorderWidth);
        dotInner.style.fill = eventColor;
        dotInner.style.opacity = '0.9';
        svg.appendChild(dotInner);
        
        // Draw thin horizontal line to the card
        const lineEndX = exp.side === 'right' 
            ? x + treeConfig.rightOffset 
            : x - treeConfig.leftOffset;
        
        const connectLine = createPath([
            `M ${x} ${y}`,
            `L ${lineEndX} ${y}`
        ]);
        connectLine.style.stroke = eventColor;
        connectLine.style.strokeWidth = treeConfig.lineWidth;
        connectLine.style.opacity = '0.3';
        svg.appendChild(connectLine);
    });
}

// Helper to create SVG path element
function createPath(commands) {
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', commands.join(' '));
    return path;
}

// Render experience nodes - refined layout
function renderExperiences(container) {
    container.innerHTML = '';
    
    experiences.forEach(exp => {
        const element = document.createElement('div');
        element.setAttribute('data-id', exp.id);
        
        const y = exp.calculatedY;
        
        if (exp.side === 'right') {
            // Main content on the right - full detailed cards with spacing
            element.className = 'experience-main';
            element.style.left = `${treeConfig.timelineX + treeConfig.rightOffset + 5}px`;
            element.style.top = `${y - 30}px`;
            
            element.innerHTML = `
                <div class="main-header">
                    <div class="main-title">${exp.title}</div>
                    <div class="main-year">${exp.year}</div>
                </div>
                <div class="main-description">${exp.description}</div>
                <div class="main-stack">
                    ${exp.stack.map(tech => `<span class="stack-tag">${tech}</span>`).join('')}
                </div>
            `;
        } else {
            // Small events on the left - simple p tags
            element.className = 'experience-note';
            element.style.right = `${document.querySelector('.timeline-container').offsetWidth - treeConfig.timelineX + treeConfig.leftOffset - 5}px`;
            element.style.top = `${y - 12}px`;
            element.style.textAlign = 'right';
            
            element.innerHTML = `
                <p class="note-title">${exp.title}</p>
                <p class="note-year">${exp.year}</p>
            `;
        }
        
        container.appendChild(element);
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);

// Re-calculate on window resize
window.addEventListener('resize', () => {
    init();
});
