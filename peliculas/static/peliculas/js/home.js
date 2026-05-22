// SECCIÓN LO ÚLTIMO - FUNCIONALIDAD DE CARRUSEL

    document.addEventListener("DOMContentLoaded", () => {

        function getVisibleItems() {
            if (window.innerWidth <= 480) return 2;
            if (window.innerWidth <= 768) return 3;
            if (window.innerWidth <= 1024) return 4;
            return 6;
        }

        function initSlider(sliderId, leftBtnId, rightBtnId) {
            const slider = document.getElementById(sliderId);
            const btnLeft = document.getElementById(leftBtnId);
            const btnRight = document.getElementById(rightBtnId);

            if (!slider) return;

            const itemWidth = slider.querySelector(".lo-ultimo-item").offsetWidth + 15;
            const totalItems = slider.children.length;
            let currentPosition = 0;

            btnRight.addEventListener("click", () => {
                const visibleItems = getVisibleItems();
                if (currentPosition > -(itemWidth * (totalItems - visibleItems))) {
                    currentPosition -= itemWidth;
                    slider.style.transform = `translateX(${currentPosition}px)`;
                }
            });

            btnLeft.addEventListener("click", () => {
                if (currentPosition < 0) {
                    currentPosition += itemWidth;
                    slider.style.transform = `translateX(${currentPosition}px)`;
                }
            });
        }

        // Inicializar LO ÚLTIMO
        initSlider("slider", "btn-left", "btn-right");

        // Inicializar TENDENCIAS
        initSlider("tend-slider", "tend-left", "tend-right");

        // Inicializar MEJOR VALORADAS
        initSlider("best-slider", "best-left", "best-right");

    });