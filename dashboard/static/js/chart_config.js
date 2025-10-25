// Chart.js configuration for AQI dashboard
// This file contains reusable chart configurations

// Default chart options
const defaultChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
        },
        tooltip: {
            mode: 'index',
            intersect: false
        },
        title: {
            display: false
        }
    },
    scales: {
        x: {
            display: true,
            title: {
                display: true,
                text: 'Time'
            }
        },
        y: {
            display: true,
            title: {
                display: true,
                text: 'AQI Value'
            },
            beginAtZero: true
        }
    },
    interaction: {
        mode: 'nearest',
        axis: 'x',
        intersect: false
    }
};

// Function to create AQI comparison chart
function createAQIComparisonChart(ctx, data) {
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels || [],
            datasets: [
                {
                    label: 'Linear Regression',
                    data: data.lrData || [],
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.1)',
                    tension: 0.4,
                    fill: false,
                    pointRadius: 4,
                    pointHoverRadius: 6
                },
                {
                    label: 'Decision Tree',
                    data: data.dtData || [],
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    tension: 0.4,
                    fill: false,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }
            ]
        },
        options: defaultChartOptions
    });
}

// Function to update chart with new data
function updateChart(chart, newData) {
    chart.data.labels = newData.labels;
    chart.data.datasets[0].data = newData.lrData;
    chart.data.datasets[1].data = newData.dtData;
    chart.update();
}

// Function to create AQI distribution chart
function createAQIDistributionChart(ctx, categories) {
    const categoryNames = Object.keys(categories);
    const categoryCounts = Object.values(categories);
    
    return new Chart(ctx, {
        type: 'bar',
        data: {
            labels: categoryNames,
            datasets: [{
                label: 'Prediction Count',
                data: categoryCounts,
                backgroundColor: [
                    'rgba(0, 228, 0, 0.7)', // Good
                    'rgba(255, 255, 0, 0.7)', // Moderate
                    'rgba(255, 126, 0, 0.7)', // Unhealthy for Sensitive
                    'rgba(255, 0, 0, 0.7)', // Unhealthy
                    'rgba(143, 63, 151, 0.7)', // Very Unhealthy
                    'rgba(126, 0, 35, 0.7)' // Hazardous
                ],
                borderColor: [
                    'rgba(0, 228, 0, 1)',
                    'rgba(255, 255, 0, 1)',
                    'rgba(255, 126, 0, 1)',
                    'rgba(255, 0, 0, 1)',
                    'rgba(143, 63, 151, 1)',
                    'rgba(126, 0, 35, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'AQI Category Distribution'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Count'
                    }
                }
            }
        }
    });
}

// Function to format AQI value with category
function formatAQIWithCategory(aqiValue) {
    let category = '';
    let color = '';
    
    if (aqiValue >= 0 && aqiValue <= 50) {
        category = 'Good';
        color = '#00e400';
    } else if (aqiValue > 50 && aqiValue <= 100) {
        category = 'Moderate';
        color = '#ffff00';
    } else if (aqiValue > 100 && aqiValue <= 150) {
        category = 'Unhealthy for Sensitive Groups';
        color = '#ff7e00';
    } else if (aqiValue > 150 && aqiValue <= 200) {
        category = 'Unhealthy';
        color = '#ff0000';
    } else if (aqiValue > 200 && aqiValue <= 300) {
        category = 'Very Unhealthy';
        color = '#8f3f97';
    } else {
        category = 'Hazardous';
        color = '#7e0023';
    }
    
    return {
        value: aqiValue.toFixed(1),
        category: category,
        color: color
    };
}

// Utility function to generate time labels for charts
function generateTimeLabels(count, interval = 'hour') {
    const labels = [];
    const now = new Date();
    
    for (let i = count - 1; i >= 0; i--) {
        const date = new Date(now);
        
        if (interval === 'hour') {
            date.setHours(now.getHours() - i);
            labels.push(date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
        } else if (interval === 'day') {
            date.setDate(now.getDate() - i);
            labels.push(date.toLocaleDateString([], { month: 'short', day: 'numeric' }));
        }
    }
    
    return labels;
}

// Export functions for use in other scripts (if using modules)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        defaultChartOptions,
        createAQIComparisonChart,
        updateChart,
        createAQIDistributionChart,
        formatAQIWithCategory,
        generateTimeLabels
    };
}