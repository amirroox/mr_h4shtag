document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('vulnChart').getContext('2d');
    const vulnChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Critical', 'High', 'Medium', 'Low'],
            datasets: [{
                label: 'Vulnerabilities',
                data: [0, 0, 0, 0], // Updated dynamically via API in production
                backgroundColor: ['#ff0000', '#ffa500', '#ffff00', '#008000']
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
});