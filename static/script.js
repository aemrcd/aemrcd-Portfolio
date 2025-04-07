// Scroll progress bar and navbar
window.addEventListener('scroll', () => {
    const progressBar = document.querySelector('.progress-bar');
    const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (window.scrollY / scrollHeight) * 100;
    progressBar.style.width = `${scrolled}%`;
    
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Video controls
const video = document.getElementById('scroll-video');
const playPauseBtn = document.getElementById('play-pause-btn');
const playPauseIcon = document.getElementById('play-pause-icon');

playPauseBtn.addEventListener('click', () => {
    video.paused ? video.play() : video.pause();
    playPauseIcon.classList.toggle('bx-play');
    playPauseIcon.classList.toggle('bx-pause');
});

video.addEventListener('ended', () => {
    playPauseIcon.classList.replace('bx-pause', 'bx-play');
});

// Carousel population
document.addEventListener("DOMContentLoaded", () => {
    fetch('/static/cardwheel.json')
        .then(response => response.json())
        .then(works => {
            const container = document.getElementById('product-container');
            works.forEach((work, index) => {
                const item = document.createElement('div');
                item.className = `carousel-item ${index === 0 ? 'active' : ''}`;
                item.innerHTML = `
                    <div class="d-flex justify-content-center">
                        <img src="${work.image}" class="d-block img-fluid" style="max-height: 600px; object-fit: cover;">
                    </div>
                    <div class="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded-3">
                        <p class="mb-0">${work.info}</p>
                    </div>
                `;
                container.appendChild(item);
            });
        })
        .catch(error => {
            console.error('Error loading works:', error);
            document.getElementById('product-container').innerHTML = `
                <div class="carousel-item active">
                    <div class="alert alert-danger">Failed to load portfolio items</div>
                </div>
            `;
        });
});