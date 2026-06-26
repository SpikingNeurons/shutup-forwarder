<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    // Existing state
    let availableJobs = $state<any[]>([]);
    let isLoading = $state(true);
    
    // New Bidding State
    let selectedJob = $state<any>(null);
    let isFetchingDetails = $state(false);
    let bidAmount = $state<number | ''>('');
    let isSubmittingBid = $state(false);

    onMount(async () => {
        try {
            const res = await fetch('http://127.0.0.1:8000/api/jobs');
            if (res.ok) {
                const responseData = await res.json();
                const allJobs = responseData.data || responseData;
                
                // FILTER APPLIED: Only grabs fresh jobs
                availableJobs = allJobs.filter((job: any) => job.status === 'Reviewing');
            }
        } catch (error) {
            console.error("Failed to load live jobs:", error);
        } finally {
            isLoading = false;
        }
    });

    // 1. Fetch job details and open the sidebar
    async function openBiddingStation(jobId: string) {
        isFetchingDetails = true;
        selectedJob = null; 
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/jobs/${jobId}`);
            const result = await response.json();
            if (result.status === 'success') {
                selectedJob = result.data;
            }
        } catch (error) {
            console.error("Error fetching job details:", error);
        } finally {
            isFetchingDetails = false;
        }
    }

    // 2. Submit the driver's bid
    async function submitBid() {
        if (!bidAmount || bidAmount <= 0) return alert("Please enter a valid amount!");
        
        isSubmittingBid = true;
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/jobs/${selectedJob.id}/bids`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    driverName: "Test Driver", // Hardcoded until Auth is added
                    amount: bidAmount
                })
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                // Svelte 5 reactivity: Create a new array to trigger UI update
                selectedJob.bids = [...(selectedJob.bids || []), result.data]; 
                bidAmount = ''; // Clear input
            } else {
                alert("Failed to submit bid.");
            }
        } catch (error) {
            console.error("Error submitting bid:", error);
            alert("Network error while submitting bid.");
        } finally {
            isSubmittingBid = false;
        }
    }

    let isAcceptingDeal = $state(false);

    async function acceptCounterOffer(bidId: string) {
        isAcceptingDeal = true;
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/jobs/${selectedJob.id}/bids/${bidId}/accept`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' }
            });
            
            const result = await response.json();
            
            if (result.status === 'success') {
                // 1. Save the job to memory so the active dashboard knows what to load
                localStorage.setItem('activeTransitJob', JSON.stringify(selectedJob));
                
                // 2. Teleport the driver to their active jobs dashboard!
                goto('/jobs/active');
            } else {
                alert("Failed to accept the deal.");
            }
        } catch (error) {
            console.error("Error accepting deal:", error);
            alert("Network error.");
        } finally {
            isAcceptingDeal = false;
        }
    }
</script>

<div class="marketplace-layout">
    <header class="marketplace-header">
        <div>
            <h1>Available Loads</h1>
            <p class="subtitle">Select a job to view details and negotiate your rate.</p>
        </div>
        <div class="header-actions">
            <a href="/" class="btn-outline">Exit Marketplace</a>
        </div>
    </header>

    <div class="main-content-split">
        <div class="jobs-grid">
            {#each availableJobs as job}
                <div class="job-card" class:active-card={selectedJob?.id === job.id}>
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
                        class:loading={isFetchingDetails && selectedJob?.id === job.id}
                        onclick={() => openBiddingStation(job.id)}
                    >
                        View & Bid
                    </button>
                </div>
            {/each}

            {#if availableJobs.length === 0 && !isLoading}
                <div class="empty-state">No jobs available right now. Check back later!</div>
            {/if}
        </div>

        <div class="sidebar-wrapper">
            {#if selectedJob}
                <div class="bidding-sidebar">
                    <div class="sidebar-header">
                        <h2 class="sidebar-title">{selectedJob.make} {selectedJob.model}</h2>
                        <p class="sidebar-subtitle">Tracking: {selectedJob.trackingNumber}</p>
                    </div>
                    
                    <div class="sidebar-content">
                        <h3 class="bids-title">Live Negotiations</h3>
                        
                        <div class="bids-list">
                            {#if selectedJob.bids && selectedJob.bids.length > 0}
                                {#each selectedJob.bids as bid}
                                    <div class="bid-item">
                                        <div class="bid-header">
                                            <span class="bid-driver">{bid.driverName}</span>
                                            <div class="bid-details">
                                                <span class="bid-amount" class:text-red-500={bid.status === 'REJECTED'} class:text-green-500={bid.status === 'ACCEPTED'}>
                                                    €{bid.amount}
                                                </span>
                                                <span class="bid-status">{bid.status.replace(/_/g, ' ')}</span>
                                            </div>
                                        </div>

                                        {#if bid.status === 'COUNTER_OFFERED' && bid.aiCounterAmount}
                                            <div class="action-box counter-box">
                                                <div class="box-text">
                                                    <span class="box-label">AI Counter Offer</span>
                                                    <span class="box-value">€{bid.aiCounterAmount}</span>
                                                </div>
                                                <button class="btn-accept sidebar-btn" disabled={isAcceptingDeal} onclick={() => acceptCounterOffer(bid.id)}>
                                                    {isAcceptingDeal ? '...' : 'Accept'}
                                                </button>
                                            </div>
                                        
                                        {:else if bid.status === 'ACCEPTED'}
                                            <div class="action-box success-box">
                                                <div class="box-text">
                                                    <span class="box-label text-emerald-600">Offer Accepted!</span>
                                                    <span class="box-subtext">You won this load.</span>
                                                </div>
                                                <button class="btn-success sidebar-btn" disabled={isAcceptingDeal} onclick={() => acceptCounterOffer(bid.id)}>
                                                    {isAcceptingDeal ? '...' : 'Proceed to Load'}
                                                </button>
                                            </div>
                                        {/if}
                                    </div>
                                {/each}
                            {:else}
                                <p class="empty-bids">No bids yet. Start the negotiation!</p>
                            {/if}
                        </div>

                        <div class="bid-input-group">
                            <input 
                                type="number" 
                                bind:value={bidAmount} 
                                placeholder="Offer €..." 
                                class="bid-input"
                            />
                            <button 
                                class="btn-accept submit-btn" 
                                disabled={isSubmittingBid}
                                onclick={submitBid}
                            >
                                {isSubmittingBid ? '...' : 'Submit'}
                            </button>
                        </div>
                    </div>
                </div>
            {:else}
                <div class="empty-sidebar">
                    <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"></path></svg>
                    <p class="empty-title">Select a Load</p>
                    <p class="empty-subtitle">Click "View & Bid" to open the negotiation terminal.</p>
                </div>
            {/if}
        </div>
    </div>
</div>

<style>
    /* Premium Light Theme Styles */
    .marketplace-layout { 
        padding: 40px 20px; 
        background: #f8fafc; /* slate-50 */
        min-height: 100vh; 
        color: #0f172a; 
        font-family: 'Inter', system-ui, sans-serif; 
        max-width: 1480px; 
        margin: 0 auto;
    }

    .marketplace-header { 
        display: flex; justify-content: space-between; align-items: center; 
        margin-bottom: 40px; flex-wrap: wrap; gap: 20px;
    }
    .marketplace-header h1 { margin: 0; font-size: 2rem; font-weight: 800; color: #0f172a; }
    .subtitle { margin: 4px 0 0 0; color: #64748b; font-size: 0.95rem; font-weight: 500; }

    .btn-outline {
        background: #ffffff; color: #475569; text-decoration: none;
        padding: 8px 16px; border-radius: 8px; font-weight: 600;
        border: 1px solid #cbd5e1; transition: all 0.2s;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .btn-outline:hover { background: #f1f5f9; color: #0f172a; border-color: #94a3b8; }

    /* SPLIT VIEW LAYOUT */
    .main-content-split {
        display: grid;
        grid-template-columns: 1fr 480px; 
        gap: 48px; 
        align-items: start;
    }

    .jobs-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 24px;
    }

    .job-card {
        background: #ffffff; border: 1px solid #cbd5e1; border-radius: 16px;
        padding: 24px; display: flex; flex-direction: column;
        transition: transform 0.2s, box-shadow 0.2s, border-color 0.2s;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .job-card:hover { transform: translateY(-4px); box-shadow: 0 12px 24px rgba(0,0,0,0.1); border-color: #94a3b8; }
    .active-card { border-color: #3b82f6; box-shadow: 0 0 0 2px #3b82f6; } 

    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0; }
    .payout { font-size: 1.5rem; font-weight: 800; color: #10b981; }
    .distance { font-size: 0.85rem; font-weight: 700; color: #475569; background: #f1f5f9; padding: 4px 10px; border-radius: 12px; border: 1px solid #e2e8f0;}

    .route-info { display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px; position: relative; }
    .location { display: flex; align-items: flex-start; gap: 12px; z-index: 2; }
    .dot { width: 12px; height: 12px; border-radius: 50%; margin-top: 4px; border: 2px solid #ffffff; box-shadow: 0 0 0 2px currentColor; }
    .pickup-dot { color: #0ea5e9; background: #0ea5e9; }
    .delivery-dot { color: #8b5cf6; background: #8b5cf6; }
    
    .text-group { display: flex; flex-direction: column; }
    .label { font-size: 0.7rem; font-weight: 700; color: #64748b; letter-spacing: 0.5px; }
    .city { font-size: 1rem; font-weight: 700; color: #0f172a; }

    .route-line { position: absolute; left: 5px; top: 20px; bottom: 20px; width: 2px; background: dashed 2px #cbd5e1; z-index: 1; }

    .vehicle-info { font-size: 0.95rem; color: #475569; margin-bottom: 16px; font-weight: 500; }
    
    .ai-insight {
        background: #f0f9ff; border: 1px solid #bae6fd;
        border-radius: 8px; padding: 12px; display: flex; gap: 10px; align-items: flex-start;
        margin-bottom: 24px; margin-top: auto; 
    }
    .ai-icon { font-size: 1.2rem; }
    .ai-text { font-size: 0.85rem; color: #0369a1; line-height: 1.4; font-weight: 500; }

    .btn-accept {
        width: 100%; padding: 14px; border: none; border-radius: 8px;
        background: #3b82f6; color: white; font-size: 1rem; font-weight: 600;
        cursor: pointer; transition: all 0.2s; box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .btn-accept:hover:not(:disabled) { background: #2563eb; }
    .btn-accept:disabled { background: #f1f5f9; color: #94a3b8; border: 1px solid #cbd5e1; cursor: not-allowed; box-shadow: none; }
    .btn-accept.loading { animation: pulse 1.5s infinite; }
    .sidebar-btn { width: auto; padding: 10px 20px; font-size: 0.9rem; border-radius: 8px; }

    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.7; } 100% { opacity: 1; } }

    .empty-state { grid-column: 1 / -1; text-align: center; padding: 60px; color: #64748b; font-size: 1.1rem; font-weight: 500; }

    /* --- RIGHT SIDEBAR: BIDDING STATION --- */
    .sidebar-wrapper { position: sticky; top: 40px; }

    .bidding-sidebar {
        background: #ffffff; border: 1px solid #cbd5e1; border-radius: 16px;
        overflow: hidden; display: flex; flex-direction: column;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }

    .sidebar-header { 
        background: #f8fafc; 
        padding: 32px; 
        border-bottom: 1px solid #cbd5e1; 
    }
    .sidebar-title { margin: 0; font-size: 1.25rem; font-weight: 800; color: #0f172a; }
    .sidebar-subtitle { margin: 4px 0 0 0; font-size: 0.85rem; color: #64748b; font-family: monospace; font-weight: 600;}

    .sidebar-content { padding: 32px; }
    .bids-title { margin: 0 0 16px 0; font-size: 0.95rem; font-weight: 800; color: #475569; text-transform: uppercase; letter-spacing: 0.5px;}
    
    .bids-list {
        max-height: 400px; overflow-y: auto; display: flex; flex-direction: column;
        gap: 16px; margin-bottom: 32px; padding-right: 12px;
    }

    .bids-list::-webkit-scrollbar { width: 6px; }
    .bids-list::-webkit-scrollbar-track { background: #f1f5f9; border-radius: 4px;}
    .bids-list::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }

    .bid-item {
        background: #f8fafc; border: 1px solid #cbd5e1; 
        padding: 24px; 
        border-radius: 16px; display: flex; flex-direction: column;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    .bid-header { display: flex; justify-content: space-between; align-items: center; width: 100%; }
    .bid-driver { color: #0f172a; font-weight: 700; font-size: 1rem; }
    .bid-details { text-align: right; }
    .bid-amount { display: block; color: #0f172a; font-weight: 800; font-size: 1.25rem; }
    .bid-status { display: block; font-size: 0.65rem; font-weight: 700; color: #64748b; margin-top: 4px; letter-spacing: 0.5px;}

    .text-red-500 { color: #ef4444 !important; }
    .text-green-500 { color: #10b981 !important; }
    .text-emerald-600 { color: #059669 !important; }

    /* Action Boxes */
    .action-box {
        margin-top: 16px; padding: 16px; border-radius: 12px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .counter-box { background: #eff6ff; border: 1px solid #bfdbfe; }
    .success-box { background: #ecfdf5; border: 1px solid #a7f3d0; }

    .box-text { display: flex; flex-direction: column; }
    .box-label { font-size: 0.75rem; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
    .box-value { font-size: 1.25rem; font-weight: 800; color: #2563eb; margin-top: 2px; }
    .box-subtext { font-size: 0.9rem; font-weight: 600; color: #10b981; margin-top: 2px; }

    .btn-success { background: #10b981; color: white; border: none; font-weight: 600; cursor: pointer; transition: 0.2s; }
    .btn-success:hover:not(:disabled) { background: #059669; }

    .empty-bids { color: #64748b; font-size: 0.95rem; font-style: italic; text-align: center; padding: 30px 0; }

    .bid-input-group { 
        border-top: 1px solid #cbd5e1; 
        padding-top: 32px; 
        margin-top: 16px; 
        display: flex; gap: 16px; 
    }
    
    .bid-input {
        flex: 1; background: #f8fafc; border: 1px solid #cbd5e1; color: #0f172a;
        padding: 16px 20px; 
        border-radius: 12px; font-size: 1.1rem;
        font-weight: 600; transition: border-color 0.2s, background 0.2s;
    }
    .bid-input:focus { outline: none; border-color: #3b82f6; background: #ffffff;}
    .bid-input::placeholder { color: #94a3b8; font-weight: 500; }
    .submit-btn { padding: 16px 28px; border-radius: 12px; width: auto; } 

    .empty-sidebar {
        background: #ffffff; border: 2px dashed #cbd5e1; border-radius: 16px;
        padding: 80px 30px; text-align: center; color: #64748b;
    }
    .empty-icon { width: 64px; height: 64px; margin: 0 auto 16px auto; color: #94a3b8; }
    .empty-title { font-size: 1.25rem; font-weight: 800; color: #475569; margin: 0 0 8px 0; }
    .empty-subtitle { font-size: 0.95rem; line-height: 1.5; margin: 0; font-weight: 500; }

    @media (max-width: 1024px) {
        .main-content-split { grid-template-columns: 1fr; }
        .sidebar-wrapper { position: static; margin-top: 24px; }
    }
</style>