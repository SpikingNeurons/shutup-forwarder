<script lang="ts">
    import { onMount } from 'svelte';

    // State to hold our live retrieved data
    let jobData = {
        trackingNumber: 'Loading...',
        make: 'Loading Vehicle...',
        pickup: 'Origin',
        delivery: 'Destination'
    };

    // We will keep the mock driver data for now since the MVP backend doesn't handle driver matching yet
    let driver = {
        name: 'Pieter van Dam',
        rating: 4.7,
        trips: 312,
        lastUpdate: '"Driving through Cologne, on schedule for tomorrow."'
    };

    onMount(async () => {
        // 1. Get the live job ID that we saved in the processing page
        const jobId = sessionStorage.getItem('shutup-live-job-id');

        if (jobId) {
            try {
                // 2. Fetch the exact job details from the FastAPI database
                const response = await fetch(`https://shutup-forwarder-production.up.railway.app/api/jobs/${jobId}`);
                
                if (response.ok) {
                    const result = await response.json();
                    const liveData = result.data; // The Prisma database object
                    
                    // 3. Update the UI state with the real database values
                    // FIXED: We now use `jobNumber` instead of the old trackingNumber
                    jobData.trackingNumber = `SF-${liveData.jobNumber}`;
                    jobData.make = `${liveData.make} ${liveData.model} · ${liveData.year}`;
                    
                    // Split by comma to keep the UI clean (e.g., "Amsterdam, Netherlands" -> "Amsterdam")
                    jobData.pickup = liveData.pickup.split(',')[0]; 
                    jobData.delivery = liveData.delivery.split(',')[0];
                } else {
                    console.error("Failed to load job from database");
                    jobData.trackingNumber = "Error loading tracking";
                }
            } catch (e) {
                console.error("Database connection error:", e);
                jobData.trackingNumber = "Connection offline";
            }
        } else {
            jobData.trackingNumber = "No active job found";
        }
    });
</script>

<svelte:head>
    <title>Live Tracking | ShutUP Forwarder</title>
</svelte:head>

<section class="wizard-section">
    <div class="container wizard-container">
        
        <div class="wizard-header">
            <a href="/" class="back-link">← Back to Dashboard</a>
            <div class="step-indicator success-indicator">Driver Assigned ✅</div>
        </div>

        <div class="wizard-card tracking-card">
            <div class="job-header">
                <div class="job-id">Tracking: {jobData.trackingNumber}</div>
                <h2 class="car-name">{jobData.make}</h2>
            </div>

            <div class="route-map">
                <div class="map-point">
                    <div class="point-dot active"></div>
                    <div class="point-label">{jobData.pickup}</div>
                    <div class="point-sub">(Origin)</div>
                </div>
                <div class="map-line">
                    <div class="line-progress"></div>
                    <div class="car-icon">🚗</div>
                </div>
                <div class="map-point">
                    <div class="point-dot"></div>
                    <div class="point-label">{jobData.delivery}</div>
                    <div class="point-sub">(Destination)</div>
                </div>
            </div>

            <hr class="divider" />

            <div class="timeline">
                <div class="time-item done">
                    <div class="time-dot">✅</div>
                    <div class="time-content">
                        <strong>Thu 09:00</strong> — Car collected. Photos locked.
                    </div>
                </div>
                <div class="time-item done">
                    <div class="time-dot">✅</div>
                    <div class="time-content">
                        <strong>Thu 14:00</strong> — Departed pickup region.
                    </div>
                </div>
                <div class="time-item done">
                    <div class="time-dot">✅</div>
                    <div class="time-content">
                        <strong>Fri 14:00</strong> — Crossed border.
                    </div>
                </div>
                <div class="time-item current">
                    <div class="time-dot pulse">📍</div>
                    <div class="time-content">
                        <strong>Fri 17:30</strong> — On the way
                    </div>
                </div>
                <div class="time-item future">
                    <div class="time-dot">○</div>
                    <div class="time-content">
                        <strong>Sat 09:00</strong> — Estimated delivery
                    </div>
                </div>
            </div>

            <hr class="divider" />

            <div class="driver-card">
                <div class="driver-info">
                    <div class="driver-avatar">👨‍✈️</div>
                    <div class="driver-details">
                        <h3>{driver.name}</h3>
                        <div class="driver-stats">
                            <span class="stars">★★★★☆</span> {driver.rating} · {driver.trips} trips
                        </div>
                    </div>
                </div>
                
                <div class="driver-update">
                    <span class="update-time">Last update · 2 hours ago</span>
                    <p>{driver.lastUpdate}</p>
                </div>

                <div class="driver-actions">
                    <button class="action-btn call-btn">📞 Call</button>
                    <button class="action-btn msg-btn">💬 Message</button>
                </div>
            </div>

        </div>
    </div>
</section>

