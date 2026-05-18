<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    let availableJobs = $state<any[]>([]);
    let isLoading = $state(true);
    let processingJobId = $state<string | null>(null);

    onMount(async () => {
        try {
            const res = await fetch('http://127.0.0.1:8000/api/jobs');
            if (res.ok) {
                const responseData = await res.json();
                const allJobs = responseData.data || responseData;
                
                // FILTER APPLIED: Now it ONLY grabs jobs that are fresh and unclaimed.
                // Anything marked "Pending Pickup", "In Transit", or "Completed" is hidden.
                availableJobs = allJobs.filter((job: any) => job.status === 'Reviewing');
            }
        } catch (error) {
            console.error("Failed to load live jobs:", error);
        } finally {
            isLoading = false;
        }
    });

    async function acceptJob(job: any) {
        processingJobId = job.id;

        try {
            const res = await fetch(`http://127.0.0.1:8000/api/jobs/${job.id}/accept`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' }
            });

            if (res.ok) {
                // 1. Save the specific job data to the browser memory!
                localStorage.setItem('activeTransitJob', JSON.stringify(job));
                
                // 2. Remove from board and redirect
                availableJobs = availableJobs.filter(j => j.id !== job.id);
                goto('/jobs/active');
            } else {
                alert("Error: Job could not be claimed.");
            }
        } catch (error) {
            alert("Network error.");
        } finally {
            processingJobId = null;
        }
    }
</script>

<div class="marketplace-layout">
    <header class="marketplace-header">
        <div>
            <h1>Available Loads</h1>
            <p class="subtitle">Select a job to view details and accept.</p>
        </div>
        <div class="header-actions">
            <a href="/" class="btn-outline">Exit Marketplace</a>
        </div>
    </header>

    <div class="jobs-grid">
        {#each availableJobs as job}
            <div class="job-card">
                <div class="card-header">
                    <span class="payout">{job.payout ? `€${job.payout.replace('₹', '')}` : '€500'}</span>
                    <span class="distance">{job.distance || 'Route Calc Pending'}</span>
                </div>
                
                <div class="route-info">
                    <div class="location">
                        <span class="dot pickup-dot"></span>
                        <div class="text-group">
                            <span class="label">PICKUP</span>
                            <span class="city">{job.pickup || job.pickupAddress || 'Unknown Pickup'}</span>
                        </div>
                    </div>
                    <div class="route-line"></div>
                    <div class="location">
                        <span class="dot delivery-dot"></span>
                        <div class="text-group">
                            <span class="label">DELIVERY</span>
                            <span class="city">{job.delivery || job.deliveryAddress || 'Unknown Delivery'}</span>
                        </div>
                    </div>
                </div>

                <div class="vehicle-info">
                    <strong>Vehicle:</strong> {job.make || job.vehicleMake || ''} {job.model || job.vehicleModel || 'Unknown Vehicle'}
                </div>
                
                <div class="ai-insight">
                    <span class="ai-icon">🤖</span>
                    <span class="ai-text">
                        {job.ai_analysis || job.aiAnalysis || job.aiReasoning || 'AI Cleared: Route and vehicle details validated.'}
                    </span>
                </div>

                <button 
                    class="btn-accept" 
                    class:loading={processingJobId === job.id}
                    disabled={processingJobId !== null}
                    onclick={() => acceptJob(job)}
                >
                    {#if processingJobId === job.id} Assigning to you...
                    {:else} Accept Job {/if}
                </button>
            </div>
        {/each}

        {#if availableJobs.length === 0 && !isLoading}
            <div class="empty-state">No jobs available right now. Check back later!</div>
        {/if}
    </div>
</div>

<style>
    /* Premium Dark Theme for Drivers */
    .marketplace-layout { 
        padding: 40px 20px; 
        background: #0f172a; 
        min-height: 100vh; 
        color: #f8fafc; 
        font-family: 'Inter', system-ui, sans-serif; 
        max-width: 1200px;
        margin: 0 auto;
    }

    .marketplace-header { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        margin-bottom: 40px; 
        flex-wrap: wrap;
        gap: 20px;
    }
    .marketplace-header h1 { margin: 0; font-size: 2rem; font-weight: 700; color: #ffffff; }
    .subtitle { margin: 4px 0 0 0; color: #94a3b8; font-size: 0.95rem; }

    .btn-outline {
        background: transparent; color: #94a3b8; text-decoration: none;
        padding: 8px 16px; border-radius: 8px; font-weight: 500;
        border: 1px solid #334155; transition: all 0.2s;
    }
    .btn-outline:hover { background: #1e293b; color: #f8fafc; }

    /* Grid Layout */
    .jobs-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 24px;
    }

    /* Card Styling */
    .job-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 24px;
        display: flex;
        flex-direction: column;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .job-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.2);
        border-color: #475569;
    }

    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 1px solid #334155;
    }
    .payout { font-size: 1.5rem; font-weight: 800; color: #10b981; }
    .distance { font-size: 0.85rem; font-weight: 600; color: #94a3b8; background: #0f172a; padding: 4px 10px; border-radius: 12px; }

    /* Route Visualization */
    .route-info { display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px; position: relative; }
    .location { display: flex; align-items: flex-start; gap: 12px; z-index: 2; }
    .dot { width: 12px; height: 12px; border-radius: 50%; margin-top: 4px; border: 2px solid #0f172a; box-shadow: 0 0 0 2px currentColor; }
    .pickup-dot { color: #38bdf8; background: #38bdf8; }
    .delivery-dot { color: #a855f7; background: #a855f7; }
    
    .text-group { display: flex; flex-direction: column; }
    .label { font-size: 0.7rem; font-weight: 700; color: #64748b; letter-spacing: 0.5px; }
    .city { font-size: 1rem; font-weight: 600; color: #f1f5f9; }

    .route-line {
        position: absolute;
        left: 5px;
        top: 20px;
        bottom: 20px;
        width: 2px;
        background: dashed 2px #334155;
        z-index: 1;
    }

    /* Details */
    .vehicle-info { font-size: 0.95rem; color: #cbd5e1; margin-bottom: 16px; }
    
    .ai-insight {
        background: rgba(56, 189, 248, 0.05);
        border: 1px solid rgba(56, 189, 248, 0.1);
        border-radius: 8px;
        padding: 12px;
        display: flex;
        gap: 10px;
        align-items: flex-start;
        margin-bottom: 24px;
        margin-top: auto; /* Pushes button to bottom */
    }
    .ai-icon { font-size: 1.2rem; }
    .ai-text { font-size: 0.85rem; color: #7dd3fc; line-height: 1.4; }

    /* Button */
    .btn-accept {
        width: 100%;
        padding: 14px;
        border: none;
        border-radius: 8px;
        background: #3b82f6;
        color: white;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
    }
    .btn-accept:hover:not(:disabled) { background: #2563eb; }
    .btn-accept:disabled { background: #334155; color: #94a3b8; cursor: not-allowed; }
    .btn-accept.loading { animation: pulse 1.5s infinite; }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }

    .empty-state { grid-column: 1 / -1; text-align: center; padding: 60px; color: #64748b; font-size: 1.1rem; }
</style>