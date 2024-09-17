window.addEventListener('scroll', function() {
    const videoContainer = document.querySelector('.video-container');
    const targetWidthPx = 1280;
    const targetHeightPx = 660;
    const viewportWidth = window.innerWidth;
    const mobileBreakpoint = 768;

    if (viewportWidth <= mobileBreakpoint) {
        return;
    }

    const scrollY = window.scrollY;
    const maxScroll = 600;
    const scaleFactor = Math.max(0, Math.min(1, scrollY / maxScroll));

    const initialWidthPx = window.innerWidth;
    const initialHeightPx = window.innerHeight;
    const newWidthPx = initialWidthPx - ((initialWidthPx - targetWidthPx) * scaleFactor);
    const newHeightPx = initialHeightPx - ((initialHeightPx - targetHeightPx) * scaleFactor);

    videoContainer.style.width = `${newWidthPx}px`;
    videoContainer.style.height = `${newHeightPx}px`;

    videoContainer.style.position = 'absolute';
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;

    videoContainer.style.left = `${(windowWidth - newWidthPx) / 2}px`;
    videoContainer.style.top = `${(windowHeight - newHeightPx) / 2}px`;
});

const video = document.getElementById('scroll-video');
const playPauseBtn = document.getElementById('play-pause-btn');
const playPauseIcon = document.getElementById('play-pause-icon');

playPauseBtn.addEventListener('click', function() {
    if (video.paused) {
        video.play();
        playPauseIcon.classList.remove('bx-play');
        playPauseIcon.classList.add('bx-pause');
    } else {
        video.pause();
        playPauseIcon.classList.remove('bx-pause');
        playPauseIcon.classList.add('bx-play');
    }
});

video.addEventListener('ended', function() {
    playPauseIcon.classList.remove('bx-pause');
    playPauseIcon.classList.add('bx-play');
});

document.addEventListener("DOMContentLoaded", function() {
    const productContainer = document.getElementById('product-container');
    const scrollRightButton = document.getElementById('scroll-right');
    const scrollLeftButton = document.getElementById('scroll-left');

    fetch('cardwheel.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(products => {
            products.forEach(product => {
                const productCard = document.createElement('div');
                productCard.classList.add('product-card');

                let infoBox = '';
                if (product.info && product.showInfo) {
                    infoBox = `
                        <div class="info-box">
                            <p>${product.info}</p>
                        </div>
                        <button class="plus-button">+</button>
                    `;
                }

                productCard.innerHTML = `
                    <img src="${product.image}" alt="Product Image">
                    ${infoBox}
                `;

                productContainer.appendChild(productCard);

                const plusButton = productCard.querySelector('.plus-button');
                if (plusButton) {
                    plusButton.addEventListener('click', () => {
                        const infoBox = productCard.querySelector('.info-box');
                        if (infoBox.style.display === 'none' || infoBox.style.display === '') {
                            infoBox.style.display = 'block';
                        } else {
                            infoBox.style.display = 'none';
                        }
                    });
                }
            });
        })
        .catch(error => console.error('Error fetching the products:', error));

    scrollRightButton.addEventListener('click', () => {
        productContainer.scrollBy({
            left: 300,
            behavior: 'smooth'
        });
    });

    scrollLeftButton.addEventListener('click', () => {
        productContainer.scrollBy({
            left: -300,
            behavior: 'smooth'
        });
    });
});