<style>
    /* Premium Light Theme Styles */
    .wizard-section { 
        min-height: 100vh; 
        background: #f8fafc; /* slate-50 */
        color: #0f172a; 
        padding: 60px 20px; 
        font-family: 'Inter', system-ui, sans-serif; 
    }
    
    /* FIXED: Expanded to 600px to match the rest of the application */
    .wizard-container { max-width: 600px; margin: 0 auto; }
    
    .wizard-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
    .back-link { color: #64748b; text-decoration: none; font-weight: 600; font-size: 0.95rem; transition: color 0.2s; }
    .back-link:hover { color: #2563eb; }
    
    .step-indicator { 
        background: #ffffff; 
        border: 1px solid #cbd5e1; 
        padding: 6px 14px; 
        border-radius: 20px; 
        font-size: 0.85rem; 
        font-weight: 700; 
        color: #475569; 
        box-shadow: 0 1px 2px rgba(0,0,0,0.05); 
    }
    .success-indicator { 
        background: #dcfce7; 
        border-color: #86efac; 
        color: #16a34a; 
    }
    
    .wizard-card { 
        background: #ffffff; 
        border: 1px solid #cbd5e1; 
        border-radius: 24px; 
        padding: 40px; 
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01); 
    }
    
    .job-header { text-align: center; margin-bottom: 32px; }
    .job-id { color: #64748b; font-size: 0.95rem; font-weight: 700; margin-bottom: 8px; letter-spacing: 0.5px; text-transform: uppercase; }
    .car-name { font-size: 1.6rem; font-weight: 800; margin: 0; color: #0f172a; }

    .divider { border: 0; height: 1px; background: #e2e8f0; margin: 28px 0; }

    /* FIXED: Visual Route Map Layout */
    .route-map { 
        display: flex; 
        align-items: flex-start; /* Keeps the line at the top, not the center of the block */
        justify-content: space-between; 
        padding: 10px 0; 
    }
    .map-point { 
        text-align: center; 
        flex: 0 0 140px; /* Gives the text more room so it doesn't squish */
    }
    .point-dot { 
        width: 18px; height: 18px; border-radius: 50%; 
        background: #cbd5e1; border: 4px solid #ffffff; 
        margin: 0 auto 10px; z-index: 2; position: relative; 
    }
    .point-dot.active { background: #3b82f6; box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15); }
    .point-label { font-weight: 700; font-size: 0.95rem; color: #0f172a; line-height: 1.3; }
    .point-sub { font-size: 0.75rem; color: #64748b; font-weight: 500; margin-top: 4px; }
    
    .map-line { 
        flex: 1; 
        height: 4px; 
        background: #e2e8f0; 
        border-radius: 2px; 
        position: relative; 
        margin: 7px -20px 0; /* Pushes the line down perfectly to intersect the dots */
        z-index: 1;
    }
    .line-progress { position: absolute; top: 0; left: 0; height: 100%; width: 75%; background: linear-gradient(90deg, #3b82f6, #60a5fa); border-radius: 2px; }
    .car-icon { position: absolute; top: -14px; left: 75%; transform: translateX(-50%); font-size: 1.5rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1)); }

    /* Timeline */
    .timeline { display: flex; flex-direction: column; gap: 18px; padding: 0 10px; }
    .time-item { display: flex; gap: 16px; align-items: flex-start; }
    .time-dot { font-size: 1.1rem; width: 24px; text-align: center; }
    .time-content { color: #475569; font-size: 0.95rem; line-height: 1.4; padding-top: 2px; }
    .time-content strong { color: #0f172a; }
    
    .time-item.current .time-content { color: #2563eb; font-weight: 600; }
    .time-item.future .time-content { color: #94a3b8; }
    .pulse { animation: pulse-anim 2s infinite; display: inline-block; }

    /* Driver Card */
    .driver-card { 
        background: #f8fafc; 
        border-radius: 16px; 
        padding: 24px; 
        border: 1px solid #cbd5e1; 
    }
    .driver-info { display: flex; gap: 16px; align-items: center; margin-bottom: 20px; }
    .driver-avatar { 
        font-size: 2.5rem; background: #e2e8f0; 
        width: 64px; height: 64px; display: flex; align-items: center; 
        justify-content: center; border-radius: 50%; 
    }
    .driver-details h3 { margin: 0 0 6px 0; font-size: 1.15rem; color: #0f172a; font-weight: 800;}
    .driver-stats { font-size: 0.9rem; color: #64748b; font-weight: 600;}
    .stars { color: #f59e0b; letter-spacing: 2px; }

    .driver-update { 
        background: #ffffff; 
        padding: 16px; 
        border-radius: 10px; 
        margin-bottom: 20px; 
        border: 1px solid #e2e8f0;
        border-left: 4px solid #3b82f6; 
    }
    .update-time { font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; display: block; margin-bottom: 6px; font-weight: 700;}
    .driver-update p { margin: 0; font-size: 0.95rem; color: #334155; font-style: italic; font-weight: 500;}

    .driver-actions { display: flex; gap: 12px; }
    .action-btn { flex: 1; padding: 14px; border-radius: 10px; border: 1px solid transparent; font-weight: 700; cursor: pointer; transition: all 0.2s; font-size: 1rem;}
    
    .call-btn { background: #ffffff; border-color: #cbd5e1; color: #334155; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
    .call-btn:hover { background: #f1f5f9; border-color: #94a3b8; }
    
    .msg-btn { background: #2563eb; color: white; box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2); }
    .msg-btn:hover { background: #1d4ed8; transform: translateY(-2px); box-shadow: 0 6px 12px -2px rgba(37, 99, 235, 0.3); }

    @keyframes pulse-anim {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.2); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    @media (max-width: 600px) {
        .wizard-card { padding: 30px 20px; }
        .wizard-section { padding: 30px 15px; }
        .route-map { padding: 10px 0; }
        .map-point { flex: 0 0 100px; } /* Shrink slightly on mobile */
    }
</style>