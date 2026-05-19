<script lang="ts">
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';

    // The full lifecycle of a job
    type JobStatus = 'pending_pickup' | 'in_transit' | 'delivery_protocol' | 'ai_analyzing' | 'resolved';
    
    // Start with empty placeholders so Svelte doesn't crash before loading
    let activeJob = $state({
        id: '',
        make: '',
        model: '',
        pickup: '',
        delivery: '',
        payout: '₹5,000',
        status: 'pending_pickup' as JobStatus
    });

    // When the page loads, grab the real car from localStorage!
    onMount(() => {
        const savedJob = localStorage.getItem('activeTransitJob');
        if (savedJob) {
            const parsedJob = JSON.parse(savedJob);
            activeJob = {
                id: parsedJob.id || '',
                make: parsedJob.make || parsedJob.vehicleMake || 'Unknown Make',
                model: parsedJob.model || parsedJob.vehicleModel || 'Unknown Model',
                pickup: parsedJob.pickup || parsedJob.pickupAddress || 'Unknown Pickup',
                delivery: parsedJob.delivery || parsedJob.deliveryAddress || 'Unknown Delivery',
                payout: parsedJob.payout || '₹5,000',
                status: 'pending_pickup'
            };
        } else {
            // If they somehow got here without clicking a job, kick them back
            goto('/jobs');
        }
    });

    let protocolStarted = $state(false);
    let isCompleting = $state(false); // NEW: Tracks the backend loading state
    
    // Pickup Photos
    let pickupPhotos = $state([
        { label: 'Front View', uploaded: false },
        { label: 'Rear View', uploaded: false },
        { label: 'Left Side', uploaded: false },
        { label: 'Right Side', uploaded: false }
    ]);

    // Delivery Photos
    let deliveryPhotos = $state([
        { label: 'Front View', uploaded: false },
        { label: 'Rear View', uploaded: false },
        { label: 'Left Side', uploaded: false },
        { label: 'Right Side', uploaded: false }
    ]);

    let allPickupUploaded = $derived(pickupPhotos.every(p => p.uploaded));
    let allDeliveryUploaded = $derived(deliveryPhotos.every(p => p.uploaded));

    // AI Assessment State
    let aiAssessmentResult = $state<'cleared' | 'damage_detected' | null>(null);

    // --- PICKUP PHASE ---
    function simulatePickupUpload(index: number) {
        setTimeout(() => { pickupPhotos[index].uploaded = true; }, 600);
    }

    function completePickup() {
        activeJob.status = 'in_transit';
    }

    // --- TRANSIT PHASE ---
    function arriveAtDelivery() {
        activeJob.status = 'delivery_protocol';
    }

    // --- DELIVERY PHASE ---
    function simulateDeliveryUpload(index: number) {
        setTimeout(() => { deliveryPhotos[index].uploaded = true; }, 600);
    }

    function runAIAnalysis(forceResult: 'cleared' | 'damage_detected') {
        activeJob.status = 'ai_analyzing';
        
        // Simulate AI comparing pixels for 2.5 seconds
        setTimeout(() => {
            aiAssessmentResult = forceResult;
            activeJob.status = 'resolved';
        }, 2500);
    }

    // NEW: Complete Job Backend Integration
    async function finalizeJob() {
        if (!activeJob.id) {
            alert("Error: Job ID is missing.");
            return;
        }

        isCompleting = true;
        try {
            const response = await fetch(`https://shutup-forwarder-production.up.railway.app/api/jobs/${activeJob.id}/complete`, {
                method: 'PATCH'
            });

            if (response.ok) {
                // Clear the active job from local storage so they can accept a new one
                localStorage.removeItem('activeTransitJob');
                alert("Job successfully completed!");
                goto('/jobs');
            } else {
                const errorData = await response.json();
                alert("Failed to complete job: " + errorData.detail);
            }
        } catch (error) {
            console.error("Error completing job:", error);
            alert("Network error. Make sure you are connected.");
        } finally {
            isCompleting = false;
        }
    }
</script>

