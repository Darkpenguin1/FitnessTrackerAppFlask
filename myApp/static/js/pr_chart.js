document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('prChart').getContext('2d'); 
    const dropdown = document.getElementById('exercise-select');
    // Fetch exercise data
    fetch('/api/exercises/')
        .then(function(response) {
            if (response.ok) {
                return response.json(); // Parse JSON data
            }
            throw new Error('Failed to fetch exercise data');
        })
        .then(function(data) {
            console.log(data); // Log data for debugging purposes
            populateDropdown(data); // Populate dropdown with exercise names
        })
        .catch(function(error) {
            console.error('Error fetching data:', error);
        });

    function populateDropdown(exercises) {
        exercises.forEach(function(exercise) {
            const option = document.createElement('option');
            option.value = exercise; // Set value to exercise name
            option.textContent = exercise; // Display name in the dropdown
            dropdown.appendChild(option); // Add the option to the dropdown
        });
    }

        // Event listener for dropdown change
    dropdown.addEventListener('change', function() {
        const selectedExercise = dropdown.value;
        if (selectedExercise) {
            fetch(`/api/getPRS/`) 
                .then(function(response) {
                    if (response.ok) {
                        return response.json();
                    }
                    throw new Error('Failed to fetch PR data');
                })
                .then(function(prData) {
                    console.log(prData);
                    const prDataForSelectedExercise = prData[selectedExercise] || [];
                    createChart(prDataForSelectedExercise, 'line'); // Update the chart with PR data
                })
                .catch(function(error) {
                    console.error('Error fetching PR data:', error);
                });
        }
    });

    function createChart(data, type) {
        // Clear existing chart if necessary
        if (window.myChart) {
            window.myChart.destroy();
        }
        
        window.myChart = new Chart(ctx, {
            type: type, // Dynamic chart type
            data: {
                labels: data.map(row => row.date), // Use dates for labels
                datasets: [{
                    label: 'PR Progression',
                    data: data.map(row => row.weight), // Use weights for data
                    borderWidth: 1,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    fill: false
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
});
