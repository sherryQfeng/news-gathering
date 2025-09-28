// Simple News Hub - JavaScript Interactions

// Show modal with message
function showModal(message, isError = false) {
    const modal = document.getElementById('messageModal');
    const modalMessage = document.getElementById('modalMessage');
    
    if (modal && modalMessage) {
        modalMessage.innerHTML = message;
        modal.style.display = 'flex';
        
        // Add some animation
        modal.style.opacity = '0';
        setTimeout(() => {
            modal.style.opacity = '1';
        }, 10);
    }
}

// Close modal
function closeModal() {
    const modal = document.getElementById('messageModal');
    if (modal) {
        modal.style.opacity = '0';
        setTimeout(() => {
            modal.style.display = 'none';
        }, 200);
    }
}

// Refresh feeds functionality
async function refreshFeeds() {
    showModal('🔄 Refreshing news feeds...');
    
    try {
        const response = await fetch('/refresh');
        const data = await response.json();
        
        if (data.success) {
            showModal(`✅ Added ${data.new_count} new articles! Refreshing page...`);
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            showModal(`❌ Error: ${data.message}`);
        }
    } catch (error) {
        showModal(`❌ Network error: ${error.message}`);
    }
}

// Send digest functionality
async function sendDigest() {
    showModal('📧 Sending email digest...');
    
    try {
        const response = await fetch('/send-digest');
        const data = await response.json();
        
        if (data.success) {
            showModal('✅ Email sent! Check your inbox.');
        } else {
            showModal(`❌ Email failed: ${data.message}`);
        }
    } catch (error) {
        showModal(`❌ Network error: ${error.message}`);
    }
}

// Show statistics
async function showStats() {
    showModal('📊 Blathers is calculating statistics! Please wait... 🦉');
    
    try {
        const response = await fetch('/stats');
        const data = await response.json();
        
        const statsHtml = `
            <div style="text-align: left; line-height: 1.6;">
                <h3 style="text-align: center; margin-bottom: 20px;">📊 News Hub Statistics 📊</h3>
                
                <div style="margin-bottom: 15px;">
                    <strong>📰 Total Articles:</strong> ${data.total_articles}
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong>🤖 AI Articles:</strong> ${data.ai_articles}
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong>💰 Economics/Politics:</strong> ${data.econ_articles}
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong>🆕 Today's Articles:</strong> ${data.today_articles}
                </div>
                
                <div style="margin-bottom: 20px;">
                    <strong>📅 This Week:</strong> ${data.week_articles}
                </div>
                
                <div style="border-top: 2px solid #8FBC8F; padding-top: 15px;">
                    <strong>🏆 Top News Sources:</strong><br>
                    ${data.top_sources.map((source, index) => 
                        `${index + 1}. ${source.name} (${source.count} articles)`
                    ).join('<br>')}
                </div>
                
                <div style="text-align: center; margin-top: 20px; font-style: italic; color: #666;">
                    🦉 "Fascinating data indeed!" - Blathers
                </div>
            </div>
        `;
        
        showModal(statsHtml);
    } catch (error) {
        showModal(`❌ Error loading statistics: ${error.message}<br><br>📊 Blathers is having trouble with his calculations!`, true);
    }
}

// Add some fun Easter eggs and interactions
document.addEventListener('DOMContentLoaded', function() {
    // Add click animations to article cards
    const articleCards = document.querySelectorAll('.article-card');
    articleCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Add floating animation to villager avatar
    const villagerAvatar = document.querySelector('.villager-avatar');
    if (villagerAvatar) {
        villagerAvatar.addEventListener('click', function() {
            this.style.animation = 'none';
            setTimeout(() => {
                this.style.animation = 'bounce 0.6s ease';
            }, 10);
            
            // Show a random fun message
            const funMessages = [
                "🦝 Tom Nook says: 'Thanks for staying informed!'",
                "🐕 Isabelle: 'Great job keeping up with the news!'",
                "🦉 Blathers: 'Knowledge is truly fascinating!'",
                "🎵 K.K. Slider: 'Stay groovy and informed!'",
                "⭐ Celeste: 'The stars shine brighter when you're informed!'"
            ];
            
            const randomMessage = funMessages[Math.floor(Math.random() * funMessages.length)];
            showModal(randomMessage);
        });
    }
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(event) {
        // ESC to close modal
        if (event.key === 'Escape') {
            closeModal();
        }
        
        // Ctrl/Cmd + R for refresh (in addition to normal browser refresh)
        if ((event.ctrlKey || event.metaKey) && event.key === 'r') {
            event.preventDefault();
            refreshFeeds();
        }
        
        // Tab switching with number keys
        if (event.key === '1') {
            switchTab('ai');
        } else if (event.key === '2') {
            switchTab('econ');
        }
    });
    
    // Close modal when clicking outside
    const modal = document.getElementById('messageModal');
    if (modal) {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                closeModal();
            }
        });
    }
    
    // Add some particle effects on page load
    createParticleEffect();
});

// Fun particle effect for page load
function createParticleEffect() {
    const particles = ['🌟', '⭐', '✨', '🌸', '🍃'];
    
    for (let i = 0; i < 8; i++) {
        setTimeout(() => {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: fixed;
                top: -20px;
                left: ${Math.random() * window.innerWidth}px;
                font-size: 20px;
                pointer-events: none;
                z-index: 9999;
                animation: fall 3s ease-out forwards;
            `;
            particle.textContent = particles[Math.floor(Math.random() * particles.length)];
            
            document.body.appendChild(particle);
            
            // Remove particle after animation
            setTimeout(() => {
                particle.remove();
            }, 3000);
        }, i * 200);
    }
}

// Add CSS for falling animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fall {
        to {
            transform: translateY(${window.innerHeight + 100}px) rotate(360deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Console Easter egg
console.log(`
🌟 Welcome to Animal Crossing News Hub! 🌟

🦝 Tom Nook says: "Thanks for checking out the developer console!"
🐕 Isabelle adds: "Here are some fun keyboard shortcuts:"

⌨️  Keyboard Shortcuts:
   • Press '1' to switch to AI news
   • Press '2' to switch to Economics/Politics
   • Press 'Escape' to close modals
   • Click the villager avatar for surprises!

🎮 Built with love, inspired by Animal Crossing! 🏝️
`);
