// Experience data structure with branch information
const experiences = [
    {
        id: 'bachelor',
        title: 'Bachelor - IT',
        year: '2016 - 2019',
        description: 'Comprehensive computer science education focusing on software engineering principles, algorithms, and modern web technologies.',
        stack: ['Java', 'Python', 'SQL', 'Git', 'Linux', 'React', 'Node.js'],
        type: 'main',
        branch: 'education',
        branchLane: 0,
        timelinePos: 0
    },
    {
        id: 'canvas-lib',
        title: 'JS Canvas Projects Library',
        year: '2017 - Present',
        description: 'Personal collection of creative coding experiments and reusable canvas utilities for interactive visualizations.',
        stack: ['JavaScript', 'Canvas API', 'WebGL'],
        type: 'main',
        branch: 'personal-creative',
        branchLane: 1,
        timelinePos: 1,
        parentBranch: 'education'
    },
    {
        id: 'frontend-dev',
        title: 'Full-time Frontend Dev',
        year: '2019 - Present',
        description: 'Building scalable, performant web applications with modern JavaScript frameworks. Focus on user experience and clean code architecture.',
        stack: ['TypeScript', 'React', 'Vue.js', 'CSS3', 'Webpack', 'Jest', 'GraphQL'],
        type: 'main',
        branch: 'professional',
        branchLane: 0,
        timelinePos: 2
    },
    {
        id: 'bash-utils',
        title: 'Bash Utils Library',
        year: '2020 - Present',
        description: 'CLI automation scripts and shell utilities for developer productivity and workflow optimization.',
        stack: ['Bash', 'Shell Scripting', 'CLI Tools'],
        type: 'main',
        branch: 'personal-tools',
        branchLane: 2,
        timelinePos: 3,
        parentBranch: 'professional'
    },
    {
        id: 'timesheet-auto',
        title: 'Timesheet automation',
        note: 'vibe coding',
        type: 'sub',
        branch: 'personal-tools',
        branchLane: 2,
        timelinePos: 4,
        parentId: 'bash-utils'
    }
];

// Tree configuration
const treeConfig = {
    startPoint: { x: 100, y: 30 },
    laneWidth: 150,
    rowHeight: 120,
    curveRadius: 20,
    dotRadius: 4,
    mainLineColor: '#b8d0e0',
    branchColors: {
        'education': '#7fa8c4',
        'professional': '#6b92ab',
        'personal-creative': '#8eb3c9',
        'personal-tools': '#9fb8cc'
    }
};

// Initialize the visualization
function init() {
    const canvas = document.getElementById('treeCanvas');
    const container = document.getElementById('experiences');
    const containerRect = document.querySelector('.timeline-container').getBoundingClientRect();
    
    // Calculate positions for all experiences
    calculatePositions();
    
    // Set SVG dimensions dynamically
    const maxY = Math.max(...experiences.map(e => e.calculatedY || 0)) + 150;
    canvas.setAttribute('width', containerRect.width);
    canvas.setAttribute('height', Math.max(maxY, 600));
    
    // Draw tree structure
    drawTree(canvas);
    
    // Render experience nodes
    renderExperiences(container);
}

// Calculate positions for all experiences based on timeline and lanes
function calculatePositions() {
    experiences.forEach(exp => {
        exp.calculatedX = treeConfig.startPoint.x + (exp.branchLane * treeConfig.laneWidth);
        exp.calculatedY = treeConfig.startPoint.y + (exp.timelinePos * treeConfig.rowHeight);
    });
}

