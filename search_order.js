/**
 * Re-orders search results based on a folder priority:
 * 1. bpc/
 * 2. ipc/
 * 3. bpc_key/
 * 4. ipc_key/
 */
(function() {
    const priority = [
        "bpc/",
        "ipc/",
        "bpc_key/",
        "ipc_key/"
    ];

    let isSorting = false;

    function getPriority(url) {
        for (let i = 0; i < priority.length; i++) {
            if (url.includes(priority[i])) {
                return i;
            }
        }
        return 999;
    }

    function sortResults(list) {
        if (isSorting) return;
        isSorting = true;

        const items = Array.from(list.querySelectorAll(".md-search-result__item"));
        if (items.length <= 1) {
            isSorting = false;
            return;
        }

        const sortedItems = [...items].sort((a, b) => {
            const aUrl = a.querySelector("a")?.getAttribute("href") || "";
            const bUrl = b.querySelector("a")?.getAttribute("href") || "";
            
            const aPrio = getPriority(aUrl);
            const bPrio = getPriority(bUrl);

            if (aPrio !== bPrio) {
                return aPrio - bPrio;
            }
            return 0;
        });

        // Check if order actually changed to avoid unnecessary DOM ops
        let changed = false;
        for (let i = 0; i < items.length; i++) {
            if (items[i] !== sortedItems[i]) {
                changed = true;
                break;
            }
        }

        if (changed) {
            // Append in sorted order
            sortedItems.forEach(item => list.appendChild(item));
        }

        isSorting = false;
    }

    const observer = new MutationObserver((mutations) => {
        if (isSorting) return;
        
        const list = document.querySelector(".md-search-result__list");
        if (list) {
            sortResults(list);
        }
    });

    // Start by looking for the container that will hold the list
    const container = document.querySelector(".md-search-result");
    if (container) {
        observer.observe(container, { childList: true, subtree: true });
    }
})();
