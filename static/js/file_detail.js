// Date Formatter
function formatDate(date) {
    let d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [year, month, day].join('-');
}

$(document).ready(function() {
    console.log('File detail loaded');
    let document_id = location.pathname.split('/')[3];
        $.ajax({
        url: "http://localhost:8000/accounts/api/" + document_id,
        type: 'GET',
        dataType: 'json', // added data type
        success: function(res) {
            // Initialize radar chart
            let radar_chart = document.getElementById('radarChart').getContext('2d');
            let my_radar_chart = new Chart(radar_chart, {
                type: 'radar',
                data: {
                    labels: res.csv_data.date_data.map(function (item, index) {
                        return formatDate(item);
                    }),
                    datasets: [{
                            label: 'Session Views',
                            data: res.csv_data.session_data,
                            backgroundColor: "#33AEEF",
                            borderColor: [
                                'rgba(255, 159, 64, 1)'
                            ],
                        },
                        {
                            label: 'Page Views',
                            data: res.csv_data.page_data,
                            backgroundColor: "#D5496D",
                            borderColor: [
                                'rgba(75, 192, 192, 1)',
                            ],
                        }
                    ]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
            // Initialize Line Chart
            let line_chart = document.getElementById('lineChart').getContext('2d');
            let my_line_chart = new Chart(line_chart, {
                type: 'line',
                data: {
                    labels: res.csv_data.date_data.map(function (item, index) {
                        return formatDate(item);
                    }),
                    datasets: [{
                        label: 'Session Views',
                        data: res.csv_data.session_data,
                        backgroundColor: "#33AEEF",
                        borderColor: [
                            'rgba(255, 159, 64, 1)'
                        ],
                        },
                        {
                            label: 'Page Views',
                        data: res.csv_data.page_data,
                        backgroundColor: "#D5496D",
                        borderColor: [
                            'rgba(75, 192, 192, 1)',
                        ],
                        }
                    ]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
        }
    });
})

