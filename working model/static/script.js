// Advanced Malicious Link Detection Script with Animations and Interactive Elements

// Initialize the application when DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Focus on the input field when the page loads
    document.getElementById('link').focus();
    
    // Initialize tilt effect
    initializeTiltEffect();
    
    // Initialize particles background
    initializeParticles();
    
    // Add event listeners
    setupEventListeners();
});

// Initialize particles.js background
function initializeParticles() {
    // Check if particlesJS is loaded
    if (typeof particlesJS !== 'undefined') {
        // Load particles configuration
        // Configuration is in particles-config.js
        if (document.getElementById('particles-js')) {
            particlesJS('particles-js', {
                "particles": {
                    "number": {
                        "value": 120,
                        "density": {
                            "enable": true,
                            "value_area": 800
                        }
                    },
                    "color": {
                        "value": ["#e53935", "#ff5252", "#ffcdd2", "#ffffff"]
                    },
                    "shape": {
                        "type": ["circle", "triangle", "polygon"],
                        "stroke": {
                            "width": 0,
                            "color": "#000000"
                        },
                        "polygon": {
                            "nb_sides": 5
                        }
                    },
                    "opacity": {
                        "value": 0.7,
                        "random": true,
                        "anim": {
                            "enable": true,
                            "speed": 1,
                            "opacity_min": 0.1,
                            "sync": false
                        }
                    },
                    "size": {
                        "value": 5,
                        "random": true,
                        "anim": {
                            "enable": true,
                            "speed": 2,
                            "size_min": 0.3,
                            "sync": false
                        }
                    },
                    "line_linked": {
                        "enable": true,
                        "distance": 150,
                        "color": "#ffffff",
                        "opacity": 0.4,
                        "width": 1
                    },
                    "move": {
                        "enable": true,
                        "speed": 2,
                        "direction": "none",
                        "random": true,
                        "straight": false,
                        "out_mode": "out",
                        "bounce": false,
                        "attract": {
                            "enable": true,
                            "rotateX": 600,
                            "rotateY": 1200
                        }
                    }
                },
                "interactivity": {
                    "detect_on": "canvas",
                    "events": {
                        "onhover": {
                            "enable": true,
                            "mode": "grab"
                        },
                        "onclick": {
                            "enable": true,
                            "mode": "push"
                        },
                        "resize": true
                    },
                    "modes": {
                        "grab": {
                            "distance": 140,
                            "line_linked": {
                                "opacity": 1
                            }
                        },
                        "bubble": {
                            "distance": 400,
                            "size": 40,
                            "duration": 2,
                            "opacity": 8,
                            "speed": 3
                        },
                        "repulse": {
                            "distance": 200,
                            "duration": 0.4
                        },
                        "push": {
                            "particles_nb": 4
                        },
                        "remove": {
                            "particles_nb": 2
                        }
                    }
                },
                "retina_detect": true
            });
        }
    }
}



// Initialize tilt effect for glass panels
function initializeTiltEffect() {
    // Check if VanillaTilt is loaded
    if (typeof VanillaTilt !== 'undefined') {
        VanillaTilt.init(document.querySelectorAll('.tilt-effect'), {
            max: 5,
            speed: 400,
            glare: true,
            'max-glare': 0.2,
            scale: 1.03
        });
        
        // Special settings for about cards to make them more interactive
        VanillaTilt.init(document.querySelectorAll('.about-card'), {
            max: 10,
            speed: 400,
            glare: true,
            'max-glare': 0.3,
            scale: 1.05
        });
    }
}

// Setup all event listeners
function setupEventListeners() {
    // Submit button click event
    const checkButton = document.getElementById('check-button');
    if (checkButton) {
        checkButton.addEventListener('click', analyzeMaliciousLink);
    }
    
    // Enter key press event on input field
    const linkInput = document.getElementById('link');
    if (linkInput) {
        linkInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                analyzeMaliciousLink();
            }
        });
    }
}

// Main function to check if link is malicious
async function analyzeMaliciousLink() {
    const link = document.getElementById('link').value.trim();
    const resultBox = document.getElementById('result-box');
    const resultText = document.getElementById('result');
    const resultIcon = document.getElementById('result-icon');
    const confidenceMeter = document.querySelector('.meter-fill');
    const confidencePercent = document.getElementById('confidence-percent');
    const explanation = document.querySelector('.explanation');
    
    // Validate input
    if (!link) {
        // Shake animation for empty input
        const inputField = document.getElementById('link');
        inputField.classList.add('shake');
        setTimeout(() => {
            inputField.classList.remove('shake');
        }, 500);
        return;
    }
    
    try {
        // Show loading state
        document.getElementById('check-button').innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        document.getElementById('check-button').disabled = true;
        
        // Hide previous result if visible
        resultBox.classList.add('hidden');
        
        // Send request to the server
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `link=${encodeURIComponent(link)}`
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        // Calculate a random confidence percentage between 70-95% for demonstration
        // In a real app, this would come from the model
        const confidenceValue = data.result === 'Malicious' ? 
            Math.floor(Math.random() * 25) + 70 : 
            Math.floor(Math.random() * 25) + 70;
        
        // Update confidence meter
        confidenceMeter.style.width = `${confidenceValue}%`;
        confidencePercent.textContent = `${confidenceValue}%`;
        
        // Set result text and icon based on prediction
        if (data.result === 'Malicious') {
            resultText.textContent = 'Malicious Link Detected';
            resultText.style.color = '#d32f2f';
            resultIcon.className = 'fas fa-exclamation-triangle';
            resultIcon.style.color = '#d32f2f';
            explanation.textContent = 'This link contains suspicious patterns that may indicate malicious intent. Exercise caution.';
        } else {
            resultText.textContent = 'Safe Link';
            resultText.style.color = '#2e7d32';
            resultIcon.className = 'fas fa-check-circle';
            resultIcon.style.color = '#2e7d32';
            explanation.textContent = 'This link appears to be safe based on our analysis.';
        }
        
        // Show the result with animation
        resultBox.classList.remove('hidden');
        
    } catch (error) {
        console.error('Error:', error);
        resultText.textContent = 'Error analyzing link';
        resultText.style.color = '#ff9800';
        resultIcon.className = 'fas fa-exclamation-circle';
        resultIcon.style.color = '#ff9800';
        resultBox.classList.remove('hidden');
    } finally {
        // Reset button state
        document.getElementById('check-button').innerHTML = '<i class="fas fa-search"></i> Analyze Link';
        document.getElementById('check-button').disabled = false;
    }
}



// Add shake animation for invalid input
document.head.insertAdjacentHTML('beforeend', `
<style>
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
    20%, 40%, 60%, 80% { transform: translateX(5px); }
}
.shake {
    animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
}
</style>
`);
