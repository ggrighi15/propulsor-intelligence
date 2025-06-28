class CRMApp {
    constructor() {
        this.apiBase = '/api/crm';
        this.currentPage = 1;
        this.currentTab = 'dashboard';
        this.colors = null;
        this.charts = {};
        
        this.init();
    }

    async init() {
        this.setupEventListeners();
        await this.loadColors();
        await this.loadDashboard();
    }

    setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchTab(e.target.dataset.tab);
            });
        });

        // Global search
        const globalSearch = document.getElementById('globalSearch');
        globalSearch.addEventListener('input', this.debounce((e) => {
            this.performGlobalSearch(e.target.value);
        }, 300));

        // Filter inputs
        ['pessoas', 'contratos', 'instituicoes', 'requisicoes'].forEach(entity => {
            const filter = document.getElementById(`${entity}Filter`);
            if (filter) {
                filter.addEventListener('input', this.debounce((e) => {
                    this.filterData(entity, e.target.value);
                }, 300));
            }
        });
    }

    async loadColors() {
        try {
            const response = await fetch(`${this.apiBase}/config/colors`);
            const result = await response.json();
            if (result.success) {
                this.colors = result.data;
                this.updateCSSColors();
            }
        } catch (error) {
            console.error('Erro ao carregar cores:', error);
        }
    }

    updateCSSColors() {
        if (!this.colors) return;
        
        const root = document.documentElement;
        root.style.setProperty('--primary-color', this.colors.background);
        root.style.setProperty('--accent-color', this.colors.tableAccent);
        root.style.setProperty('--light-color', this.colors.foreground);
    }

    async loadDashboard() {
        try {
            this.showLoading('statsGrid');
            
            const response = await fetch(`${this.apiBase}/dashboard/stats`);
            const result = await response.json();
            
            if (result.success) {
                this.renderStats(result.data.stats);
                this.renderContratosChart(result.data.contratos_por_situacao);
                this.renderPessoasChart(result.data.pessoas_por_tipo);
            } else {
                this.showError('statsGrid', result.error);
            }
        } catch (error) {
            this.showError('statsGrid', 'Erro ao carregar dashboard');
            console.error('Erro:', error);
        }
    }

    renderStats(stats) {
        const statsGrid = document.getElementById('statsGrid');
        
        const statsCards = [
            {
                icon: 'fas fa-users',
                number: this.formatNumber(stats.total_pessoas),
                label: 'Total de Pessoas',
                color: '#007dff'
            },
            {
                icon: 'fas fa-file-contract',
                number: this.formatNumber(stats.total_contratos),
                label: 'Total de Contratos',
                color: '#5001b4'
            },
            {
                icon: 'fas fa-building',
                number: this.formatNumber(stats.total_instituicoes),
                label: 'Total de Instituições',
                color: '#65b1ff'
            },
            {
                icon: 'fas fa-clipboard-list',
                number: this.formatNumber(stats.total_requisicoes),
                label: 'Total de Requisições',
                color: '#78aadd'
            }
        ];

        statsGrid.innerHTML = statsCards.map(card => `
            <div class="stat-card">
                <i class="${card.icon}" style="color: ${card.color}"></i>
                <div class="stat-number">${card.number}</div>
                <div class="stat-label">${card.label}</div>
            </div>
        `).join('');
    }

    renderContratosChart(data) {
        const ctx = document.getElementById('contratosChart').getContext('2d');
        
        if (this.charts.contratos) {
            this.charts.contratos.destroy();
        }

        this.charts.contratos = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(item => item.situacao || 'Não definido'),
                datasets: [{
                    data: data.map(item => item.quantidade),
                    backgroundColor: this.colors ? this.colors.dataColors : [
                        '#007dff', '#5001b4', '#65b1ff', '#78aadd', '#0627ff'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    renderPessoasChart(data) {
        const ctx = document.getElementById('pessoasChart').getContext('2d');
        
        if (this.charts.pessoas) {
            this.charts.pessoas.destroy();
        }

        this.charts.pessoas = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(item => item.tipo),
                datasets: [{
                    label: 'Quantidade',
                    data: data.map(item => item.quantidade),
                    backgroundColor: this.colors ? this.colors.dataColors[0] : '#007dff'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    async switchTab(tabName) {
        // Update active tab
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update active content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabName).classList.add('active');

        this.currentTab = tabName;
        this.currentPage = 1;

        // Load data for the tab
        if (tabName !== 'dashboard') {
            await this.loadTabData(tabName);
        }
    }

    async loadTabData(tabName, page = 1, search = '') {
        try {
            const tableId = `${tabName}Table`;
            this.showLoading(tableId);

            const params = new URLSearchParams({
                page: page,
                per_page: 20
            });

            if (search) {
                params.append('search', search);
            }

            const response = await fetch(`${this.apiBase}/${tabName}?${params}`);
            const result = await response.json();

            if (result.success) {
                this.renderTable(tabName, result.data, result.pagination);
            } else {
                this.showError(tableId, result.error);
            }
        } catch (error) {
            this.showError(`${tabName}Table`, 'Erro ao carregar dados');
            console.error('Erro:', error);
        }
    }

    renderTable(tabName, data, pagination) {
        const tableContainer = document.getElementById(`${tabName}Table`);
        
        if (!data || data.length === 0) {
            tableContainer.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-inbox"></i>
                    <h3>Nenhum registro encontrado</h3>
                    <p>Não há dados para exibir no momento.</p>
                </div>
            `;
            return;
        }

        const headers = this.getTableHeaders(tabName);
        const rows = data.map(item => this.renderTableRow(tabName, item)).join('');

        tableContainer.innerHTML = `
            <table>
                <thead>
                    <tr>${headers.map(header => `<th>${header}</th>`).join('')}</tr>
                </thead>
                <tbody>
                    ${rows}
                </tbody>
            </table>
            ${this.renderPagination(pagination)}
        `;
    }

    getTableHeaders(tabName) {
        const headers = {
            pessoas: ['Nome/Razão Social', 'CPF/CNPJ', 'Telefone', 'Endereço', 'Tipo', 'Status'],
            contratos: ['Pasta', 'Título', 'Contratante', 'Contratado', 'Situação', 'Classificação'],
            instituicoes: ['Nome/Razão Social', 'CNPJ', 'Tipo', 'Situação', 'Data Constituição'],
            requisicoes: ['Número', 'Responsável', 'Status', 'Tipo', 'Categoria']
        };
        return headers[tabName] || [];
    }

    renderTableRow(tabName, item) {
        const formatters = {
            pessoas: (item) => `
                <td><strong>${item.nome_ou_razao_social || '-'}</strong></td>
                <td>${item.cpf || item.cnpj || '-'}</td>
                <td>${item.telefone || '-'}</td>
                <td>${item.endereco || '-'}</td>
                <td>${item.tipo || '-'}</td>
                <td>${item.status || '-'}</td>
            `,
            contratos: (item) => `
                <td><strong>${item.pasta || '-'}</strong></td>
                <td>${item.titulo || '-'}</td>
                <td>${item.contratante || '-'}</td>
                <td>${item.contratado || '-'}</td>
                <td>${item.situacao || '-'}</td>
                <td>${item.classificacao || '-'}</td>
            `,
            instituicoes: (item) => `
                <td><strong>${item.nome_ou_razao_social || '-'}</strong></td>
                <td>${item.cnpj || '-'}</td>
                <td>${item.tipo_sociedade || '-'}</td>
                <td>${item.situacao || '-'}</td>
                <td>${this.formatDate(item.data_constituicao) || '-'}</td>
            `,
            requisicoes: (item) => `
                <td><strong>${item.numero || '-'}</strong></td>
                <td>${item.responsavel || '-'}</td>
                <td>${item.status || '-'}</td>
                <td>${item.tipo || '-'}</td>
                <td>${item.categoria || '-'}</td>
            `
        };

        const formatter = formatters[tabName];
        return formatter ? `<tr>${formatter(item)}</tr>` : '';
    }

    renderPagination(pagination) {
        if (!pagination || pagination.total <= pagination.per_page) {
            return '';
        }

        const totalPages = Math.ceil(pagination.total / pagination.per_page);
        const currentPage = pagination.page;
        
        let paginationHTML = '<div class="pagination">';
        
        // Previous button
        if (currentPage > 1) {
            paginationHTML += `<button class="page-btn" onclick="app.changePage(${currentPage - 1})">
                <i class="fas fa-chevron-left"></i>
            </button>`;
        }
        
        // Page numbers
        for (let i = Math.max(1, currentPage - 2); i <= Math.min(totalPages, currentPage + 2); i++) {
            const activeClass = i === currentPage ? 'active' : '';
            paginationHTML += `<button class="page-btn ${activeClass}" onclick="app.changePage(${i})">${i}</button>`;
        }
        
        // Next button
        if (currentPage < totalPages) {
            paginationHTML += `<button class="page-btn" onclick="app.changePage(${currentPage + 1})">
                <i class="fas fa-chevron-right"></i>
            </button>`;
        }
        
        paginationHTML += '</div>';
        return paginationHTML;
    }

    async changePage(page) {
        this.currentPage = page;
        await this.loadTabData(this.currentTab, page);
    }

    async filterData(entity, searchTerm) {
        if (this.currentTab === entity) {
            await this.loadTabData(entity, 1, searchTerm);
        }
    }

    async performGlobalSearch(searchTerm) {
        if (!searchTerm.trim()) return;

        try {
            const response = await fetch(`${this.apiBase}/search?q=${encodeURIComponent(searchTerm)}`);
            const result = await response.json();

            if (result.success) {
                this.showSearchResults(result.data);
            }
        } catch (error) {
            console.error('Erro na busca global:', error);
        }
    }

    showSearchResults(results) {
        // Implementation for showing search results
        console.log('Resultados da busca:', results);
    }

    showLoading(containerId) {
        const container = document.getElementById(containerId);
        container.innerHTML = `
            <div class="loading">
                <i class="fas fa-spinner"></i>
                <p>Carregando...</p>
            </div>
        `;
    }

    showError(containerId, message) {
        const container = document.getElementById(containerId);
        container.innerHTML = `
            <div class="error">
                <i class="fas fa-exclamation-triangle"></i>
                <strong>Erro:</strong> ${message}
            </div>
        `;
    }

    formatNumber(num) {
        return new Intl.NumberFormat('pt-BR').format(num);
    }

    formatDate(dateString) {
        if (!dateString) return null;
        try {
            return new Date(dateString).toLocaleDateString('pt-BR');
        } catch {
            return dateString;
        }
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.app = new CRMApp();
});

