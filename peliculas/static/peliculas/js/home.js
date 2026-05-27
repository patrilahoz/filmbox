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

            const container = slider.closest(".slider-container");
            const itemWidth = slider.querySelector(".lo-ultimo-item").offsetWidth + 15;
            const totalItems = slider.children.length;
            let currentPosition = 0;

            function getMaxScroll() {
                return -(itemWidth * (totalItems - getVisibleItems()));
            }

            function moveTo(pos) {
                currentPosition = Math.max(getMaxScroll(), Math.min(0, pos));
                slider.style.transition = "transform 0.4s ease";
                slider.style.transform = `translateX(${currentPosition}px)`;
            }

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

            // ── Deslizamiento con panel táctil (trackpad) ──
            let snapTimer = null;

            container.addEventListener("wheel", (e) => {
                // deltaX === 0 → scroll puramente vertical, dejar pasar al navegador
                if (e.deltaX === 0) return;

                // Llamar preventDefault inmediatamente para que el navegador
                // no tome el gesto como navegación o scroll de página
                e.preventDefault();

                // Mover el slider en tiempo real siguiendo el gesto
                const newPos = Math.max(getMaxScroll(), Math.min(0, currentPosition - e.deltaX));
                currentPosition = newPos;
                slider.style.transition = "none";
                slider.style.transform = `translateX(${currentPosition}px)`;

                // Snap al ítem más cercano cuando el gesto se detiene
                clearTimeout(snapTimer);
                snapTimer = setTimeout(() => {
                    const snapIndex = Math.round(-currentPosition / itemWidth);
                    moveTo(-snapIndex * itemWidth);
                }, 150);
            }, { passive: false });
        }

        // Inicializar LO ÚLTIMO
        initSlider("slider", "btn-left", "btn-right");

        // Inicializar TENDENCIAS
        initSlider("tend-slider", "tend-left", "tend-right");

        // Inicializar MEJOR VALORADAS
        initSlider("best-slider", "best-left", "best-right");

    });
