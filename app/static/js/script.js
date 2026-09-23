document.addEventListener("DOMContentLoaded", () => {

    const categoryButtons =
        document.querySelectorAll(".category-btn");

    const wallpaperCards =
        document.querySelectorAll(".wallpaper-card");

    const searchInput =
        document.getElementById("searchInput");

    const noResults =
        document.getElementById("noResults");

    let selectedCategory = "All";


    function filterWallpapers() {

        const searchText =
            searchInput.value.trim().toLowerCase();

        let visibleCount = 0;


        wallpaperCards.forEach((card) => {

            const category =
                card.dataset.category.toLowerCase();

            const title =
                card.dataset.title.toLowerCase();


            const categoryMatch =
                selectedCategory === "All" ||
                category === selectedCategory.toLowerCase();


            const searchMatch =
                title.includes(searchText) ||
                category.includes(searchText);


            if (categoryMatch && searchMatch) {

                card.style.display = "";

                visibleCount++;

            } else {

                card.style.display = "none";

            }

        });


        if (visibleCount === 0) {

            noResults.classList.add("show");

        } else {

            noResults.classList.remove("show");

        }

    }


    categoryButtons.forEach((button) => {

        button.addEventListener("click", () => {

            categoryButtons.forEach((btn) => {
                btn.classList.remove("active");
            });


            button.classList.add("active");


            selectedCategory =
                button.dataset.category;


            filterWallpapers();

        });

    });


    searchInput.addEventListener(
        "input",
        filterWallpapers
    );


    document
        .querySelectorAll('a[href^="#"]')
        .forEach((link) => {

            link.addEventListener("click", (event) => {

                const targetId =
                    link.getAttribute("href");

                const target =
                    document.querySelector(targetId);


                if (target) {

                    event.preventDefault();

                    target.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

                }

            });

        });


    document
        .querySelectorAll(".download-button")
        .forEach((button) => {

            button.addEventListener("click", () => {

                const originalText =
                    button.innerHTML;


                button.innerHTML =
                    "<span>✓</span> Downloading...";


                setTimeout(() => {

                    button.innerHTML =
                        originalText;

                }, 1800);

            });

        });


    filterWallpapers();

});