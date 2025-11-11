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

// Tree configuration - simplified
const treeConfig = {
    centerLineX: 300,  // Center timeline position
    startY: 50,
    rowGap: 100,
    leftOffset: 250,   // How far left from center
    rightOffset: 40,   // How far right from center
    dotRadius: 5,
    lineColor: '#b8d0e0'
};

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

// Calculate positions - simple vertical spacing
function calculatePositions() {
    experiences.forEach(exp => {
        exp.calculatedY = treeConfig.startY + (exp.timelinePos * treeConfig.rowGap);
        exp.calculatedX = treeConfig.centerLineX;
    });
}

// Draw the tree structure - single center timeline
function drawTree(svg) {
    svg.innerHTML = '';
    
    // Draw single vertical timeline in the center
    const startY = treeConfig.startY - 20;
    const endY = experiences[experiences.length - 1].calculatedY + 50;
    
    const timeline = createPath([
        `M ${treeConfig.centerLineX} ${startY}`,
        `L ${treeConfig.centerLineX} ${endY}`
    ]);
    timeline.style.stroke = treeConfig.lineColor;
    timeline.style.strokeWidth = '2';
    timeline.style.opacity = '0.6';
    svg.appendChild(timeline);
    
    // Draw dots and simple horizontal lines for each event
    experiences.forEach(exp => {
        const x = exp.calculatedX;
        const y = exp.calculatedY;
        
        // Draw dot at this point
        const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        dot.setAttribute('cx', x);
        dot.setAttribute('cy', y);
        dot.setAttribute('r', treeConfig.dotRadius);
        dot.style.fill = '#7fa8c4';
        dot.style.opacity = '0.7';
        svg.appendChild(dot);
        
        // Draw simple horizontal line to the card
        const lineEndX = exp.side === 'right' 
            ? x + treeConfig.rightOffset 
            : x - treeConfig.leftOffset;
        
        const connectLine = createPath([
            `M ${x} ${y}`,
            `L ${lineEndX} ${y}`
        ]);
        connectLine.style.stroke = treeConfig.lineColor;
        connectLine.style.strokeWidth = '1';
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

// Render experience nodes - simplified layout
function renderExperiences(container) {
    container.innerHTML = '';
    
    experiences.forEach(exp => {
        const element = document.createElement('div');
        element.setAttribute('data-id', exp.id);
        
        const y = exp.calculatedY;
        
        if (exp.side === 'right') {
            // Main content on the right - full detailed cards
            element.className = 'experience-main';
            element.style.left = `${treeConfig.centerLineX + treeConfig.rightOffset + 5}px`;
            element.style.top = `${y - 25}px`;
            
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
            // Small events on the left - simple notes
            element.className = 'experience-note';
            element.style.right = `${document.querySelector('.timeline-container').offsetWidth - treeConfig.centerLineX + treeConfig.leftOffset - 5}px`;
            element.style.top = `${y - 10}px`;
            element.style.textAlign = 'right';
            
            element.innerHTML = `
                <div class="note-title">${exp.title}</div>
                <div class="note-year">${exp.year}</div>
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
