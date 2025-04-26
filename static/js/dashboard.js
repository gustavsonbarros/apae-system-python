// Função para inicializar os gráficos
function initCharts(ativos, inativos, suspensos, areasData) {
    // Gráfico de Situação
    const situacaoCanvas = document.getElementById('situacaoChart');
    if (situacaoCanvas) {
        const situacaoCtx = situacaoCanvas.getContext('2d');
        new Chart(situacaoCtx, {
            type: 'doughnut',
            data: {
                labels: ['Ativos', 'Inativos', 'Suspensos'],
                datasets: [{
                    data: [ativos, inativos, suspensos],
                    backgroundColor: [
                        '#28a745', // verde
                        '#ffc107', // amarelo
                        '#dc3545'  // vermelho
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                }
            }
        });
    }

    // Gráfico de Áreas
    const areasCanvas = document.getElementById('areasChart');
    if (areasCanvas) {
        const areasCtx = areasCanvas.getContext('2d');
        new Chart(areasCtx, {
            type: 'bar',
            data: {
                labels: ['Assistência', 'Saúde', 'Educação', 'Social'],
                datasets: [{
                    label: 'Quantidade de Usuários',
                    data: [
                        areasData.assistencia,
                        areasData.saude,
                        areasData.educacao,
                        areasData.social
                    ],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
}

// Esperar o DOM carregar
document.addEventListener('DOMContentLoaded', function() {
    // Obter dados passados pelo Flask
    const chartData = JSON.parse(document.getElementById('chart-data').textContent);
    
    // Inicializar gráficos
    initCharts(
        chartData.ativos,
        chartData.inativos,
        chartData.suspensos,
        chartData.areas
    );
});

// Função para inicializar os gráficos
function initDashboardCharts() {
    // Obter os dados do elemento JSON
    const chartData = JSON.parse(document.getElementById('chart-data').textContent);
    
    // Gráfico de Situação (Doughnut)
    const situacaoCtx = document.getElementById('situacaoChart');
    if (situacaoCtx) {
        new Chart(situacaoCtx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Ativos', 'Inativos', 'Suspensos'],
                datasets: [{
                    data: [chartData.ativos, chartData.inativos, chartData.suspensos],
                    backgroundColor: ['#28a745', '#ffc107', '#dc3545']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }
    
    // Gráfico de Áreas (Bar)
    const areasCtx = document.getElementById('areasChart');
    if (areasCtx) {
        new Chart(areasCtx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Assistência', 'Saúde', 'Educação', 'Social'],
                datasets: [{
                    label: 'Quantidade de Usuários',
                    data: [
                        chartData.areas.assistencia,
                        chartData.areas.saude,
                        chartData.areas.educacao,
                        chartData.areas.social
                    ],
                    backgroundColor: [
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)'
                    ],
                    borderColor: [
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: { y: { beginAtZero: true } }
            }
        });
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', initDashboardCharts);