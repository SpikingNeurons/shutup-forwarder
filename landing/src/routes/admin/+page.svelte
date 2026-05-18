<script lang="ts">
    import { onMount } from 'svelte';
    import { SignOutButton } from 'svelte-clerk';

    interface Job {
        id: string;
        trackingNumber: string;
        make: string;
        model: string;
        year: number;
        pickup: string;
        delivery: string;
        status: string;
        aiIsValid: boolean;
        aiReasoning: string;
    }

    let jobs: Job[] = [];
    let isLoading = true;
    let filter = 'all'; // 'all', 'valid', 'invalid'

    async function fetchJobs() {
        isLoading = true;
        try {
            const response = await fetch('http://127.0.0.1:8000/api/jobs');
            if (response.ok) {
                const result = await response.json();
                jobs = result.data;
            }
        } catch (e) {
            console.error("Failed to fetch jobs:", e);
        } finally {
            isLoading = false;
        }
    }

    onMount(fetchJobs);

    async function deleteJob(id: string, trackingNumber: string) {
        const confirmed = confirm(`Are you sure you want to delete Job #${trackingNumber}? This cannot be undone.`);
        
        if (!confirmed) return;

        try {
            const response = await fetch(`http://127.0.0.1:8000/api/jobs/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                jobs = jobs.filter(job => job.id !== id);
                console.log(`Job ${trackingNumber} deleted successfully.`);
            } else {
                const error = await response.json();
                alert("Failed to delete: " + error.detail);
            }
        } catch (e) {
            console.error("Network error during deletion:", e);
            alert("Could not reach the server to delete the job.");
        }
    }

    // Derived list based on filters
    $: filteredJobs = jobs.filter((j: Job) => {
        if (filter === 'valid') return j.aiIsValid === true;
        if (filter === 'invalid') return j.aiIsValid === false;
        return true;
    });
</script>

<div class="admin-layout">
    <header class="admin-header">
        <div>
            <h1>Logistics Command Center</h1>
            <p class="subtitle">Overview of all incoming transport requests</p>
        </div>
        <div class="stats">
            <span class="total-badge">Total Jobs: {jobs.length}</span>
            
            <a href="/admin/users" class="users-redirect-btn">
                👥 Manage Team
            </a>

            <button on:click={fetchJobs} class="refresh-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.59-10.42l5.6 5.6"/></svg>
                Refresh
            </button>
            <div class="logout-wrapper">
                <SignOutButton redirectUrl="/login" />
            </div>
        </div>
    </header>

    <nav class="filter-bar">
        <button class:active={filter === 'all'} on:click={() => filter = 'all'}>All Jobs</button>
        <button class:active={filter === 'invalid'} on:click={() => filter = 'invalid'}>⚠️ Action Required</button>
        <button class:active={filter === 'valid'} on:click={() => filter = 'valid'}>✅ Ready for Dispatch</button>
    </nav>

    {#if isLoading}
        <div class="loader-container">
            <div class="spinner"></div>
            <p>Syncing with Database...</p>
        </div>
    {:else if filteredJobs.length === 0}
        <div class="empty-state">No jobs found for this filter.</div>
    {:else}
        <div class="job-grid">
            {#each filteredJobs as job}
                <div class="job-card" class:flagged={!job.aiIsValid}>
                    <div class="card-top">
                        <span class="tracking">#{job.trackingNumber.slice(0, 12)}...</span>
                        <span class="badge {job.aiIsValid ? 'badge-success' : 'badge-danger'}">
                            {job.aiIsValid ? 'Cleared' : 'Flagged'}
                        </span>
                    </div>

                    <div class="card-main">
                        <h3 class="vehicle-title">{job.year} {job.make} {job.model}</h3>
                        <div class="route-details">
                            <div class="route-point">📍 {job.pickup.split(',')[0]}</div>
                            <div class="route-divider">|</div>
                            <div class="route-point">🏁 {job.delivery.split(',')[0]}</div>
                        </div>
                    </div>
                    
                    <div class="ai-box">
                        <span class="ai-label">🤖 AI Analysis</span>
                        <p class="ai-text">{job.aiReasoning}</p>
                    </div>

                    <div class="card-footer">
                        <span class="system-status">{job.status}</span>
                        <div class="action-buttons">
                            <button class="delete-btn" on:click={() => deleteJob(job.id, job.trackingNumber)} title="Delete Test Data">
                                🗑️
                            </button>
                            <a href="/admin/jobs/{job.id}" class="manage-btn">Review Job</a>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {/if}
</div>

<style>
    /* Premium Dark Theme Styles */
    .admin-layout { 
        padding: 40px; 
        background: #0f172a; /* Slate 900 */
        min-height: 100vh; 
        color: #f8fafc; 
        font-family: 'Inter', system-ui, sans-serif; 
    }

    /* Header */
    .admin-header { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        margin-bottom: 30px; 
    }
    .admin-header h1 { margin: 0; font-size: 2rem; font-weight: 700; color: #ffffff; }
    .subtitle { margin: 4px 0 0 0; color: #94a3b8; font-size: 0.95rem; }
    
    .stats { display: flex; align-items: center; gap: 16px; }
    .total-badge { background: #1e293b; padding: 8px 16px; border-radius: 20px; font-size: 0.9rem; border: 1px solid #334155; }
    
    /* NEW: User Redirect Button Styles */
    .users-redirect-btn {
        display: flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #8b5cf6, #6d28d9);
        color: #ffffff;
        text-decoration: none;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 14px;
        border: 1px solid rgba(139, 92, 246, 0.5);
        transition: all 0.2s ease;
    }

    .users-redirect-btn:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #a78bfa, #7c3aed);
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
    }

    .refresh-btn { 
        display: flex; align-items: center; gap: 8px; 
        background: #3b82f6; color: white; 
        border: none; padding: 8px 16px; border-radius: 20px; 
        cursor: pointer; font-weight: 600; transition: background 0.2s; 
    }
    .refresh-btn:hover { background: #2563eb; }

    /* New Logout Wrapper Styling to match theme */
    .logout-wrapper {
        display: flex;
        align-items: center;
    }
    :global(.logout-wrapper button) {
        background: #ef4444; 
        color: white; 
        border: none; 
        padding: 8px 16px; 
        border-radius: 20px; 
        cursor: pointer; 
        font-weight: 600; 
        transition: background 0.2s;
        font-family: inherit;
        font-size: 14px;
    }
    :global(.logout-wrapper button:hover) {
        background: #dc2626;
    }

    /* Filters */
    .filter-bar { display: flex; gap: 12px; margin-bottom: 30px; border-bottom: 1px solid #1e293b; padding-bottom: 20px; }
    .filter-bar button { 
        background: transparent; border: 1px solid #334155; color: #94a3b8; 
        padding: 8px 20px; border-radius: 20px; cursor: pointer; 
        font-weight: 500; transition: all 0.2s; 
    }
    .filter-bar button:hover { background: #1e293b; color: white; }
    .filter-bar button.active { background: #3b82f6; color: white; border-color: #3b82f6; }

    /* Loading & Empty States */
    .loader-container, .empty-state { text-align: center; padding: 60px; color: #94a3b8; }
    .spinner { 
        width: 40px; height: 40px; border: 3px solid rgba(59, 130, 246, 0.3); 
        border-radius: 50%; border-top-color: #3b82f6; animation: spin 1s ease-in-out infinite; 
        margin: 0 auto 16px auto; 
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    /* Job Grid & Cards */
    .job-grid { 
        display: grid; 
        grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); 
        gap: 24px; 
    }
    
    .job-card { 
        background: #1e293b; 
        border: 1px solid #334155; 
        border-radius: 16px; 
        padding: 24px; 
        display: flex; 
        flex-direction: column; 
        gap: 20px; 
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .job-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
    }

    .job-card.flagged::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: #ef4444;
    }

    /* Card Top */
    .card-top { display: flex; justify-content: space-between; align-items: center; }
    .tracking { font-family: monospace; color: #64748b; font-size: 0.9rem; }
    
    .badge { padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
    .badge-success { background: rgba(34, 197, 94, 0.1); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.2); }
    .badge-danger { background: rgba(239, 68, 68, 0.1); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }

    /* Card Main */
    .vehicle-title { margin: 0 0 12px 0; font-size: 1.25rem; font-weight: 700; color: #f1f5f9; }
    .route-details { display: flex; flex-direction: column; gap: 6px; color: #cbd5e1; font-size: 0.9rem; }
    .route-divider { color: #475569; margin-left: 6px; font-size: 0.8rem; }

    /* AI Box */
    .ai-box { background: rgba(0, 0, 0, 0.2); border-radius: 8px; padding: 12px; border: 1px solid rgba(255, 255, 255, 0.05); }
    .ai-label { font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; display: block; margin-bottom: 6px; }
    .ai-text { margin: 0; font-size: 0.85rem; color: #94a3b8; line-height: 1.5; }

    /* Card Footer & Action Buttons */
    .card-footer { display: flex; justify-content: space-between; align-items: center; margin-top: auto; padding-top: 16px; border-top: 1px solid #334155; }
    .system-status { font-size: 0.85rem; color: #64748b; display: flex; align-items: center; gap: 6px; }
    .system-status::before { content: ''; width: 8px; height: 8px; background: #fbbf24; border-radius: 50%; display: inline-block; }
    
    .action-buttons { display: flex; gap: 8px; align-items: center; }
    
    .delete-btn {
        background: transparent; border: 1px solid rgba(239, 68, 68, 0.3); color: #ef4444;
        padding: 6px 10px; border-radius: 8px; cursor: pointer; transition: all 0.2s;
        font-size: 1rem;
    }
    .delete-btn:hover { background: rgba(239, 68, 68, 0.1); border-color: #ef4444; }

    .manage-btn { 
        background: rgba(255, 255, 255, 0.05); color: #ffffff; 
        text-decoration: none; padding: 8px 16px; border-radius: 8px; 
        font-size: 0.9rem; font-weight: 500; transition: background 0.2s; 
    }
    .manage-btn:hover { background: rgba(255, 255, 255, 0.1); }
</style>