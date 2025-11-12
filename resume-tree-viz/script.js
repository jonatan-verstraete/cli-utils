// Timeline Renderer
// This file handles the rendering of the timeline visualization
// Data is loaded from timeline-data.js

// Get color based on timeline position
function getEventColor(index, total) {
    if (timelineConfig.colorMode === 'mono') {
        return timelineConfig.baseColor;
    } else if (timelineConfig.colorMode === 'blueGradient') {
        // Grayscale blue gradient: darker to lighter blue with low saturation
        const lightness = 35 + (index / (total - 1)) * 25; // 35% to 60%
        const saturation = 15 + (index / (total - 1)) * 15; // 15% to 30%
        return `hsl(210, ${saturation}%, ${lightness}%)`;
    } else {
        // Original hue mode
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
    const startY = timelineConfig.startY - 20;
    const endY = timelineData[timelineData.length - 1].calculatedY + 50;
    
    // Create defs for gradients and filters
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    
    // Create gradient for main timeline (darker neutral blue with gradient)
    const gradientId = 'timelineGradient';
    const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
    gradient.setAttribute('id', gradientId);
    gradient.setAttribute('x1', '0%');
    gradient.setAttribute('y1', '0%');
    gradient.setAttribute('x2', '0%');
    gradient.setAttribute('y2', '100%');
    
    const fadeLength = 40; // pixels to fade at ends
    const totalLength = endY - startY;
    
    // Base color: darker neutral blue (low saturation grayscale-ish)
    const baseColor = 'hsl(210, 12%, 45%)'; // Darker, neutral blue-gray
    
    // Top fade
    const topStop = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
    topStop.setAttribute('offset', '0%');
    topStop.setAttribute('stop-color', baseColor);
    topStop.setAttribute('stop-opacity', '0.2');
    gradient.appendChild(topStop);
    
    const topFadeStop = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
    topFadeStop.setAttribute('offset', `${(fadeLength / totalLength) * 100}%`);
    topFadeStop.setAttribute('stop-color', baseColor);
    topFadeStop.setAttribute('stop-opacity', '0.8');
    gradient.appendChild(topFadeStop);
    
    // Event color influences (subtle variations in the blue gradient)
    timelineData.forEach((event, index) => {
        const eventColor = getEventColor(index, totalEvents);
        const yPercent = ((event.calculatedY - startY) / totalLength) * 100;
        
        // Add color stops slightly before and after each event
        const colorStop1 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        colorStop1.setAttribute('offset', `${Math.max(0, yPercent - 2)}%`);
        colorStop1.setAttribute('stop-color', baseColor);
        colorStop1.setAttribute('stop-opacity', '0.8');
        gradient.appendChild(colorStop1);
        
        const colorStop2 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        colorStop2.setAttribute('offset', `${yPercent}%`);
        colorStop2.setAttribute('stop-color', eventColor);
        colorStop2.setAttribute('stop-opacity', '0.7');
        gradient.appendChild(colorStop2);
        
        const colorStop3 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        colorStop3.setAttribute('offset', `${Math.min(100, yPercent + 2)}%`);
        colorStop3.setAttribute('stop-color', baseColor);
        colorStop3.setAttribute('stop-opacity', '0.8');
        gradient.appendChild(colorStop3);
    });
    
    // Bottom fade
    const bottomFadeStop = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
    bottomFadeStop.setAttribute('offset', `${100 - (fadeLength / totalLength) * 100}%`);
    bottomFadeStop.setAttribute('stop-color', baseColor);
    bottomFadeStop.setAttribute('stop-opacity', '0.8');
    gradient.appendChild(bottomFadeStop);
    
    const bottomStop = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
    bottomStop.setAttribute('offset', '100%');
    bottomStop.setAttribute('stop-color', baseColor);
    bottomStop.setAttribute('stop-opacity', '0.2');
    gradient.appendChild(bottomStop);
    
    defs.appendChild(gradient);
    
    // Create subtle shadow filter for dots
    const dotFilter = document.createElementNS('http://www.w3.org/2000/svg', 'filter');
    dotFilter.setAttribute('id', 'dotShadow');
    dotFilter.setAttribute('x', '-100%');
    dotFilter.setAttribute('y', '-100%');
    dotFilter.setAttribute('width', '300%');
    dotFilter.setAttribute('height', '300%');
    
    const feDropShadow = document.createElementNS('http://www.w3.org/2000/svg', 'feDropShadow');
    feDropShadow.setAttribute('dx', '0');
    feDropShadow.setAttribute('dy', '1');
    feDropShadow.setAttribute('stdDeviation', '1.2');
    feDropShadow.setAttribute('flood-opacity', '0.2');
    dotFilter.appendChild(feDropShadow);
    
    defs.appendChild(dotFilter);
    svg.appendChild(defs);
    
    // Draw main vertical timeline with gradient
    const timeline = createPath([
        `M ${timelineConfig.timelineX} ${startY}`,
        `L ${timelineConfig.timelineX} ${endY}`
    ]);
    timeline.style.stroke = `url(#${gradientId})`;
    timeline.style.strokeWidth = '2';
    svg.appendChild(timeline);
    
    // Draw events
    timelineData.forEach((event, index) => {
        const x = event.calculatedX;
        const y = event.calculatedY;
        const eventColor = getEventColor(index, totalEvents);
        
        // Create gradient for horizontal line (fades at tip)
        const lineGradientId = `lineGradient-${event.id}`;
        const lineGradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
        lineGradient.setAttribute('id', lineGradientId);
        
        const lineEndX = event.side === 'right' 
            ? x + timelineConfig.rightOffset + timelineConfig.rightLineLength
            : x - timelineConfig.leftOffset - timelineConfig.leftLineLength;
        
        if (event.side === 'right') {
            lineGradient.setAttribute('x1', '0%');
            lineGradient.setAttribute('x2', '100%');
            
            const startStop = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
            startStop.setAttribute('offset', '0%');
            startStop.setAttribute('stop-color', eventColor);
            startStop.setAttribute('stop-opacity', '0.25');
            lineGradient.appendChild(startStop);
            
            const midStop = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
            midStop.setAttribute('offset', '80%');
            midStop.setAttribute('stop-color', eventColor);
            midStop.setAttribute('stop-opacity', '0.15');
            lineGradient.appendChild(midStop);
            
            const endStop = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
            endStop.setAttribute('offset', '100%');
            endStop.setAttribute('stop-color', eventColor);
            endStop.setAttribute('stop-opacity', '0');
            lineGradient.appendChild(endStop);
        } else {
            lineGradient.setAttribute('x1', '100%');
            lineGradient.setAttribute('x2', '0%');
            
            const startStop = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
            startStop.setAttribute('offset', '0%');
            startStop.setAttribute('stop-color', eventColor);
            startStop.setAttribute('stop-opacity', '0.25');
            lineGradient.appendChild(startStop);
            
            const midStop = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
            midStop.setAttribute('offset', '80%');
            midStop.setAttribute('stop-color', eventColor);
            midStop.setAttribute('stop-opacity', '0.15');
            lineGradient.appendChild(midStop);
            
            const endStop = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
            endStop.setAttribute('offset', '100%');
            endStop.setAttribute('stop-color', eventColor);
            endStop.setAttribute('stop-opacity', '0');
            lineGradient.appendChild(endStop);
        }
        
        defs.appendChild(lineGradient);
        
        // Draw refined dot with white border and shadow
        const dotOuter = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        dotOuter.setAttribute('cx', x);
        dotOuter.setAttribute('cy', y);
        dotOuter.setAttribute('r', timelineConfig.dotRadius);
        dotOuter.style.fill = '#ffffff';
        dotOuter.style.filter = 'url(#dotShadow)';
        svg.appendChild(dotOuter);
        
        const dotInner = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        dotInner.setAttribute('cx', x);
        dotInner.setAttribute('cy', y);
        dotInner.setAttribute('r', timelineConfig.dotRadius - timelineConfig.dotBorderWidth);
        dotInner.style.fill = eventColor;
        svg.appendChild(dotInner);
        
        // Draw horizontal line with gradient fade
        const connectLine = createPath([
            `M ${x} ${y}`,
            `L ${lineEndX} ${y}`
        ]);
        connectLine.style.stroke = `url(#${lineGradientId})`;
        connectLine.style.strokeWidth = '1';
        connectLine.setAttribute('data-event-id', event.id);
        svg.appendChild(connectLine);
        
        // Add date text on the line
        const dateText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        dateText.setAttribute('x', event.side === 'right' ? x + 10 : x - 10);
        dateText.setAttribute('y', y - 5);
        dateText.setAttribute('text-anchor', event.side === 'right' ? 'start' : 'end');
        dateText.classList.add('timeline-date');
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
            const contentStartY = y - 15;
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
            element.style.top = `${y + 2}px`;
            
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

