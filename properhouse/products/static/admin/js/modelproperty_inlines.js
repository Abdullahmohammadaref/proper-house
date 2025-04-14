document.addEventListener('DOMContentLoaded', function() {
    function toggleInlines() {
        const propertySelect = document.querySelector('#id_property');
        if (!propertySelect) return;

        const selectedOption = propertySelect.options[propertySelect.selectedIndex];
        const dataType = selectedOption.dataset.type;

        // Hide all inlines
        document.querySelectorAll('.inline-related').forEach(el => {
            el.style.display = 'none';
        });

        // Show only relevant inline
        if (dataType) {
            const targetInline = document.querySelector(`.inline-related[data-type="${dataType}"]`);
            if (targetInline) {
                targetInline.style.display = 'block';
            }
        }
    }

    // Initial toggle
    toggleInlines();

    // Add event listener for property changes
    document.querySelector('#id_property').addEventListener('change', toggleInlines);
});