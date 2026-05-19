<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    let routeData = {
        pickup: '',
        pickupDate: '',
        delivery: '',
        isRunning: 'yes',
        extras: {
            roofBox: false,
            bikeRack: false,
            extraWheels: false
        }
    };

    let isSubmitting = false;

    onMount(() => {
        // Pull the initial addresses if they came from the homepage form
        const savedQuote = sessionStorage.getItem('shutup-initial-quote');
        if (savedQuote) {
            try {
                const data = JSON.parse(savedQuote);
                if (data.pickupAddr) routeData.pickup = data.pickupAddr;
                if (data.deliveryAddr) routeData.delivery = data.deliveryAddr;
            } catch (e) {
                console.error("Failed to parse initial quote data", e);
            }
        }
    });

    async function handleSubmit(event: Event) {
        event.preventDefault(); // Stops the page from refreshing
        
        isSubmitting = true;
        
        // Save current step data to session storage for consistency
        sessionStorage.setItem('shutup-step3-route', JSON.stringify(routeData));

        try {
            // 1. Gather data from previous steps
            const step1Str = sessionStorage.getItem('shutup-step1-vehicle');
            const step1 = step1Str ? JSON.parse(step1Str) : {};
            
            // Grabbing the updated Photos data which now contains Base64 strings
            const step2Str = sessionStorage.getItem('shutup-step2-photos');
            const step2Data = step2Str ? JSON.parse(step2Str) : {};
            const base64Images = step2Data.images || {};

            // Convert checked 'extras' into a notes string for the AI
            const extrasList = Object.entries(routeData.extras)
                .filter(([_, isChecked]) => isChecked)
                .map(([key, _]) => key)
                .join(', ');
            const finalNotes = extrasList ? `Extras included: ${extrasList}` : "No extras attached.";

            // 2. Build the exact payload for your FastAPI endpoint
            const payload = {
                vehicle: {
                    make: step1.make || "Unknown",
                    model: step1.model || "Unknown",
                    year: parseInt(step1.year) || 0,
                    runs: routeData.isRunning,
                    notes: finalNotes
                },
                // NEW: We are now passing the actual Base64 images object!
                photos: base64Images, 
                route: {
                    pickup: routeData.pickup,
                    delivery: routeData.delivery,
                    distance: "Unknown" // Placeholder until distance calculation is added
                }
            };

            console.log("Sending to AI Dispatch:", payload);

            // 3. Send to FastAPI backend
            const response = await fetch('https://shutup-forwarder-production.up.railway.app/api/submit-job', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                const result = await response.json();
                console.log("Success! Job saved:", result);
                
                // Save the tracking info so the processing page can display it
                // (Using 'shutup-live-job-id' to match our tracking page logic)
                const newJobId = result.job_id || result.id || (result.data && result.data.id);
                sessionStorage.setItem('shutup-live-job-id', newJobId);

                // Navigate to the processing/tracking screen
                goto('/submit/processing'); 
            } else {
                const errorData = await response.json();
                console.error("Backend Error:", errorData);
                alert("Submission failed. Check backend logs.");
            }

        } catch (err) {
            console.error("Network Error:", err);
            alert("Could not connect to AI Dispatcher. Is the FastAPI server running?");
        } finally {
            isSubmitting = false;
        }
    }
</script>

<svelte:head>
    <title>Step 3: Route | ShutUP Forwarder</title>
</svelte:head>

