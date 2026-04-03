// Swap -b/-d image variants when MkDocs Material theme changes.
(function () {
    function applyTheme(scheme) {
        var dark = scheme === 'slate';
        document.querySelectorAll('img[src]').forEach(function (img) {
            var src = img.getAttribute('src');
            if (!src) return;
            if (dark && src.endsWith('-b.png')) {
                img.setAttribute('src', src.slice(0, -6) + '-d.png');
            } else if (!dark && src.endsWith('-d.png')) {
                img.setAttribute('src', src.slice(0, -6) + '-b.png');
            }
        });
    }

    function getCurrentScheme() {
        return document.body.getAttribute('data-md-color-scheme') || 'default';
    }

    document.addEventListener('DOMContentLoaded', function () {
        applyTheme(getCurrentScheme());
    });

    var observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (m) {
            if (m.attributeName === 'data-md-color-scheme') {
                applyTheme(getCurrentScheme());
            }
        });
    });
    observer.observe(document.body, { attributes: true, attributeFilter: ['data-md-color-scheme'] });
})();
