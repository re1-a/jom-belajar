import os
import re

with open('matematik-darjah2/style.css', 'r') as f:
    css = f.read()

# Replace root variables
replacements = {
    '--primary-color: #6C5CE7': '--primary-color: #00B894',
    '--secondary-color: #A29BFE': '--secondary-color: #55EFC4',
    '--accent-color: #FD79A8': '--accent-color: #FDCB6E',
    '--bg-color: #F0F3FF': '--bg-color: #F0FFF4',
    '--exam-color: #6C5CE7': '--kemahiran-color: #00B894',
    '--syllabus-color: #00B894': '--penerokaan-color: #0984E3',
    'exam-section': 'kemahiran-section',
    'syllabus-section': 'penerokaan-section'
}

for k, v in replacements.items():
    css = css.replace(k, v)

# Add drag and drop specific styles at the end
drag_drop_css = """

/* =========================================
   Sains Specific Styles (Drag & Drop, etc)
   ========================================= */

.drag-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-top: 15px;
}

.drop-zones-wrapper {
    display: flex;
    gap: 15px;
    justify-content: center;
    flex-wrap: wrap;
}

.drop-zone {
    flex: 1;
    min-width: 120px;
    min-height: 150px;
    border: 3px dashed var(--text-light);
    border-radius: 15px;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px;
    background: rgba(255, 255, 255, 0.5);
    transition: all 0.3s;
}

[data-theme="dark"] .drop-zone {
    background: rgba(0, 0, 0, 0.2);
}

.drop-zone.over {
    background: var(--secondary-color);
    border-color: var(--primary-color);
    transform: scale(1.05);
}

.drop-zone h4 {
    margin-bottom: 10px;
    font-size: 1.1rem;
    color: var(--text-main);
    pointer-events: none;
}

.draggable-items-wrapper {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    min-height: 60px;
    padding: 10px;
    background: var(--card-bg);
    border-radius: 15px;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.05);
}

.draggable {
    padding: 8px 15px;
    background: var(--primary-color);
    color: white;
    border-radius: 10px;
    cursor: grab;
    font-weight: bold;
    font-size: 1.1rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    user-select: none;
}

.draggable:active {
    cursor: grabbing;
    transform: scale(0.95);
}

.draggable.emoji-drag {
    font-size: 2.5rem;
    padding: 10px;
    background: white;
    border: 2px solid var(--primary-color);
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

[data-theme="dark"] .draggable.emoji-drag {
    background: #2d3436;
}

.icon-wrap {
    background: white;
    width: 40px; height: 40px;
    border-radius: 50%;
    display: flex; justify-content: center; align-items: center;
    color: var(--primary-color);
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
[data-theme="dark"] .icon-wrap { background: #2d3436; }

.kemahiran-section .icon-wrap { color: var(--kemahiran-color); }
.penerokaan-section .icon-wrap { color: var(--penerokaan-color); }

.bg-shape {
    position: fixed;
    border-radius: 50%;
    opacity: 0.5;
    filter: blur(60px);
    z-index: -1;
}
.shape-1 {
    width: 400px; height: 400px;
    background: var(--primary-color);
    top: -100px; left: -100px;
    animation: float 8s ease-in-out infinite;
}
.shape-2 {
    width: 300px; height: 300px;
    background: var(--accent-color);
    bottom: -50px; right: -50px;
    animation: float 10s ease-in-out infinite reverse;
}
.shape-3 {
    width: 200px; height: 200px;
    background: var(--secondary-color);
    top: 40%; left: 60%;
    animation: float 6s ease-in-out infinite;
}
"""

css += drag_drop_css

with open('sains-darjah2/style.css', 'w') as f:
    f.write(css)

print("style.css created successfully")
