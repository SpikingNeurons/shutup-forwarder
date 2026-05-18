<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    // State to hold our retrieved data
    let jobData = {
        make: 'Unknown Vehicle',
        pickup: 'Origin',
        delivery: 'Destination'
    };

    // State for our fake AI loading sequence
    let aiSteps = $state({
        details: false,
        photos: false,
        route: false,
        drivers: false,
        bids: 0
    });

    onMount(() => {
        // 1. Pull data from sessionStorage
        let step1: any = {};
        let step2: any = {};
        let step3: any = {};
        try {
            step1 = JSON.parse(sessionStorage.getItem('shutup-step1-vehicle') || '{}');
            step2 = JSON.parse(sessionStorage.getItem('shutup-step2-photos') || '{}');
            step3 = JSON.parse(sessionStorage.getItem('shutup-step3-route') || '{}');
            
            if (step1.make && step1.model) jobData.make = `${step1.make} ${step1.model}`;
            if (step3.pickup) jobData.pickup = step3.pickup.split(',')[0];
            if (step3.delivery) jobData.delivery = step3.delivery.split(',')[0];
        } catch(e) {
            console.error("Error reading session data:", e);
        }

        // --- THE FAKE AI SEQUENCE + REAL API CALL ---
        setTimeout(() => aiSteps.details = true, 1000);   
        setTimeout(() => aiSteps.photos = true, 2500);    
        setTimeout(() => aiSteps.route = true, 4000);     
        
        setTimeout(async () => {
            aiSteps.drivers = true;                       
            
            // Simulate bids coming in while we wait for the backend
            const bidInterval = setInterval(() => {
                if (aiSteps.bids < 3) aiSteps.bids += 1;
            }, 800);

            try {
                // ACTUAL BACKEND CONNECTION!
                const response = await fetch('http://127.0.0.1:8000/api/submit-job', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        vehicle: step1,
                        photos: step2,
                        route: step3
                    })
                });

                const result = await response.json();
                console.log("Backend response:", result); // Check your browser console to see this!

                clearInterval(bidInterval);
                aiSteps.bids = 3; // Max out the bids visually

                if (response.ok) {
                    // BULLETPROOF ID GRABBER: 
                    // This checks the different ways FastAPI might have returned the ID
                    const newJobId = result.job_id || result.id || (result.data && result.data.id);
                    
                    console.log("Saving this ID to session storage:", newJobId);
                    
                    // Save the real job ID so the Tracking page can fetch it!
                    sessionStorage.setItem('shutup-live-job-id', newJobId);
                    
                    // AI found a driver & backend saved it! Move to final tracking step
                    setTimeout(() => goto('/submit/tracking'), 1500); 
                } else {
                    alert("Backend error: " + (result.detail || "Unknown error"));
                }
            } catch (error) {
                // ... your existing catch block ...
                clearInterval(bidInterval);
                console.error("Failed to reach backend:", error);
                alert("Could not connect to the Python backend. Is it running on port 8000?");
            }

        }, 5500);
    });
</script>
<svelte:head>
    <title>AI Processing | ShutUP Forwarder</title>
</svelte:head>

