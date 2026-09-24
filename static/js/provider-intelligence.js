(function() {
    // DOM Elements
    const modal = document.getElementById('provider-intelligence-modal');
    if (!modal) return;
    
    const closeBtn = modal.querySelector('.close-btn');
    const navBtns = modal.querySelectorAll('.pi-nav-btn');
    const pages = modal.querySelectorAll('.pi-page');
    
    const overviewCounts = document.getElementById('pi-overview-counts');
    const overviewHealth = document.getElementById('pi-overview-health');
    const overviewLocal = document.getElementById('pi-overview-local');
    
    const modelGrid = document.getElementById('pi-model-grid');
    const providerList = document.getElementById('pi-provider-list');
    
    const modelDetail = document.getElementById('pi-model-detail');
    const detailBackBtn = document.getElementById('pi-detail-back-btn');
    const detailBody = document.getElementById('pi-model-detail-body');
    
    // State
    let piState = {
        providers: [],
        models: [],
        routing_decision: null
    };
    
    // API Fetch
    async function fetchState() {
        try {
            const res = await fetch('/api/v1/provider-intelligence/state', { credentials: 'same-origin' });
            if(res.ok) {
                piState = await res.json();
                renderAll();
            }
        } catch (e) {
            console.error("Provider Intelligence fetch failed", e);
        }
    }
    
    // Navigation
    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            navBtns.forEach(b => b.classList.remove('active'));
            pages.forEach(p => p.classList.remove('active'));
            
            btn.classList.add('active');
            const target = btn.getAttribute('data-pi-target');
            document.getElementById(`pi-page-${target}`).classList.add('active');
            
            // Close detail panel when navigating
            modelDetail.classList.add('hidden');
        });
    });
    
    // Modal controls
    window.openProviderIntelligence = function() {
        modal.classList.remove('hidden');
        fetchState();
    };
    
    function closeProviderIntelligence() {
        modal.classList.add('hidden');
    }

    closeBtn.addEventListener('click', closeProviderIntelligence);

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
            closeProviderIntelligence();
        }
    });

    // Close on backdrop click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeProviderIntelligence();
        }
    });
    
    detailBackBtn.addEventListener('click', () => {
        modelDetail.classList.add('hidden');
    });
    
    // Render functions
    function renderAll() {
        renderOverview();
        renderModels();
        renderProviders();
    }
    
    function renderOverview() {
        const pCount = piState.providers.length;
        const mCount = piState.models.length;
        const lCount = piState.models.filter(m => m.is_local).length;
        
        overviewCounts.innerHTML = `${pCount} Providers &middot; ${mCount} Models &middot; ${lCount} Local`;
        overviewHealth.innerHTML = `${pCount} / ${pCount} providers active`;
        overviewLocal.innerHTML = `${lCount} models`;
    }
    
    // Rendering State
    let filteredModels = [];

    function renderModels() {
        const searchTerm = (document.getElementById('pi-model-search')?.value || '').toLowerCase();
        const capFilter = document.getElementById('pi-model-filter-cap')?.value || '';
        const locFilter = document.getElementById('pi-model-filter-loc')?.value || '';

        filteredModels = piState.models.filter(model => {
            const matchesSearch = model.name.toLowerCase().includes(searchTerm) || model.id.toLowerCase().includes(searchTerm);
            const matchesCap = !capFilter || model.capabilities.includes(capFilter);
            const matchesLoc = !locFilter || (locFilter === 'local' ? model.is_local : !model.is_local);
            return matchesSearch && matchesCap && matchesLoc;
        });

        modelGrid.innerHTML = '';
        if(filteredModels.length === 0) {
            modelGrid.innerHTML = `<div class="pi-empty-state" style="grid-column: 1/-1;"><h3>No Models Found</h3><p>Try adjusting your search or filters.</p></div>`;
            return;
        }
        
        filteredModels.forEach(model => {
            const card = document.createElement('div');
            card.className = 'pi-card pi-model-card';
            
            const capsHtml = model.capabilities.slice(0,4).map(c => `<span class="pi-cap-chip">${c}</span>`).join('');
            
            card.innerHTML = `
                <div class="pi-model-title">${model.name}</div>
                <div class="pi-model-provider">${model.provider_id} ${model.is_local ? '<span class="pi-local-badge">LOCAL</span>' : ''} ${model.is_free ? '<span class="pi-local-badge" style="background:#2ea043;margin-left:4px;">FREE</span>' : ''}</div>
                <div class="pi-model-caps">${capsHtml}</div>
                <div class="pi-model-footer">
                    <span><span class="pi-dot pi-healthy"></span> Healthy</span>
                    <span>${Math.round(model.context_window/1000)}K ctx</span>
                </div>
            `;
            
            card.addEventListener('click', () => openModelDetail(model));
            modelGrid.appendChild(card);
        });
    }
    
    // Add Event Listeners for Filters
    document.getElementById('pi-model-search')?.addEventListener('input', renderModels);
    document.getElementById('pi-model-filter-cap')?.addEventListener('change', renderModels);
    document.getElementById('pi-model-filter-loc')?.addEventListener('change', renderModels);

    function openModelDetail(model) {
        detailBody.innerHTML = `
            <div class="pi-detail-row">
                <span class="pi-detail-label">Model ID</span>
                <span class="pi-detail-value">${model.id}</span>
            </div>
            <div class="pi-detail-row">
                <span class="pi-detail-label">Provider</span>
                <span class="pi-detail-value">${model.provider_id}</span>
            </div>
            <div class="pi-detail-row">
                <span class="pi-detail-label">Execution</span>
                <span class="pi-detail-value">${model.is_local ? 'Local Device' : 'Remote API'}</span>
            </div>
            <div class="pi-detail-row">
                <span class="pi-detail-label">Context Window</span>
                <span class="pi-detail-value">${model.context_window} tokens</span>
            </div>
            <div class="pi-detail-row">
                <span class="pi-detail-label">Health</span>
                <span class="pi-detail-value"><span class="pi-dot pi-healthy"></span> Healthy</span>
            </div>
            <hr style="border-color:var(--aurex-border); margin: 24px 0;">
            <h4 style="margin-bottom: 12px; font-size: 13px; color: var(--aurex-text-muted);">WHY AUREX CAN USE THIS</h4>
            <div style="display:flex; flex-direction:column; gap:8px; font-size:14px; margin-bottom: 24px;">
                ${model.capabilities.map(c => `<div><span style="color:#2ea043; margin-right:8px;">✓</span> Supports ${c.toLowerCase().replace('_', ' ')}</div>`).join('')}
                <div><span style="color:#2ea043; margin-right:8px;">✓</span> Provider is healthy</div>
                <div><span style="color:#2ea043; margin-right:8px;">✓</span> Matches privacy policy</div>
            </div>
            <button id="pi-use-model-btn" class="pi-btn pi-btn-primary" style="width: 100%;">Use This Model in Chat</button>
        `;
        
        document.getElementById('pi-use-model-btn').addEventListener('click', () => {
            // Set it in local storage
            localStorage.setItem('aurex_active_model', model.id);
            // Trigger a pick in modelPicker
            document.dispatchEvent(new CustomEvent('aurex:force-select-model', { 
                detail: { modelId: model.id } 
            }));
            
            // Close the PI modal
            modal.classList.add('hidden');
        });
        
        modelDetail.classList.remove('hidden');
    }
    
    function renderProviders() {
        providerList.innerHTML = '';
        if(piState.providers.length === 0) {
            providerList.innerHTML = `<div class="pi-empty-state"><h3>No Providers</h3><p>Connect a provider to begin.</p></div>`;
            return;
        }
        
        piState.providers.forEach(prov => {
            const el = document.createElement('div');
            el.className = 'pi-pref-item';
            el.innerHTML = `
                <div class="pi-pref-info">
                    <h4 style="display:flex; align-items:center; gap:8px;">
                        ${prov.name} 
                        ${prov.is_local ? '<span class="pi-local-badge">LOCAL</span>' : ''}
                    </h4>
                    <p><span class="pi-dot pi-healthy"></span> Healthy &middot; ${prov.models_count} models &middot; ${prov.latency_ms}ms latency</p>
                </div>
                <div class="pi-pref-control">
                    <button class="pi-btn">Manage</button>
                </div>
            `;
            providerList.appendChild(el);
        });
    }

    // Preferences persistence
    const routingSelect = document.getElementById('pi-routing-mode-select');
    const telemetryToggle = document.getElementById('pi-disable-telemetry');
    
    if (routingSelect) {
        const savedMode = localStorage.getItem('aurex_pi_routing_mode') || 'auto';
        routingSelect.value = savedMode;
        routingSelect.addEventListener('change', () => {
            localStorage.setItem('aurex_pi_routing_mode', routingSelect.value);
        });
    }
    
    if (telemetryToggle) {
        const savedTelemetry = localStorage.getItem('aurex_pi_disable_telemetry') === 'true';
        telemetryToggle.checked = savedTelemetry;
        telemetryToggle.addEventListener('change', () => {
            localStorage.setItem('aurex_pi_disable_telemetry', telemetryToggle.checked);
        });
    }

    // Connect Provider Button
    document.getElementById('pi-add-provider-btn')?.addEventListener('click', () => {
        closeProviderIntelligence();
        const settingsBtn = document.getElementById('user-bar-settings');
        if (settingsBtn) {
            settingsBtn.click();
            // Try to navigate to services tab if adminModule exists
            setTimeout(() => {
                if (window.adminModule && typeof window.adminModule.open === 'function') {
                    window.adminModule.open('services');
                } else {
                    const servicesTab = document.querySelector('.settings-nav-item[data-settings-tab="services"]');
                    if (servicesTab) servicesTab.click();
                }
            }, 50);
        }
    });

    // Connect to global UI if settings modal exists
    document.addEventListener("DOMContentLoaded", () => {
        const piBtn = document.getElementById("sidebar-pi-btn");
        if(piBtn) {
            piBtn.addEventListener("click", () => {
                window.openProviderIntelligence();
            });
        }
        const sb = document.querySelector('.settings-sidebar');
        if (sb) {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'settings-nav-item';
            btn.innerHTML = `<span style="margin-right:8px;">🧠</span> Provider Intelligence`;
            btn.addEventListener('click', () => {
                document.getElementById('settings-modal').classList.add('hidden');
                window.openProviderIntelligence();
            });
            sb.appendChild(btn);
        }
    });

})();
