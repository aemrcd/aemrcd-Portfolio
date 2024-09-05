// A DISPLAY SCROLLING FUNCTION THAT LET THE VIDEO REDUCE THE RESOLUTION WHILE SCROLLING
window.addEventListener('scroll', function() {
    // Select the video container
    const videoContainer = document.querySelector('.video-container');

    // Define the target dimensions in pixels
    const targetWidthPx = 1280;
    const targetHeightPx = 660;

    // Get the current scroll position
    const scrollY = window.scrollY;

    // Define the maximum scroll value where the animation should complete
    const maxScroll = 600; // Adjust this value to control the scroll length for the animation

    // Calculate the current width and height based on the scroll position
    const scaleFactor = Math.max(0, Math.min(1, scrollY / maxScroll)); // Clamps the value between 0 and 1
    const initialWidthPx = window.innerWidth;
    const initialHeightPx = window.innerHeight;

    const newWidthPx = initialWidthPx - ((initialWidthPx - targetWidthPx) * scaleFactor);
    const newHeightPx = initialHeightPx - ((initialHeightPx - targetHeightPx) * scaleFactor);

    // Apply the new width and height to the video container
    videoContainer.style.width = `${newWidthPx}px`;
    videoContainer.style.height = `${newHeightPx}px`;

    // Center the video container by setting left and top positions
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;

    videoContainer.style.left = `${(windowWidth - newWidthPx) / 2}px`;
    videoContainer.style.top = `${(windowHeight - newHeightPx) / 2}px`;
});

window.addEventListener('scroll', function() {
    // Select the video element
    const video = document.getElementById('scroll-video');
    
    // Ensure the video element exists
    if (!video) return;

    // Calculate the scroll position and the document height
    const scrollPosition = window.scrollY;
    const documentHeight = document.documentElement.scrollHeight;
    const viewportHeight = window.innerHeight;
    
    // Calculate 90% of the document height (corrected the multiplier)
    const top = documentHeight * 0.7 - viewportHeight;

    // Check if the scroll position is below 90% of the document height
    if (scrollPosition >= top) {
        // Play the video if scrolling past the 90% mark
        if (video.paused) {
            video.play();
        }
    } else {
        // Pause the video if scrolling above the 90% mark
        if (!video.paused) {
            video.pause();
        }
    }
});

// CARD WHEEL 
document.addEventListener("DOMContentLoaded", function() {
    const productContainer = document.getElementById('product-container');
    const scrollRightButton = document.getElementById('scroll-right');
    const scrollLeftButton = document.getElementById('scroll-left');

    // Fetch data from the JSON file
    fetch('cardwheel.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(products => {
            products.forEach(product => {
                // Create a product card
                const productCard = document.createElement('div');
                productCard.classList.add('product-card');

                // Create the info box and plus button if info is available
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

                // Append the product card to the container
                productContainer.appendChild(productCard);

                // Add event listener to the plus button
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

    // Scroll to the right when button is clicked
    scrollRightButton.addEventListener('click', () => {
        productContainer.scrollBy({
            left: 300, // Adjust this value to control scroll amount
            behavior: 'smooth'
        });
    });

    // Scroll to the left when button is clicked
    scrollLeftButton.addEventListener('click', () => {
        productContainer.scrollBy({
            left: -300, // Use negative value to scroll left
            behavior: 'smooth'
        });
    });
});