// Draw the tree structure with SVG (git-like with concurrent branches)
function drawTree(svg) {
    svg.innerHTML = '';
    
    // Draw vertical lines for each branch lane
    const lanes = [...new Set(experiences.map(e => e.branchLane))].sort();
    lanes.forEach(lane => {
        const laneExps = experiences.filter(e => e.branchLane === lane).sort((a, b) => a.timelinePos - b.timelinePos);
        if (laneExps.length > 0) {
            const x = treeConfig.startPoint.x + (lane * treeConfig.laneWidth);
            const startY = laneExps[0].calculatedY;
            const endY = laneExps[laneExps.length - 1].calculatedY;
            
            const laneLine = createPath([
                `M ${x} ${startY}`,
                `L ${x} ${endY + 50}`
            ]);
            laneLine.classList.add('tree-line');
            laneLine.style.stroke = treeConfig.mainLineColor;
            svg.appendChild(laneLine);
        }
    });
    
    // Draw branch connections and dots
    experiences.forEach(exp => {
        const x = exp.calculatedX;
        const y = exp.calculatedY;
        const color = treeConfig.branchColors[exp.branch] || treeConfig.mainLineColor;
        
        // Draw dot at this commit/experience
        const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        dot.setAttribute('cx', x);
        dot.setAttribute('cy', y);
        dot.setAttribute('r', exp.type === 'sub' ? '3' : '5');
        dot.classList.add('tree-node-dot');
        dot.style.fill = color;
        svg.appendChild(dot);
        
        // Draw curved branch if this is a new branch
        if (exp.parentBranch) {
            const parentExp = experiences.find(e => e.branch === exp.parentBranch);
            if (parentExp) {
                const startX = parentExp.calculatedX;
                const startY = parentExp.calculatedY;
                const branchPath = createCurvedBranchPath(startX, startY, x, y);
                branchPath.classList.add('tree-line');
                branchPath.style.stroke = color;
                svg.appendChild(branchPath);
            }
        }
        
        // Draw connection to parent commit in same branch (sub-branches)
        if (exp.parentId) {
            const parentExp = experiences.find(e => e.id === exp.parentId);
            if (parentExp && parentExp.branchLane === exp.branchLane) {
                const startX = parentExp.calculatedX;
                const startY = parentExp.calculatedY;
                const subBranchPath = createCurvedBranchPath(startX, startY, x, y);
                subBranchPath.classList.add('tree-line-fade');
                subBranchPath.style.stroke = color;
                svg.appendChild(subBranchPath);
            }
        }
        
        // Draw connecting line to the experience card
        if (exp.type === 'main') {
            const cardX = x + 30;
            const connectLine = createPath([
                `M ${x} ${y}`,
                `L ${cardX} ${y}`
            ]);
            connectLine.classList.add('tree-line-fade');
            connectLine.style.stroke = color;
            svg.appendChild(connectLine);
        }
    });
}

// Create curved branch path using quadratic Bezier curves (git-like)
function createCurvedBranchPath(x1, y1, x2, y2) {
    const midY = (y1 + y2) / 2;
    const controlX1 = x1;
    const controlY1 = midY;
    const controlX2 = x2;
    const controlY2 = midY;
    
    const path = createPath([
        `M ${x1} ${y1}`,
        `C ${controlX1} ${controlY1}, ${controlX2} ${controlY2}, ${x2} ${y2}`
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
    container.innerHTML = '';
    
    experiences.forEach(exp => {
        if (exp.type === 'main') {
            // Full experience card
            const node = document.createElement('div');
            node.className = `experience-node branch-${exp.branch}`;
            node.style.left = `${exp.calculatedX + 35}px`;
            node.style.top = `${exp.calculatedY - 30}px`;
            
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
        } else if (exp.type === 'sub') {
            // Small note for sub-branches
            const note = document.createElement('div');
            note.className = 'sub-branch-note';
            note.style.left = `${exp.calculatedX + 15}px`;
            note.style.top = `${exp.calculatedY - 10}px`;
            
            note.innerHTML = `
                <div class="note-title">${exp.title}</div>
                ${exp.note ? `<div class="note-detail">${exp.note}</div>` : ''}
            `;
            
            container.appendChild(note);
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);

// Re-calculate on window resize
window.addEventListener('resize', () => {
    init();
});
