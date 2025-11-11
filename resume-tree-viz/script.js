// Experience data structure with branch information
const experiences = [
    {
        id: 'bachelor',
        title: 'Bachelor - IT',
        year: '2016 - 2019',
        description: 'Comprehensive computer science education focusing on software engineering principles, algorithms, and modern web technologies.',
        stack: ['Java', 'Python', 'SQL', 'Git', 'Linux', 'React', 'Node.js'],
        displayType: 'full', // 'full' for detailed card, 'simple' for title only
        branch: 'main',
        timelinePos: 0
    },
    {
        id: 'canvas-lib',
        title: 'JS Canvas Projects Library',
        year: '2017 - Present',
        displayType: 'simple',
        branch: 'personal',
        timelinePos: 1,
        parentId: 'bachelor',
        parentBranch: 'main'
    },
    {
        id: 'frontend-dev',
        title: 'Full-time Frontend Dev',
        year: '2019 - Present',
        description: 'Building scalable, performant web applications with modern JavaScript frameworks. Focus on user experience and clean code architecture.',
        stack: ['TypeScript', 'React', 'Vue.js', 'CSS3', 'Webpack', 'Jest', 'GraphQL'],
        displayType: 'full',
        branch: 'main',
        timelinePos: 2
    },
    {
        id: 'bash-utils',
        title: 'Bash Utils Library',
        year: '2020 - Present',
        displayType: 'simple',
        branch: 'personal',
        timelinePos: 3,
        parentId: 'frontend-dev',
        parentBranch: 'main'
    },
    {
        id: 'timesheet-auto',
        title: 'Timesheet automation',
        note: 'vibe coding',
        displayType: 'note',
        branch: 'personal',
        timelinePos: 4,
        parentId: 'bash-utils'
    }
];

// Tree configuration
const treeConfig = {
    mainLineX: 80,
    personalLineX: 140,
    startY: 50,
    minRowGap: 30,
    cardOffsetX: 30,
    dotRadius: 5,
    colors: {
        main: '#7fa8c4',
        personal: '#9fb8cc',
        mainLine: '#b8d0e0',
        personalLine: '#d0dce5'
    }
};

// Initialize the visualization
function init() {
    const canvas = document.getElementById('treeCanvas');
    const container = document.getElementById('experiences');
    const containerRect = document.querySelector('.timeline-container').getBoundingClientRect();
    
    // First render all nodes to get their heights
    renderExperiences(container);
    
    // Calculate dynamic Y positions based on actual card heights
    calculateDynamicPositions(container);
    
    // Re-render with calculated positions
    renderExperiences(container);
    
    // Calculate SVG height based on final positions
    const maxY = Math.max(...experiences.map(e => e.calculatedY || 0)) + 100;
    canvas.setAttribute('width', containerRect.width);
    canvas.setAttribute('height', maxY);
    
    // Draw tree structure
    drawTree(canvas);
}

// Calculate Y positions dynamically to avoid overlaps
function calculateDynamicPositions(container) {
    let currentY = treeConfig.startY;
    
    experiences.forEach((exp, index) => {
        // Set X position based on branch
        exp.calculatedX = exp.branch === 'main' ? treeConfig.mainLineX : treeConfig.personalLineX;
        
        // For main branch, check if we need to skip space for personal branch items
        if (exp.branch === 'main' && index > 0) {
            // Check if any personal items need space before this main item
            const prevMainExp = experiences.slice(0, index).filter(e => e.branch === 'main').pop();
            const personalItemsBetween = experiences.slice(0, index).filter(e => 
                e.branch === 'personal' && 
                (!prevMainExp || e.timelinePos > prevMainExp.timelinePos)
            );
            
            // Calculate space needed for personal items
            personalItemsBetween.forEach(pExp => {
                const pElement = container.querySelector(`[data-id="${pExp.id}"]`);
                if (pElement) {
                    const height = pElement.offsetHeight;
                    currentY = Math.max(currentY, (pExp.calculatedY || 0) + height + treeConfig.minRowGap);
                }
            });
        }
        
        exp.calculatedY = currentY;
        
        // Add spacing based on the element's height if it exists
        const element = container.querySelector(`[data-id="${exp.id}"]`);
        if (element) {
            currentY += element.offsetHeight + treeConfig.minRowGap;
        } else {
            // Fallback heights
            if (exp.displayType === 'full') {
                currentY += 150;
            } else if (exp.displayType === 'simple') {
                currentY += 60;
            } else {
                currentY += 40;
            }
        }
    });
}

// Calculate positions - simplified for cleaner layout
function calculatePositions() {
    let currentY = treeConfig.startY;
    
    experiences.forEach(exp => {
        exp.calculatedX = exp.branch === 'main' ? treeConfig.mainLineX : treeConfig.personalLineX;
        exp.calculatedY = currentY;
        
        // Add spacing based on display type
        if (exp.displayType === 'full') {
            currentY += 150;
        } else if (exp.displayType === 'simple') {
            currentY += 70;
        } else {
            currentY += 50;
        }
    });
}

