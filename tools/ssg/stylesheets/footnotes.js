document.addEventListener("DOMContentLoaded", function() {
    const footnoteRefs = document.querySelectorAll("sup.manual-fn-ref");
    const defs = {};
    document.querySelectorAll("div.manual-fn-def").forEach(def => {
        defs[def.getAttribute("data-fn")] = def;
    });

    footnoteRefs.forEach(ref => {
        const fnId = ref.getAttribute("data-fn");
        const fnContentLi = defs[fnId];
        
        if (fnContentLi) {
            const tooltip = document.createElement("div");
            tooltip.className = "footnote-tooltip";
            
            const visibleNumber = fnId;
            
            const contentClone = fnContentLi.cloneNode(true);
            
            tooltip.innerHTML = `<b>${visibleNumber}.</b> ` + contentClone.innerHTML;
            
            const wrapper = document.createElement("span");
            wrapper.className = "footnote-wrapper";
            ref.parentNode.insertBefore(wrapper, ref);
            wrapper.appendChild(ref);
            wrapper.appendChild(tooltip);
        }
    });

    // Fix for broken ordered lists (interrupted by HR, tables or other blocks)
    document.querySelectorAll(".manual-list-start").forEach(marker => {
        const startVal = marker.getAttribute("data-start");
        // The NEXT sibling (or next next if there's text) should be the <ol>
        let next = marker.nextElementSibling;
        while (next && next.tagName !== "OL" && next.classList.contains("manual-list-start") === false) {
            if (next.tagName === "OL") break;
            next = next.nextElementSibling;
        }
        
        if (next && next.tagName === "OL") {
            next.setAttribute("start", startVal);
        }
    });

    // Hide empty table headers
    document.querySelectorAll("thead").forEach(thead => {
        let isEmpty = true;
        thead.querySelectorAll("th").forEach(th => {
            if (th.textContent.trim() !== "") {
                isEmpty = false;
            }
        });
        if (isEmpty) {
            thead.style.display = "none";
        }
    });
});
