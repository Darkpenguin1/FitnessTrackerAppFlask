document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form'); // Select all forms on the page

    forms.forEach(form => {
        const unitSelect = form.querySelector('#unit'); // Select unit dropdown within the form
        const weightInput = form.querySelector('#weight'); // Select weight input within the form

        if (unitSelect && weightInput) {
            unitSelect.addEventListener('change', function() { // Add event listener to unit dropdown
                const unit = this.value;
                if (unit === 'kg') {
                    weightInput.placeholder = 'Weight (KG)';
                } else if (unit === 'lb') {
                    weightInput.placeholder = 'Weight (lb)';
                }
            });

            // Trigger change event on page load to set initial placeholder
            unitSelect.dispatchEvent(new Event('change'));
        }
    });
});
