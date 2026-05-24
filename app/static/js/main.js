document.addEventListener("DOMContentLoaded", () => {
    const btnIncrement = document.getElementById("btn-increment");
    const btnSync = document.getElementById("btn-sync");
    const counterValue = document.getElementById("counter-value");
    const syncIcon = document.querySelector(".sync-icon");
    const statusBadge = document.getElementById("status-badge");
    const counterCard = document.getElementById("counter-card");

    // Helper: Update status badge visual state
    function updateStatus(isOnline) {
        if (!statusBadge) return;
        if (isOnline) {
            statusBadge.className = "status-badge status-online";
            statusBadge.innerHTML = '<span class="pulse-dot"></span> Live';
        } else {
            statusBadge.className = "status-badge status-offline";
            statusBadge.innerHTML = '<span class="pulse-dot"></span> Offline';
        }
    }

    // Helper: Render error banner dynamically
    function showError(message) {
        let errorBanner = document.getElementById("error-banner");
        if (!errorBanner) {
            errorBanner = document.createElement("div");
            errorBanner.id = "error-banner";
            errorBanner.className = "error-banner";
            
            // Insert inside card body
            const cardBody = document.querySelector(".card-body");
            cardBody.appendChild(errorBanner);
        }
        
        errorBanner.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="error-icon">
                <circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/>
            </svg>
            <span>${message}</span>
        `;
        updateStatus(false);
    }

    // Helper: Hide error banner
    function removeError() {
        const errorBanner = document.getElementById("error-banner");
        if (errorBanner) {
            errorBanner.remove();
        }
        updateStatus(true);
    }

    // Helper: Animate the counter value change
    function animateCounter() {
        counterValue.classList.remove("pulse-up");
        // Trigger reflow to restart CSS animation
        void counterValue.offsetWidth;
        counterValue.classList.add("pulse-up");
    }

    // Task: API Call to increment count
    async function incrementCount() {
        btnIncrement.disabled = true;
        try {
            const response = await fetch("/api/increment", {
                method: "POST",
                headers: { "Content-Type": "application/json" }
            });
            const data = await response.json();
            
            if (response.ok && data.status === "success") {
                counterValue.textContent = data.count;
                animateCounter();
                removeError();
            } else {
                showError(data.message || "Failed to register visit.");
            }
        } catch (error) {
            console.error("Connection error:", error);
            showError("Network offline. Redis backend unreachable.");
        } finally {
            btnIncrement.disabled = false;
        }
    }

    // Task: API Call to sync count
    async function syncCount() {
        btnSync.disabled = true;
        if (syncIcon) syncIcon.classList.add("spin");

        try {
            const response = await fetch("/api/count");
            const data = await response.json();
            
            if (response.ok && data.status === "success") {
                counterValue.textContent = data.count;
                animateCounter();
                removeError();
            } else {
                showError(data.message || "Sync failed.");
            }
        } catch (error) {
            console.error("Connection error:", error);
            showError("Network offline. Redis backend unreachable.");
        } finally {
            setTimeout(() => {
                btnSync.disabled = false;
                if (syncIcon) syncIcon.classList.remove("spin");
            }, 600); // match animation duration
        }
    }

    // Event listeners
    if (btnIncrement) btnIncrement.addEventListener("click", incrementCount);
    if (btnSync) btnSync.addEventListener("click", syncCount);
});
