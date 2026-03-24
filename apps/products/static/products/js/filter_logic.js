document.addEventListener('change', function(e) {
    if (e.target.classList.contains('form-check-input')) {
        const url = new URL(window.location.href);
        const params = new URLSearchParams(url.search);

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

        const finalUrl = `${url.pathname}?${params.toString()}`;

        fetch(finalUrl, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(response => response.text())
        .then(html => {
            document.getElementById('ajax-product-section').innerHTML = html;
            window.history.pushState({}, '', finalUrl);
        });
    }
});