<section class="wizard-section">
    <div class="container wizard-container">
        
        <div class="summary-card">
            <div class="job-id">Job #SF-4821 <span class="badge-success">Submitted ✅</span></div>
            <h2 class="car-name">{jobData.make}</h2>
            <div class="route-display">
                <span class="city">{jobData.pickup}</span>
                <span class="arrow">──────►</span>
                <span class="city">{jobData.delivery}</span>
            </div>
        </div>

        <div class="wizard-card processing-card">
            <div class="ai-header">
                <span class="pulse-robot">🤖</span> 
                <h1 class="wizard-title">AI is working on your job...</h1>
            </div>

            <div class="checklist">
                <div class="check-item" class:active={aiSteps.details}>
                    <span class="icon">{aiSteps.details ? '✅' : '⏳'}</span>
                    <span>Car details verified</span>
                </div>
                <div class="check-item" class:active={aiSteps.photos}>
                    <span class="icon">{aiSteps.photos ? '✅' : '⏳'}</span>
                    <span>Photos annotated & locked</span>
                </div>
                <div class="check-item" class:active={aiSteps.route}>
                    <span class="icon">{aiSteps.route ? '✅' : '⏳'}</span>
                    <span>Route & documents checked</span>
                </div>
                <div class="check-item" class:active={aiSteps.drivers}>
                    <span class="icon">{aiSteps.drivers ? '✅' : '⏳'}</span>
                    <span>Finding available drivers...</span>
                </div>
            </div>

            <div class="bidding-box" class:visible={aiSteps.drivers}>
                <div class="bid-count">
                    <strong>{aiSteps.bids}</strong> drivers notified
                </div>
                <div class="bid-status">
                    {#if aiSteps.bids < 3}
                        Awaiting bids...
                    {:else}
                        <span style="color: #4ade80;">Driver secured! Finalizing contract...</span>
                    {/if}
                </div>
            </div>

            <p class="processing-note">You'll automatically be redirected once a driver is confirmed. Usually under 3 hours.</p>
        </div>
    </div>
</section>

<style>
    /* Base styles */
    .wizard-section { min-height: 100vh; background: radial-gradient(circle at top, #1e293b 0%, #0f172a 100%); color: #ffffff; padding: 60px 20px; font-family: 'Inter', system-ui, sans-serif; display: flex; align-items: center; justify-content: center; }
    .wizard-container { width: 100%; max-width: 500px; }
    
    /* Summary Card */
    .summary-card { background: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 20px; margin-bottom: 24px; text-align: center; }
    .job-id { color: #94a3b8; font-size: 0.9rem; font-weight: 600; display: flex; justify-content: center; align-items: center; gap: 10px; margin-bottom: 8px; }
    .badge-success { background: rgba(74, 222, 128, 0.1); color: #4ade80; padding: 4px 8px; border-radius: 6px; font-size: 0.75rem; }
    .car-name { font-size: 1.4rem; font-weight: 700; margin: 0 0 12px 0; color: #f8fafc; }
    .route-display { display: flex; justify-content: center; align-items: center; gap: 12px; font-weight: 500; color: #cbd5e1; }
    .arrow { color: #3b82f6; font-size: 0.8rem; letter-spacing: -2px;}

    /* Main Card */
    .wizard-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; padding: 40px; backdrop-filter: blur(16px); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); }
    
    .ai-header { display: flex; align-items: center; gap: 16px; margin-bottom: 30px; }
    .pulse-robot { font-size: 2.5rem; animation: float 3s ease-in-out infinite; }
    .wizard-title { font-size: 1.5rem; font-weight: 700; margin: 0; background: linear-gradient(to right, #ffffff, #93c5fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    /* Checklist */
    .checklist { display: flex; flex-direction: column; gap: 16px; margin-bottom: 30px; }
    .check-item { display: flex; align-items: center; gap: 12px; font-size: 1.05rem; color: #64748b; transition: color 0.3s ease; }
    .check-item.active { color: #f8fafc; font-weight: 500; }
    .icon { font-size: 1.2rem; }

    /* Bidding Box */
    .bidding-box { background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 12px; padding: 20px; text-align: center; opacity: 0; transform: translateY(10px); transition: all 0.5s ease; margin-bottom: 24px; }
    .bidding-box.visible { opacity: 1; transform: translateY(0); }
    .bid-count { font-size: 1.2rem; margin-bottom: 4px; color: #e2e8f0; }
    .bid-count strong { font-size: 1.5rem; color: #60a5fa; }
    .bid-status { color: #94a3b8; font-size: 0.95rem; }

    .processing-note { color: #64748b; font-size: 0.85rem; text-align: center; line-height: 1.5; margin: 0; }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }
</style>