<section class="wizard-section">
    <div class="container wizard-container">
        <div class="wizard-header">
            <a href="/submit/photos" class="back-link">← Back to Photos</a>
            <div class="step-indicator">Step 3 of 5</div>
        </div>

        <div class="wizard-card">
            <h1 class="wizard-title">Transport Details</h1>
            <p class="wizard-sub">Where is the car going, and what condition is it in?</p>

            <form onsubmit={handleSubmit} class="custom-form">
                
                <div class="form-group">
                    <label for="pickup">Pickup Address</label>
                    <input type="text" id="pickup" bind:value={routeData.pickup} placeholder="e.g. Herengracht 12, 1015 BZ Amsterdam" required />
                </div>

                <div class="form-group">
                    <label for="pickupDate">Preferred Pickup Date</label>
                    <input type="date" id="pickupDate" bind:value={routeData.pickupDate} required />
                </div>

                <div class="form-group">
                    <label for="delivery">Delivery Address</label>
                    <input type="text" id="delivery" bind:value={routeData.delivery} placeholder="e.g. Maximilianstr. 5, 80539 Munich" required />
                </div>

                <hr class="divider" />

                <div class="form-group">
                    <label>Does the car drive on its own?</label>
                    <div class="radio-group">
                        <label class="radio-label">
                            <input type="radio" bind:group={routeData.isRunning} value="yes" />
                            <span class="radio-custom"></span>
                            Yes, it runs
                        </label>
                        <label class="radio-label">
                            <input type="radio" bind:group={routeData.isRunning} value="no" />
                            <span class="radio-custom"></span>
                            No, it doesn't start/drive
                        </label>
                    </div>
                </div>

                <hr class="divider" />

                <div class="form-group">
                    <label>Any extras attached or inside the car?</label>
                    <div class="checkbox-group">
                        <label class="checkbox-label">
                            <input type="checkbox" bind:checked={routeData.extras.roofBox} />
                            <span class="checkbox-custom"></span>
                            Roof box
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" bind:checked={routeData.extras.bikeRack} />
                            <span class="checkbox-custom"></span>
                            Bike rack
                        </label>
                        <label class="checkbox-label">
                            <input type="checkbox" bind:checked={routeData.extras.extraWheels} />
                            <span class="checkbox-custom"></span>
                            Extra set of wheels
                        </label>
                    </div>
                </div>

                <button type="submit" class="submit-btn" disabled={isSubmitting}>
                    {#if isSubmitting}
                        Dispatching to AI Agent...
                    {:else}
                        Submit Job to AI Dispatch →
                    {/if}
                </button>
            </form>
        </div>
    </div>
</section>

<style>
    /* Base styles from previous steps */
    .wizard-section { min-height: 100vh; background: radial-gradient(circle at top, #1e293b 0%, #0f172a 100%); color: #ffffff; padding: 60px 20px; font-family: 'Inter', system-ui, sans-serif; }
    .wizard-container { max-width: 600px; margin: 0 auto; }
    .wizard-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
    .back-link { color: #94a3b8; text-decoration: none; font-weight: 500; font-size: 0.95rem; }
    .back-link:hover { color: #60a5fa; }
    .step-indicator { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; color: #cbd5e1; }
    
    .wizard-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; padding: 48px; backdrop-filter: blur(16px); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); }
    .wizard-title { font-size: 2.2rem; font-weight: 700; margin: 0 0 12px 0; background: linear-gradient(to right, #ffffff, #93c5fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .wizard-sub { color: #94a3b8; margin: 0 0 40px 0; font-size: 1.05rem; line-height: 1.5; }

    .custom-form { display: flex; flex-direction: column; gap: 24px; }
    .form-group { display: flex; flex-direction: column; gap: 8px; }
    
    label { font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: #94a3b8; }
    input[type="text"], input[type="date"] { background: rgba(0, 0, 0, 0.25); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 16px; color: #ffffff; font-size: 1rem; transition: all 0.2s ease; }
    input[type="text"]::placeholder { color: #475569; }
    input[type="text"]:focus, input[type="date"]:focus { outline: none; border-color: #3b82f6; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15); background: rgba(0, 0, 0, 0.4); }

    /* Custom Radio & Checkbox Styling */
    .divider { border: 0; height: 1px; background: rgba(255, 255, 255, 0.1); margin: 8px 0; }
    
    .radio-group, .checkbox-group { display: flex; flex-direction: column; gap: 12px; margin-top: 8px; }
    
    .radio-label, .checkbox-label {
        display: flex;
        align-items: center;
        gap: 12px;
        cursor: pointer;
        font-size: 1rem;
        font-weight: 500;
        color: #e2e8f0;
        text-transform: none;
        letter-spacing: normal;
    }

    .radio-label input, .checkbox-label input { display: none; }

    .radio-custom {
        width: 24px; height: 24px; border: 2px solid #64748b; border-radius: 50%;
        display: inline-block; position: relative; transition: all 0.2s ease;
    }
    .radio-label input:checked + .radio-custom { border-color: #3b82f6; }
    .radio-label input:checked + .radio-custom::after {
        content: ''; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        width: 12px; height: 12px; background: #3b82f6; border-radius: 50%;
    }

    .checkbox-custom {
        width: 24px; height: 24px; border: 2px solid #64748b; border-radius: 6px;
        display: inline-block; position: relative; transition: all 0.2s ease;
    }
    .checkbox-label input:checked + .checkbox-custom { background: #3b82f6; border-color: #3b82f6; }
    .checkbox-label input:checked + .checkbox-custom::after {
        content: '✓'; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
        color: white; font-size: 14px; font-weight: bold;
    }

    .submit-btn {
        margin-top: 10px; width: 100%; padding: 18px; font-size: 1.1rem; border-radius: 12px;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white; border: none; font-weight: 600; cursor: pointer; transition: transform 0.1s ease, box-shadow 0.2s ease;
        box-shadow: 0 10px 20px -10px rgba(16, 185, 129, 0.5);
    }
    .submit-btn:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 15px 25px -10px rgba(16, 185, 129, 0.7); }
    .submit-btn:disabled { opacity: 0.7; cursor: not-allowed; }

    @media (max-width: 600px) {
        .wizard-card { padding: 30px 20px; }
        .wizard-section { padding: 30px 15px; }
    }
</style>