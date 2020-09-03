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

// Create radar chart
function radar_chart(res, start_index, end_index) {
    let radar_chart = document.getElementById('radarChart').getContext('2d');
    let my_radar_chart = new Chart(radar_chart, {
        type: 'radar',
        data: {
            labels: res.csv_data.date_data.slice(start_index, end_index)
                .map(function (item, index) {
                return formatDate(item);
            }),
            datasets: [{
                    label: 'Session Views',
                    data: res.csv_data.session_data.slice(start_index, end_index),
                    backgroundColor: "#33AEEF",
                    borderColor: [
                        'rgba(255, 159, 64, 1)'
                    ],
                },
                {
                    label: 'Page Views',
                    data: res.csv_data.page_data.slice(start_index, end_index),
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

// Create Line Chart
function line_chart(res, start_index, end_index) {
    let line_chart = document.getElementById('lineChart').getContext('2d');
    let my_line_chart = new Chart(line_chart, {
        type: 'line',
        data: {
            labels: res.csv_data.date_data.slice(start_index, end_index).map(function (item, index) {
                return formatDate(item);
            }),
            datasets: [{
                        label: 'Session Views',
                        data: res.csv_data.session_data.slice(start_index, end_index),
                        backgroundColor: "#33AEEF",
                        borderColor: [
                            'rgba(255, 159, 64, 1)'
                        ],
                    },
                    {
                        label: 'Page Views',
                        data: res.csv_data.page_data.slice(start_index, end_index),
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

function call_api(start_index, end_index, total_pages) {
    let document_id = location.pathname.split('/')[3];
    $.ajax({
        url: "http://localhost:8000/accounts/api/" + document_id,
        type: 'GET',
        dataType: 'json',
        success: function(res) {
            // Set number of pages
            total_pages = Math.ceil(res.csv_data.page_data.length / 20);
            console.log('Now total pages ', total_pages);
            // Empty existing pagination contents
            $(".pagination").empty();
            // Pagination
            let append_data = '';
            // Next and previous tabs in pagination would be included if total number of pages exceed 3.
            if(total_pages > 3) {
                append_data += '<li class="page-item"><a class="page-link m-1" value="previous">Previous</a></li>';
            }
            for(let i=1; i<=total_pages; i+=1) {
                append_data += `<li class="page-item"><a class="page-link m-1" value=${i}>${i}</a></li>`
            }
            if(total_pages > 3) {
                append_data += '<li class="page-item"><a class="page-link m-1" value="next">Next</a></li>';
            }
            $('.pagination').append(append_data);
            $('.card-body').empty();
            $('.card-body').append(`<p class="text-primary">Data from indices 
${start_index} to ${end_index} is currently plotted in the charts, you can use pagination for navigation.</p>`)
            // Initialize radar chart
            radar_chart(res, start_index, end_index);
            // Initialize Line Chart
            line_chart(res, start_index, end_index);
        }
    });
}

$(document).ready(function() {
    $('#show_data_btn').click(() => {
        $('#all_data_container').toggle(1000);
    });
    let start_index = 0;
    let end_index = 20;
    let total_pages = 0;
    let current_page = 1;
    // Dynamic Event Call
    $('.pagination').on('click', '.page-item', function() {
        if(event.target.getAttribute('value') != 'next' && event.target.getAttribute('value') != 'previous') {
            current_page = event.target.getAttribute('value');
        }
        if(event.target.getAttribute('value') === 'next') {
            if(current_page > 1 && current_page <= total_pages)
                current_page += 1;
        }
        if(event.target.getAttribute('value') === 'previous') {
            if(current_page > 1 && current_page <= total_pages) {
                current_page -= 1;
            }
            console.log('Current Page : ', current_page, total_pages);
        }
        // Set start and end indices and call the API when page number is changed.
        start_index = (current_page - 1) * 20;
        end_index = start_index + 20;
        console.log('Start and end', start_index, end_index);
        call_api(start_index, end_index, total_pages);
    });
    call_api(start_index, end_index, total_pages);
})

