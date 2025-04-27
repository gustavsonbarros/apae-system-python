// Função para mostrar toast de notificação
function showToast(message, type = 'info', duration = 5000) {
    // Cores baseadas no tipo
    const colors = {
        'success': 'bg-success text-white',
        'error': 'bg-danger text-white',
        'warning': 'bg-warning text-dark',
        'info': 'bg-info text-white'
    };
    
    // Criar elemento toast
    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center border-0 ${colors[type] || colors['info']}`;
    toastEl.setAttribute('role', 'alert');
    toastEl.setAttribute('aria-live', 'assertive');
    toastEl.setAttribute('aria-atomic', 'true');
    
    // Conteúdo do toast
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    // Adicionar ao container
    const container = document.getElementById('toastContainer');
    container.appendChild(toastEl);
    
    // Inicializar e mostrar o toast
    const toast = new bootstrap.Toast(toastEl, {
        autohide: duration > 0,
        delay: duration
    });
    
    toast.show();
    
    // Remover o toast do DOM quando escondido
    toastEl.addEventListener('hidden.bs.toast', () => {
        toastEl.remove();
    });
    
    return toast;
}

// Função para inicializar os gráficos
function initCharts(ativos, inativos, suspensos, areasData) {
    try {
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
        
        // Notificação de sucesso ao carregar gráficos
        showToast('Gráficos carregados com sucesso!', 'success');
    } catch (error) {
        console.error('Erro ao carregar gráficos:', error);
        showToast('Erro ao carregar alguns gráficos', 'error');
    }
}

// Função para verificar atualizações (exemplo)
function checkForUpdates() {
    // Aqui você pode implementar uma chamada AJAX para verificar atualizações
    // Este é apenas um exemplo
    const hasUpdates = Math.random() > 0.7; // 30% de chance de ter atualizações
    
    if (hasUpdates) {
        showToast('Novas atualizações disponíveis!', 'info', 8000);
    }
}

// Esperar o DOM carregar
document.addEventListener('DOMContentLoaded', function() {
    // Obter dados passados pelo Flask
    try {
        const chartData = JSON.parse(document.getElementById('chart-data').textContent);
        
        // Inicializar gráficos
        initCharts(
            chartData.ativos,
            chartData.inativos,
            chartData.suspensos,
            chartData.areas
        );
        
        // Verificar atualizações após 5 segundos
        setTimeout(checkForUpdates, 5000);
        
    } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error);
        showToast('Erro ao carregar dados do dashboard', 'error');
    }
});