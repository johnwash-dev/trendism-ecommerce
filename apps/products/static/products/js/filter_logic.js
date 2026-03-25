function fetchFilteredProducts() {
    const url = new URL(window.location.href);
    const params = new URLSearchParams(url.search);

    const spinner = document.getElementById('loading-spinner');
    const section = document.getElementById('ajax-product-section');

    if (spinner) spinner.classList.remove('d-none');
    if (section) section.classList.add('loading-active');

    ['brand', 'color', 'category'].forEach(group => {
        const checked = Array.from(document.querySelectorAll(`input[name="${group}"]:checked`))
            .map(el => el.value);
        if (checked.length > 0) params.set(group, checked.join(','));
        else if (group !== 'category') params.delete(group);
    });

    const price = document.querySelector('input[name="price"]:checked');
    if (price) params.set('price', price.value);

    const discount = document.querySelector('input[name="discount"]:checked');
    if (discount) params.set('min_discount', discount.value);

    const sort = document.querySelector('input[name="sort"]:checked');
    if (sort) {
        params.set('sort', sort.value);
        const desktopBtn = document.getElementById('desktopSortBtn');
        if (desktopBtn) {
            const label = sort.closest('label');
            const labelText = label.querySelector('span') ? label.querySelector('span').innerText : label.innerText.trim();
            desktopBtn.innerText = `SORT BY: ${labelText}`;
        } else {
            params.set('sort', 'newest')
            if (desktopBtn) desktopBtn.innerText = `SORT BY: Newest`;
        }
    }

    const finalUrl = `${url.pathname}?${params.toString()}`;

    fetch(finalUrl, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
        .then(response => response.text())
        .then(html => {
            document.getElementById('ajax-product-section').innerHTML = html;

            const newCount = document.getElementById('current-count-hidden')?.value
            const countDisplay = document.getElementById('product-count')

            if (countDisplay && newCount !== undefined) {
                countDisplay.innerText = newCount + " Items Found"
            }

            window.history.pushState({}, '', finalUrl);

            const sortCanvas = document.getElementById('sortCanvas');
            if (sortCanvas && e.target.name === 'sort') {
                const bsOffcanvas = bootstrap.Offcanvas.getInstance(sortCanvas);
                if (bsOffcanvas) bsOffcanvas.hide();
            }
        })
        .finally(() => {
            if (spinner) spinner.classList.add('d-none');
            if (section) section.classList.remove('loading-active');
        });

}

document.addEventListener('change', function (e) {
    if (e.target.classList.contains('form-check-input') || e.target.name === 'sort') {
        fetchFilteredProducts()
    }
});

document.addEventListener('click', function (e) {
    if (e.target.id === 'clear-all-btn') {
        e.preventDefault();

        document.querySelectorAll('.form-check-input').forEach(input => {
            if (input.name !== 'category') {
                input.checked = false;
            }
        });

        const defaultSort = document.querySelector('input[name="sort"][value="newest"]');
        if (defaultSort) defaultSort.checked = true;

        fetchFilteredProducts();
    }
});