<div class="active-layout">
    <header class="active-header">
        <div>
            <h1>Active Load Tracker</h1>
            <p class="subtitle">
                {#if activeJob.status === 'pending_pickup'} Complete pickup protocol.
                {:else if activeJob.status === 'in_transit'} En route to destination.
                {:else if activeJob.status === 'delivery_protocol'} Final delivery verification.
                {:else} Job resolution. {/if}
            </p>
        </div>
        <a href="/jobs" class="btn-outline">← Exit</a>
    </header>

    <div class="job-card">
        <div class="card-header">
            <h2>{activeJob.make} {activeJob.model}</h2>
            {#if activeJob.status === 'pending_pickup'} <span class="badge badge-warning">Awaiting Pickup</span>
            {:else if activeJob.status === 'in_transit'} <span class="badge badge-info">In Transit</span>
            {:else if activeJob.status === 'resolved'} <span class="badge badge-success">Completed</span>
            {:else} <span class="badge badge-warning">Verification</span> {/if}
        </div>

        {#if activeJob.status === 'pending_pickup'}
            <div class="protocol-section reveal-anim">
                <h3>Step 1: Pickup Protocol</h3>
                <p class="sub-text">Capture 4 angles to verify pre-existing condition.</p>
                
                <div class="photo-grid">
                    {#each pickupPhotos as photo, i}
                        <button class="photo-zone" class:uploaded={photo.uploaded} onclick={() => simulatePickupUpload(i)} disabled={photo.uploaded}>
                            {#if photo.uploaded} <span class="check">✅</span> <span>{photo.label} Locked</span>
                            {:else} <span class="camera-icon">📷</span> <span>Capture {photo.label}</span> {/if}
                        </button>
                    {/each}
                </div>
                <button class="btn-primary" disabled={!allPickupUploaded} onclick={completePickup}>
                    {allPickupUploaded ? "Lock Photos & Start Transit" : "Upload all photos to continue..."}
                </button>
            </div>

        {:else if activeJob.status === 'in_transit'}
            <div class="transit-state reveal-anim">
                <div class="success-icon">🚚</div>
                <h2 class="text-blue">Transit Initiated</h2>
                <p>GPS tracking active. Proceed to {activeJob.delivery}.</p>
                <button class="btn-primary" onclick={arriveAtDelivery}>
                    📍 I have arrived at Drop-off
                </button>
            </div>

        {:else if activeJob.status === 'delivery_protocol'}
            <div class="protocol-section reveal-anim">
                <h3>Step 2: Delivery Verification</h3>
                <p class="sub-text">Capture final photos for AI damage comparison.</p>
                
                <div class="photo-grid">
                    {#each deliveryPhotos as photo, i}
                        <button class="photo-zone" class:uploaded={photo.uploaded} onclick={() => simulateDeliveryUpload(i)} disabled={photo.uploaded}>
                            {#if photo.uploaded} <span class="check">✅</span> <span>{photo.label} Locked</span>
                            {:else} <span class="camera-icon">📸</span> <span>Capture {photo.label}</span> {/if}
                        </button>
                    {/each}
                </div>

                {#if allDeliveryUploaded}
                    <div class="test-controls reveal-anim">
                        <p class="test-label">Developer Test: Choose AI Outcome</p>
                        <div class="btn-group">
                            <button class="btn-success" onclick={() => runAIAnalysis('cleared')}>Simulate: No Damage</button>
                            <button class="btn-danger" onclick={() => runAIAnalysis('damage_detected')}>Simulate: Damage Found</button>
                        </div>
                    </div>
                {/if}
            </div>

        {:else if activeJob.status === 'ai_analyzing'}
            <div class="analyzing-state reveal-anim">
                <div class="scanner-line"></div>
                <div class="ai-icon pulse">🤖</div>
                <h2>AI is comparing pixels...</h2>
                <p>Cross-referencing pickup and delivery conditions.</p>
            </div>

        {:else if activeJob.status === 'resolved'}
            <div class="resolution-state reveal-anim">
                
                {#if aiAssessmentResult === 'cleared'}
                    <div class="alert alert-success">
                        <strong>✅ AI Cleared: No Damage Detected</strong>
                        <p>Vehicle matches original condition. Job complete.</p>
                    </div>
                {:else}
                    <div class="alert alert-danger">
                        <strong>⚠️ AI Flagged: Damage Detected</strong>
                        <p>New scratch detected on Left Side. Automated insurance claim filed.</p>
                    </div>
                {/if}

                <div class="comparison-board">
                    <div class="comparison-column">
                        <h4 class="col-title">Pickup (Before)</h4>
                        <div class="mini-grid">
                            {#each pickupPhotos as p} <div class="mini-photo locked">{p.label}</div> {/each}
                        </div>
                    </div>
                    <div class="comparison-column">
                        <h4 class="col-title">Delivery (After)</h4>
                        <div class="mini-grid">
                            {#each deliveryPhotos as p} 
                                <div class="mini-photo {aiAssessmentResult === 'damage_detected' && p.label === 'Left Side' ? 'flagged' : 'locked'}">
                                    {p.label}
                                </div> 
                            {/each}
                        </div>
                    </div>
                </div>

                {#if aiAssessmentResult === 'cleared'}
                    <button class="btn-primary mt-4" disabled={isCompleting} onclick={finalizeJob}>
                        {isCompleting ? 'Finalizing...' : 'Finalize & Return to Board'}
                    </button>
                {:else}
                    <button class="btn-danger mt-4" disabled={isCompleting} onclick={finalizeJob}>
                        {isCompleting ? 'Filing Claim...' : 'Acknowledge Claim & Return'}
                    </button>
                {/if}
            </div>
        {/if}
    </div>
</div>

<style>
    /* Premium Dark Theme */
    .active-layout { padding: 40px 20px; background: #0f172a; min-height: 100vh; color: #f8fafc; font-family: 'Inter', system-ui, sans-serif; max-width: 900px; margin: 0 auto; }
    .active-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }
    .active-header h1 { margin: 0; font-size: 2rem; font-weight: 700; color: #ffffff; }
    .subtitle { margin: 4px 0 0 0; color: #94a3b8; font-size: 0.95rem; }

    .btn-outline { background: transparent; color: #94a3b8; text-decoration: none; padding: 8px 16px; border-radius: 8px; border: 1px solid #334155; transition: all 0.2s; }
    .btn-outline:hover { background: #1e293b; color: #f8fafc; }

    .job-card { background: #1e293b; border: 1px solid #334155; border-radius: 16px; padding: 32px; }
    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #334155; }
    .card-header h2 { margin: 0; color: #f1f5f9; }
    
    .badge { padding: 6px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; }
    .badge-warning { background: rgba(245, 158, 11, 0.1); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.2); }
    .badge-info { background: rgba(56, 189, 248, 0.1); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.2); }
    .badge-success { background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.2); }

    /* Protocol Sections */
    .protocol-section h3 { margin: 0 0 4px 0; color: #f1f5f9; }
    .sub-text { color: #94a3b8; font-size: 0.9rem; margin-bottom: 24px; }

    .photo-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 32px; }
    .photo-zone { background: #0f172a; border: 2px dashed #475569; border-radius: 12px; padding: 24px; display: flex; flex-direction: column; align-items: center; gap: 8px; color: #94a3b8; cursor: pointer; transition: all 0.2s; font-family: inherit; font-size: 0.95rem; }
    .photo-zone:hover:not(:disabled) { border-color: #3b82f6; color: #3b82f6; }
    .photo-zone.uploaded { border-style: solid; border-color: #10b981; color: #10b981; background: rgba(16, 185, 129, 0.05); cursor: default; }
    .camera-icon, .check { font-size: 1.5rem; }

    /* Buttons */
    .btn-primary { width: 100%; padding: 16px; border: none; border-radius: 8px; background: #3b82f6; color: white; font-size: 1.1rem; font-weight: 600; cursor: pointer; transition: background 0.2s; }
    .btn-primary:hover:not(:disabled) { background: #2563eb; }
    .btn-primary:disabled { background: #334155; color: #64748b; cursor: not-allowed; }
    
    .btn-success { padding: 14px; border: none; border-radius: 8px; background: #10b981; color: white; font-weight: 600; cursor: pointer; width: 100%; transition: background 0.2s; }
    .btn-success:hover { background: #059669; }
    .btn-danger { padding: 14px; border: none; border-radius: 8px; background: #ef4444; color: white; font-weight: 600; cursor: pointer; width: 100%; transition: background 0.2s; }
    .btn-danger:hover:not(:disabled) { background: #dc2626; }
    .btn-danger:disabled { background: #334155; color: #64748b; cursor: not-allowed; }
    .btn-group { display: flex; gap: 16px; }

    /* Developer Test Controls */
    .test-controls { margin-top: 32px; padding: 20px; background: rgba(168, 85, 247, 0.1); border: 1px dashed #c084fc; border-radius: 12px; }
    .test-label { color: #c084fc; font-weight: 700; font-size: 0.85rem; text-transform: uppercase; margin-top: 0; margin-bottom: 12px; }

    /* Transit State */
    .transit-state { text-align: center; padding: 40px 20px; }
    .success-icon { font-size: 4rem; margin-bottom: 16px; }
    .text-blue { color: #38bdf8; }
    .transit-state p { color: #94a3b8; margin-bottom: 32px; }

    /* AI Analyzing State */
    .analyzing-state { text-align: center; padding: 60px 20px; position: relative; overflow: hidden; }
    .ai-icon { font-size: 4rem; margin-bottom: 16px; display: inline-block; }
    .pulse { animation: pulseAnim 1s infinite alternate; }
    @keyframes pulseAnim { from { transform: scale(1); opacity: 0.8; } to { transform: scale(1.1); opacity: 1; } }

    /* Resolution State */
    .alert { padding: 16px 20px; border-radius: 12px; margin-bottom: 32px; }
    .alert strong { display: block; font-size: 1.1rem; margin-bottom: 4px; }
    .alert p { margin: 0; font-size: 0.95rem; opacity: 0.9; }
    .alert-success { background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; color: #34d399; }
    .alert-danger { background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; color: #f87171; }

    .comparison-board { display: flex; gap: 24px; background: #0f172a; padding: 24px; border-radius: 12px; border: 1px solid #334155; }
    .comparison-column { flex: 1; }
    .col-title { margin: 0 0 16px 0; color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; text-align: center; border-bottom: 1px solid #334155; padding-bottom: 8px; }
    
    .mini-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .mini-photo { background: #1e293b; border-radius: 8px; padding: 16px 8px; text-align: center; font-size: 0.75rem; color: #64748b; font-weight: 600; }
    .mini-photo.locked { border: 1px solid #334155; }
    .mini-photo.flagged { border: 2px solid #ef4444; color: #ef4444; background: rgba(239, 68, 68, 0.1); }

    .mt-4 { margin-top: 32px; }
    .reveal-anim { animation: slideUp 0.3s ease-out forwards; }
    @keyframes slideUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>