// Draw the tree structure with clean timelines
function drawTree(svg) {
    svg.innerHTML = '';
    
    // Get min and max Y for each branch
    const mainExps = experiences.filter(e => e.branch === 'main');
    const personalExps = experiences.filter(e => e.branch === 'personal');
    
    // Draw main timeline (thicker line)
    if (mainExps.length > 0) {
        const startY = Math.min(...mainExps.map(e => e.calculatedY));
        const endY = Math.max(...mainExps.map(e => e.calculatedY)) + 50;
        
        const mainLine = createPath([
            `M ${treeConfig.mainLineX} ${startY - 20}`,
            `L ${treeConfig.mainLineX} ${endY}`
        ]);
        mainLine.style.stroke = treeConfig.colors.mainLine;
        mainLine.style.strokeWidth = '2';
        mainLine.style.opacity = '0.6';
        svg.appendChild(mainLine);
    }
    
    // Draw personal timeline (thinner line, different color)
    if (personalExps.length > 0) {
        const startY = Math.min(...personalExps.map(e => e.calculatedY));
        const endY = Math.max(...personalExps.map(e => e.calculatedY)) + 50;
        
        const personalLine = createPath([
            `M ${treeConfig.personalLineX} ${startY - 20}`,
            `L ${treeConfig.personalLineX} ${endY}`
        ]);
        personalLine.style.stroke = treeConfig.colors.personalLine;
        personalLine.style.strokeWidth = '1.5';
        personalLine.style.opacity = '0.5';
        svg.appendChild(personalLine);
    }
    
    // Draw dots and connections
    experiences.forEach(exp => {
        const x = exp.calculatedX;
        const y = exp.calculatedY;
        const color = exp.branch === 'main' ? treeConfig.colors.main : treeConfig.colors.personal;
        
        // Draw dot at this point
        const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        dot.setAttribute('cx', x);
        dot.setAttribute('cy', y);
        dot.setAttribute('r', exp.displayType === 'note' ? '3' : '5');
        dot.style.fill = color;
        dot.style.opacity = '0.7';
        svg.appendChild(dot);
        
        // Draw curved slope branch if branching from another item
        if (exp.parentId && exp.branch !== experiences.find(e => e.id === exp.parentId)?.branch) {
            const parentExp = experiences.find(e => e.id === exp.parentId);
            if (parentExp) {
                const branchPath = createSlopeCurve(
                    parentExp.calculatedX,
                    parentExp.calculatedY,
                    x,
                    y
                );
                branchPath.style.stroke = color;
                branchPath.style.strokeWidth = '1.5';
                branchPath.style.opacity = '0.4';
                branchPath.style.fill = 'none';
                svg.appendChild(branchPath);
            }
        }
        
        // Draw connecting line to card
        if (exp.displayType !== 'note') {
            const cardX = x + treeConfig.cardOffsetX;
            const connectLine = createPath([
                `M ${x} ${y}`,
                `L ${cardX} ${y}`
            ]);
            connectLine.style.stroke = color;
            connectLine.style.strokeWidth = '1';
            connectLine.style.opacity = '0.3';
            svg.appendChild(connectLine);
        }
    });
}

// Create a curved slope path (not an arc)
function createSlopeCurve(x1, y1, x2, y2) {
    // Create a gentle slope curve using quadratic bezier
    const dx = x2 - x1;
    const dy = y2 - y1;
    
    // Control point creates a gentle slope
    const controlX = x1 + dx * 0.3;
    const controlY = y1 + dy * 0.7;
    
    const path = createPath([
        `M ${x1} ${y1}`,
        `Q ${controlX} ${controlY}, ${x2} ${y2}`
    ]);
    
    return path;
}

// Helper to create SVG path element
function createPath(commands) {
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', commands.join(' '));
    return path;
}

// Render experience nodes with dynamic layout
function renderExperiences(container) {
    container.innerHTML = '';
    
    experiences.forEach(exp => {
        const element = document.createElement('div');
        element.setAttribute('data-id', exp.id);
        
        if (exp.displayType === 'full') {
            // Full detailed card
            element.className = 'experience-card full-card';
            element.style.left = `${exp.calculatedX + treeConfig.cardOffsetX + 5}px`;
            element.style.top = `${exp.calculatedY - 25}px`;
            
            element.innerHTML = `
                <div class="card-header">
                    <div class="card-title">${exp.title}</div>
                    <div class="card-year">${exp.year}</div>
                </div>
                <div class="card-description">${exp.description}</div>
                <div class="card-stack">
                    ${exp.stack.map(tech => `<span class="stack-tag">${tech}</span>`).join('')}
                </div>
            `;
        } else if (exp.displayType === 'simple') {
            // Simple title-only card
            element.className = 'experience-card simple-card';
            element.style.left = `${exp.calculatedX + treeConfig.cardOffsetX + 5}px`;
            element.style.top = `${exp.calculatedY - 12}px`;
            
            element.innerHTML = `
                <div class="simple-title">${exp.title}</div>
                <div class="simple-year">${exp.year}</div>
            `;
        } else if (exp.displayType === 'note') {
            // Minimal note
            element.className = 'experience-note';
            element.style.left = `${exp.calculatedX + 15}px`;
            element.style.top = `${exp.calculatedY - 8}px`;
            
            element.innerHTML = `
                <span class="note-text">${exp.title}</span>
                ${exp.note ? `<span class="note-detail">${exp.note}</span>` : ''}
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
