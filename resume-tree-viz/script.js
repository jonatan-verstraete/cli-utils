// Timeline Renderer
// This file handles the rendering of the timeline visualization
// Data is loaded from timeline-data.js

// Get color based on timeline position
function getEventColor(index, total) {
    if (timelineConfig.colorMode === 'mono') {
        return timelineConfig.baseColor;
    } else {
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
    const maxY = Math.max(...timelineData.map(e => e.calculatedY || 0)) + 100;
    canvas.setAttribute('width', containerRect.width);
    canvas.setAttribute('height', maxY);
    
    // Draw tree structure
    drawTree(canvas);
    
    // Render experience nodes
    renderExperiences(container);
}

// Calculate positions for all events
function calculatePositions() {
    let currentY = timelineConfig.startY;
    
    timelineData.forEach((event, index) => {
        event.calculatedY = currentY;
        event.calculatedX = timelineConfig.timelineX;
        event.eventIndex = index;
        
        // Add spacing
        currentY += timelineConfig.eventSpacing;
    });
}

// Draw the timeline with dates on the line
function drawTree(svg) {
    svg.innerHTML = '';
    
    const totalEvents = timelineData.length;
    
    // Draw main vertical timeline
    const startY = timelineConfig.startY - 20;
    const endY = timelineData[timelineData.length - 1].calculatedY + 50;
    
    const timeline = createPath([
        `M ${timelineConfig.timelineX} ${startY}`,
        `L ${timelineConfig.timelineX} ${endY}`
    ]);
    timeline.style.stroke = '#d5dfe6';
    timeline.style.strokeWidth = timelineConfig.timelineWidth;
    timeline.style.opacity = '0.5';
    svg.appendChild(timeline);
    
    // Draw events
    timelineData.forEach((event, index) => {
        const x = event.calculatedX;
        const y = event.calculatedY;
        const eventColor = getEventColor(index, totalEvents);
        
        // Draw refined dot with white border
        const dotOuter = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        dotOuter.setAttribute('cx', x);
        dotOuter.setAttribute('cy', y);
        dotOuter.setAttribute('r', timelineConfig.dotRadius);
        dotOuter.style.fill = '#ffffff';
        dotOuter.style.filter = 'drop-shadow(0 1px 2px rgba(0,0,0,0.1))';
        svg.appendChild(dotOuter);
        
        const dotInner = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        dotInner.setAttribute('cx', x);
        dotInner.setAttribute('cy', y);
        dotInner.setAttribute('r', timelineConfig.dotRadius - timelineConfig.dotBorderWidth);
        dotInner.style.fill = eventColor;
        dotInner.style.opacity = '0.9';
        svg.appendChild(dotInner);
        
        // Draw horizontal line to content
        const lineEndX = event.side === 'right' 
            ? x + timelineConfig.rightOffset 
            : x - timelineConfig.leftOffset;
        
        const connectLine = createPath([
            `M ${x} ${y}`,
            `L ${lineEndX} ${y}`
        ]);
        connectLine.style.stroke = eventColor;
        connectLine.style.strokeWidth = timelineConfig.lineWidth;
        connectLine.style.opacity = '0.3';
        connectLine.setAttribute('data-event-id', event.id);
        svg.appendChild(connectLine);
        
        // Add date text on the line (SVG text)
        const dateText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        dateText.setAttribute('x', event.side === 'right' ? x + 10 : x - 10);
        dateText.setAttribute('y', y - 5);
        dateText.setAttribute('text-anchor', event.side === 'right' ? 'start' : 'end');
        dateText.style.fontSize = '10px';
        dateText.style.fill = '#95a5a6';
        dateText.style.fontWeight = '300';
        dateText.textContent = event.year;
        svg.appendChild(dateText);
    });
}

// Helper to create SVG path element
function createPath(commands) {
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', commands.join(' '));
    return path;
}

// Render experience content
function renderExperiences(container) {
    container.innerHTML = '';
    
    timelineData.forEach(event => {
        const y = event.calculatedY;
        
        if (event.side === 'right') {
            // Main content on the right
            const element = document.createElement('div');
            element.className = 'event-content event-right';
            element.setAttribute('data-id', event.id);
            
            // Position: title above line, content below
            const contentStartY = y;
            element.style.left = `${timelineConfig.timelineX + timelineConfig.rightOffset}px`;
            element.style.top = `${contentStartY}px`;
            
            element.innerHTML = `
                <h3 class="event-title">${event.title}</h3>
                <div class="event-description">${event.description}</div>
                ${event.stack ? `
                    <div class="event-stack">
                        ${event.stack.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                    </div>
                ` : ''}
            `;
            
            container.appendChild(element);
        } else {
            // Small events on the left
            const element = document.createElement('div');
            element.className = 'event-content event-left';
            element.setAttribute('data-id', event.id);
            
            // Position: aligned to line, text above line
            element.style.right = `${document.querySelector('.timeline-container').offsetWidth - timelineConfig.timelineX + timelineConfig.leftOffset}px`;
            element.style.top = `${y - 8}px`;
            
            element.innerHTML = `<p class="event-title-small">${event.title}</p>`;
            
            container.appendChild(element);
        }
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);

// Re-calculate on window resize
window.addEventListener('resize', () => {
    init();
});

