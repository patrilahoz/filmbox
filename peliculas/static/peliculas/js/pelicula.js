//  FUNCIONALIDAD DE ESTRELLAS DE PUNTUACIÓN

    (function () {
        const stars = Array.from(document.querySelectorAll('.rating-star'));
        const ratingInput = document.getElementById('ratingInput');
        const starsContainer = document.getElementById('starsContainer');
        if (!starsContainer) return;
        let selected = 0;

        function fill(upto) {
            stars.forEach((s, i) => {
                const icon = s.querySelector('i');
                if (i < upto) {
                    icon.classList.remove('bi-star');
                    icon.classList.add('bi-star-fill');
                } else {
                    icon.classList.add('bi-star');
                    icon.classList.remove('bi-star-fill');
                }
            });
        }

        stars.forEach((s, idx) => {
            s.addEventListener('mouseover', () => fill(idx + 1));
            s.addEventListener('click', () => {
                selected = idx + 1;
                ratingInput.value = selected;
                fill(selected);
            });
        });

        starsContainer.addEventListener('mouseleave', () => fill(selected));
    })();


    // FUNCIONALIDAD DE LIKES EN RESEÑAS

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const heart = this.querySelector('i');
            const likeNumber = this.querySelector('.like-number');
            const url = this.dataset.url;

            fetch(url, {
                method: 'POST',
                headers: { 'X-CSRFToken': csrfToken },
            })
            .then(res => res.json())
            .then(data => {
                heart.classList.toggle('bi-heart', !data.liked);
                heart.classList.toggle('bi-heart-fill', data.liked);
                likeNumber.textContent = data.count;
            });
        });
    });


    // MODAL DE ÉXITO AL GUARDAR RESEÑA

    const reviewForm = document.getElementById('reviewForm');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const puntuacion = document.getElementById('ratingInput').value;
            const resenaTexto = reviewForm.querySelector('textarea[name="reseña"]').value.trim();

            if (!puntuacion && !resenaTexto) {
                Swal.fire({
                    title: "Debes puntuar o reseñar la película para poder guardar",
                    icon: "warning",
                    iconColor: "#6E32D5",                    
                    confirmButtonText: "Aceptar",
                    showClass: {
                        popup: `animate__animated animate__fadeInUp animate__faster`
                    },
                    hideClass: {
                        popup: `animate__animated animate__fadeOutDown animate__faster`
                    },
                    customClass: {
                        title: 'swal-title',
                        confirmButton: 'swal-confirm'
                    }
                });
                return;
            }

            Swal.fire({
                title: "Película puntuada y reseñada correctamente",
                icon: "success",
                confirmButtonText: "Aceptar",
                customClass: {
                    title: 'swal-title',
                    confirmButton: 'swal-confirm',
                    icon: 'swal-icon'
                }
            }).then(() => {
                reviewForm.submit();
            });
        });
    }


    // BARRAS DE PUNTUACIONES

    document.querySelectorAll('.chart-bar[data-pct]').forEach(bar => {
        bar.style.width = bar.dataset.pct + '%';
    });

    // MODAL DE ELIMINAR RESEÑA

    document.querySelectorAll('.delete-review-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.getAttribute('href');

            Swal.fire({
                title: "¿Estás segur@ de que quieres eliminar la reseña?",
                text: "No podrás revertir esto",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#6E32D5",
                cancelButtonColor: "#d33333",
                cancelButtonText: "Cancelar",
                confirmButtonText: "Eliminar reseña",
                iconColor: "#6E32D5"
            }).then((result) => {
                if (result.isConfirmed) {
                    Swal.fire({
                        title: "Reseña eliminada correctamente",
                        icon: "success",
                        iconColor: "#6E32D5",
                        confirmButtonText: "Aceptar",
                        customClass: {
                            title: 'swal-title',
                            confirmButton: 'swal-confirm',
                            icon: 'swal-icon'
                        }
                    }).then(() => {
                        if (url) {
                            window.location.href = url;
                        }
                    });
                }
            });
        });
    });

    
    // MODAL DE ELIMINAR PELÍCULA

    document.querySelectorAll('.eliminar-pelicula-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const url = this.getAttribute('href');

            Swal.fire({
                title: "¿Estás segur@ de que quieres eliminar la película?",
                text: "No podrás revertir esto",
                icon: "warning",
                showCancelButton: true,
                confirmButtonColor: "#6E32D5",
                cancelButtonColor: "#d33333",
                cancelButtonText: "Cancelar",
                confirmButtonText: "Eliminar película",
                iconColor: "#6E32D5"
            }).then((result) => {
                if (result.isConfirmed) {
                    Swal.fire({
                        title: "Película eliminada correctamente",
                        icon: "success",
                        confirmButtonText: "Aceptar",
                        customClass: {
                            title: 'swal-title',
                            confirmButton: 'swal-confirm',
                            icon: 'swal-icon'
                        }
                    }).then(() => {
                        if (url) {
                            window.location.href = url;
                        }
                    });
                }
            });
        });
    });