document.addEventListener('DOMContentLoaded', function() {
    const unitSelect = document.getElementById('unit');     // init the vars of the things on the html page we want to change
    const weightInput = document.getElementById('weight');

    unitSelect.addEventListener('change', function() {      // if the unit select is changed then we change our place holder accordingly
        const unit = this.value;
        if (unit === 'kg') {
            weightInput.placeholder = 'Weight (KG)';
        }
        else if (unit === 'lb') {
            weightInput.placeholder = 'Weight (lb)';
        }
    });
    unitSelect.dispatchEvent(new Event('change'))

});

