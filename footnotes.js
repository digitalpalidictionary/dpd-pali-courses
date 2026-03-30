/**
 * Client-side script to handle footnote tooltips, ordered list numbering fixes,
 * and hiding empty table headers on the DPD Pāḷi Courses website.
 */
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
            tooltip.className = "footnote-tooltip md-typeset";
            
            const visibleNumber = fnId;
            const contentClone = fnContentLi.cloneNode(true);
            
            tooltip.innerHTML = `<b>${visibleNumber}.</b> ` + contentClone.innerHTML;
            
            const wrapper = document.createElement("span");
            wrapper.className = "footnote-wrapper";
            ref.parentNode.insertBefore(wrapper, ref);
            wrapper.appendChild(ref);

            let hideTimeout;

            const showTooltip = function() {
                clearTimeout(hideTimeout);
                if (tooltip.parentNode !== document.body) {
                    document.body.appendChild(tooltip);
                }
                
                // Get position of the wrapper
                const rect = wrapper.getBoundingClientRect();
                
                // Temporarily display to calculate dimensions
                tooltip.style.visibility = "hidden";
                tooltip.style.display = "block";
                
                const tooltipRect = tooltip.getBoundingClientRect();
                
                // Center horizontally relative to the wrapper
                let leftPos = rect.left + window.scrollX + (rect.width / 2);
                tooltip.style.left = leftPos + "px";
                
                // Default: above the wrapper
                let topPos = rect.top + window.scrollY - tooltipRect.height - 10;
                
                // If it goes off the top of the screen, place it below
                if (topPos < window.scrollY) {
                    topPos = rect.bottom + window.scrollY + 10;
                    tooltip.classList.add("tooltip-bottom");
                } else {
                    tooltip.classList.remove("tooltip-bottom");
                }
                
                tooltip.style.top = topPos + "px";
                tooltip.style.visibility = "visible";
            };

            const hideTooltip = function() {
                hideTimeout = setTimeout(() => {
                    if (tooltip.parentNode === document.body) {
                        document.body.removeChild(tooltip);
                    }
                }, 200); // Small delay to allow moving mouse to tooltip
            };

            wrapper.addEventListener("mouseenter", showTooltip);
            wrapper.addEventListener("mouseleave", hideTooltip);
            tooltip.addEventListener("mouseenter", showTooltip); // Keep open if hovering over tooltip
            tooltip.addEventListener("mouseleave", hideTooltip);
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

    // Make site title in header a link to the homepage
    const logoLink = document.querySelector("a.md-header__button.md-logo");
    const titleEllipsis = document.querySelector(".md-header__title .md-ellipsis");
    if (titleEllipsis && logoLink) {
        const link = document.createElement("a");
        link.href = logoLink.href;
        link.style.cssText = "color:inherit;text-decoration:none;cursor:pointer;";
        titleEllipsis.parentNode.replaceChild(link, titleEllipsis);
        link.appendChild(titleEllipsis);
    }
});
