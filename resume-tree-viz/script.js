// Experience data structure
const experiences = [
    {
        id: 'bachelor',
        title: 'Bachelor - IT',
        year: '2016 - 2019',
        description: 'Comprehensive computer science education focusing on software engineering principles, algorithms, and modern web technologies.',
        stack: ['Java', 'Python', 'SQL', 'Git', 'Linux', 'React', 'Node.js'],
        branch: 'education',
        position: { x: 150, y: 50 }
    },
    {
        id: 'frontend-dev',
        title: 'Full-time Frontend Dev',
        year: '2019 - Present',
        description: 'Building scalable, performant web applications with modern JavaScript frameworks. Focus on user experience and clean code architecture.',
        stack: ['TypeScript', 'React', 'Vue.js', 'CSS3', 'Webpack', 'Jest', 'GraphQL'],
        branch: 'professional',
        position: { x: 150, y: 280 }
    }
];

// Tree configuration
const treeConfig = {
    startPoint: { x: 80, y: 0 },
    mainLineLength: 520,
    branchOffset: 70,
    curveRadius: 30
};

// Initialize the visualization
function init() {
    const canvas = document.getElementById('treeCanvas');
    const container = document.getElementById('experiences');
    const containerRect = document.querySelector('.timeline-container').getBoundingClientRect();
    
    // Set SVG dimensions
    canvas.setAttribute('width', containerRect.width);
    canvas.setAttribute('height', containerRect.height);
    
    // Draw tree structure
    drawTree(canvas);
    
    // Render experience nodes
    renderExperiences(container);
}

// Draw the tree structure with SVG
function drawTree(svg) {
    const { startPoint, mainLineLength, branchOffset, curveRadius } = treeConfig;
    
    // Clear any existing content
    svg.innerHTML = '';
    
    // Create main vertical line
    const mainLine = createPath([
        `M ${startPoint.x} ${startPoint.y}`,
        `L ${startPoint.x} ${startPoint.y + mainLineLength}`
    ]);
    mainLine.classList.add('tree-line');
    svg.appendChild(mainLine);
    
    // Draw branches for each experience
    experiences.forEach((exp, index) => {
        const branchY = exp.position.y + 30; // Align with node center
        const nodeX = exp.position.x + 25; // Node left edge
        
        // Determine branch direction (alternate left/right for visual balance)
        const isLeft = index % 2 === 0;
        const horizontalStart = isLeft ? nodeX + 300 : nodeX; // Adjust based on node position
        
        // Create curved branch from main line to node
        const branchPath = createCurvedBranch(
            startPoint.x,
            branchY,
            horizontalStart,
            branchY,
            isLeft ? -curveRadius : curveRadius
        );
        
        branchPath.classList.add('tree-line');
        svg.appendChild(branchPath);
        
        // Add node dot at branch point
        const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        dot.setAttribute('cx', startPoint.x);
        dot.setAttribute('cy', branchY);
        dot.setAttribute('r', '4');
        dot.classList.add('tree-node-dot');
        svg.appendChild(dot);
        
        // Add subtle connecting line to node
        const connectLine = createPath([
            `M ${horizontalStart} ${branchY}`,
            `L ${nodeX} ${branchY}`
        ]);
        connectLine.classList.add('tree-line-fade');
        svg.appendChild(connectLine);
    });
}

// Create curved branch path
function createCurvedBranch(x1, y1, x2, y2, curveDirection) {
    const midX = (x1 + x2) / 2;
    const controlPoint = curveDirection;
    
    const path = createPath([
        `M ${x1} ${y1}`,
        `Q ${midX + controlPoint} ${y1}, ${midX} ${y1}`,
        `L ${x2} ${y2}`
    ]);
    
    return path;
}

// Helper to create SVG path element
function createPath(commands) {
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', commands.join(' '));
    return path;
}

// Render experience nodes
function renderExperiences(container) {
    experiences.forEach(exp => {
        const node = document.createElement('div');
        node.className = `experience-node branch-${exp.branch}`;
        node.style.left = `${exp.position.x}px`;
        node.style.top = `${exp.position.y}px`;
        
        node.innerHTML = `
            <div class="node-header">
                <div class="node-title">${exp.title}</div>
                <div class="node-year">${exp.year}</div>
            </div>
            <div class="node-description">${exp.description}</div>
            <div class="node-stack">
                ${exp.stack.map(tech => `<span class="stack-tag">${tech}</span>`).join('')}
            </div>
        `;
        
        container.appendChild(node);
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);

// Re-calculate on window resize
window.addEventListener('resize', () => {
    const canvas = document.getElementById('treeCanvas');
    const containerRect = document.querySelector('.timeline-container').getBoundingClientRect();
    canvas.setAttribute('width', containerRect.width);
    canvas.setAttribute('height', containerRect.height);
    drawTree(canvas);
});
