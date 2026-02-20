document.addEventListener('DOMContentLoaded', () => {
    // Tabs Logic
    const tabs = document.querySelectorAll('.tab-button');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById(tab.dataset.tab).classList.add('active');
            if (tab.dataset.tab === 'predictions') renderPredictionsChart();
        });
    });

    // Initialize Data
    fetchDashboard();
    fetchProducts();
    fetchAnomalies();

    let dashboardData = null;

    async function fetchDashboard() {
        try {
            const res = await fetch('/api/dashboard');
            const data = await res.json();
            dashboardData = data;
            updateKPIs(data);
            renderOEEChart(data.current);
        } catch (e) {
            console.error('Error fetching dashboard:', e);
        }
    }

    function updateKPIs(data) {
        ['L1', 'L2', 'L3'].forEach(line => {
            const metrics = data.current[line];
            if (metrics) {
                document.getElementById(`${line.toLowerCase()}-oee`).textContent = `${metrics.oee}%`;
            }
        });
        document.getElementById('recommended-line').textContent = data.recommendation.recommended_line;
        document.getElementById('recommendation-reason').textContent = data.recommendation.reason;
    }

    let oeeChart = null;
    function renderOEEChart(currentData) {
        const ctx = document.getElementById('oeeChart').getContext('2d');
        if (oeeChart) oeeChart.destroy();
        oeeChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['L1', 'L2', 'L3'],
                datasets: [{
                    label: 'OEE Actuel (%)',
                    data: ['L1', 'L2', 'L3'].map(l => currentData[l] ? currentData[l].oee : 0),
                    backgroundColor: ['#D32F2F', '#424242', '#757575'],
                    borderColor: '#ffffff',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: { beginAtZero: true, max: 100, grid: { color: '#333' }, ticks: { color: '#E0E0E0' } },
                    x: { ticks: { color: '#E0E0E0' } }
                },
                plugins: { legend: { labels: { color: '#E0E0E0' } } }
            }
        });
    }

    async function fetchProducts() {
        const res = await fetch('/api/products');
        const data = await res.json();
        const select = document.getElementById('product-type');
        data.products.forEach(p => {
            const opt = document.createElement('option');
            opt.value = p.type;
            opt.textContent = p.name;
            select.appendChild(opt);
        });
    }

    document.getElementById('simulate-btn').addEventListener('click', async () => {
        const pType = document.getElementById('product-type').value;
        const qty = document.getElementById('quantity').value;
        const res = await fetch(`/api/recommend?product_type=${pType}&quantity=${qty}`);
        const data = await res.json();
        renderScenarios(data);
    });

    function renderScenarios(data) {
        const grid = document.getElementById('scenarios-grid');
        grid.innerHTML = '';
        [data.details, ...data.alternatives].forEach(s => {
            const card = document.createElement('div');
            card.className = 'scenario-card';
            card.innerHTML = `
                <h3>${s.line_id}</h3>
                <p>Score IA: <strong>${s.score}</strong></p>
                <p>OEE Prédit: ${s.predicted_oee}%</p>
                <p>Temps: ${s.production_time_hours}h</p>
                <p>Status: ${s.status}</p>
            `;
            grid.appendChild(card);
        });
    }

    document.getElementById('search-btn').addEventListener('click', async () => {
        const desc = document.getElementById('anomaly-desc').value;
        const res = await fetch('/api/anomaly/similar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ description: desc })
        });
        const data = await res.json();
        renderSimilar(data.similar_cases);
    });

    function renderSimilar(cases) {
        const div = document.getElementById('similar-cases');
        div.innerHTML = '<h3>Cas Similaires</h3>';
        cases.forEach(c => {
            const item = document.createElement('div');
            item.className = 'similar-case';
            item.innerHTML = `
                <p><strong>${c.similarity}% Similarité</strong> - ${c.machine} (${c.line})</p>
                <p>Symptôme: ${c.symptom}</p>
                <p>Solution: ${c.solution}</p>
            `;
            div.appendChild(item);
        });
    }

    async function fetchAnomalies() {
        const res = await fetch('/api/anomalies');
        const data = await res.json();
        const tbody = document.getElementById('anomalies-tbody');
        tbody.innerHTML = '';
        data.anomalies.slice(0, 5).forEach(a => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${new Date(a.date).toLocaleDateString()}</td>
                <td>${a.line}</td>
                <td>${a.symptom}</td>
                <td>${a.solution}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    function renderPredictionsChart() {
        if (!dashboardData) return;
        const ctx = document.getElementById('predictionsChart').getContext('2d');
        const preds = dashboardData.predictions;
        const labels = preds.L1.map(p => p.date);
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: ['L1', 'L2', 'L3'].map(l => ({
                    label: `Ligne ${l}`,
                    data: preds[l].map(p => p.oee_predicted),
                    borderColor: l === 'L1' ? '#D32F2F' : l === 'L2' ? '#BDBDBD' : '#757575',
                    tension: 0.4,
                    pointBackgroundColor: '#ffffff'
                }))
            },
            options: {
                scales: {
                    y: { grid: { color: '#333' }, ticks: { color: '#E0E0E0' } },
                    x: { ticks: { color: '#E0E0E0' } }
                },
                plugins: { legend: { labels: { color: '#E0E0E0' } } }
            }
        });

        const tbody = document.getElementById('predictions-tbody');
        tbody.innerHTML = '';
        if (preds.L1) {
            for (let i = 0; i < preds.L1.length; i++) {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${preds.L1[i].date}</td>
                    <td>${preds.L1[i].oee_predicted}%</td>
                    <td>${preds.L2[i].oee_predicted}%</td>
                    <td>${preds.L3[i].oee_predicted}%</td>
                `;
                tbody.appendChild(tr);
            }
        }
    }

    // Speed Optimization
    document.getElementById('optimize-speed-btn').addEventListener('click', async () => {
        const line = document.getElementById('speed-line-select').value;
        const prod = document.getElementById('speed-product-select').value;
        const res = await fetch('/api/speed/optimize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ line_id: line, product_type: prod })
        });
        const data = await res.json();
        renderOptimization(data);
    });

    let sweetSpotChart = null;
    function renderOptimization(data) {
        document.getElementById('optimization-results').style.display = 'block';
        const ctx = document.getElementById('sweetSpotChart').getContext('2d');
        if (sweetSpotChart) sweetSpotChart.destroy();
        sweetSpotChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.curve.map(c => c.speed),
                datasets: [{
                    label: 'Production Nette (pcs/h)',
                    data: data.curve.map(c => c.output),
                    borderColor: '#7CB342',
                    fill: true,
                    backgroundColor: 'rgba(124, 179, 66, 0.1)'
                }]
            },
            options: {
                plugins: {
                    annotation: {
                        annotations: {
                            line1: {
                                type: 'line', xMin: data.optimal_speed, xMax: data.optimal_speed,
                                borderColor: 'red', borderWidth: 2, label: { content: 'Sweet Spot', enabled: true }
                            }
                        }
                    }
                }
            }
        });

        document.getElementById('speed-recommendation').innerHTML = `
            <div style="font-size: 24px; font-weight: 700; color: #6B4423;">Vitesse Optimale: ${data.optimal_speed} pcs/h</div>
            <p>Production max: ${data.max_output} pcs/h | Vitesse actuelle: ${data.current_speed} pcs/h</p>
        `;
    }

    // Agent Chat Logic
    const chatInput = document.getElementById('agent-input');
    const sendBtn = document.getElementById('send-agent-btn');
    const chatMessages = document.getElementById('chat-messages');

    async function sendChat() {
        const query = chatInput.value.trim();
        if (!query) return;

        appendMessage('user', query);
        chatInput.value = '';

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query })
            });
            const data = await res.json();
            appendMessage('assistant', data.response);
        } catch (e) {
            console.error('Chat error:', e);
            appendMessage('assistant', "Désolé, j'ai rencontré une erreur technique.");
        }
    }

    function appendMessage(role, text) {
        const msg = document.createElement('div');
        msg.className = `message ${role}`;
        msg.textContent = text;
        chatMessages.appendChild(msg);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    sendBtn.addEventListener('click', sendChat);
    chatInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendChat(); });

    // Proactive Monitoring
    setInterval(() => {
        fetchDashboard(); // Periodically refresh data and alerts
    }, 10000);
});
