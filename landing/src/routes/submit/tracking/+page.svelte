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
                    jobData.trackingNumber = liveData.trackingNumber;
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
    /* Base styles */
    .wizard-section { min-height: 100vh; background: radial-gradient(circle at top, #1e293b 0%, #0f172a 100%); color: #ffffff; padding: 60px 20px; font-family: 'Inter', system-ui, sans-serif; }
    .wizard-container { max-width: 500px; margin: 0 auto; }
    .wizard-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
    .back-link { color: #94a3b8; text-decoration: none; font-weight: 500; font-size: 0.95rem; }
    .back-link:hover { color: #60a5fa; }
    .step-indicator { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; color: #cbd5e1; }
    .success-indicator { background: rgba(74, 222, 128, 0.1); border-color: rgba(74, 222, 128, 0.3); color: #4ade80; }
    
    .wizard-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; padding: 32px; backdrop-filter: blur(16px); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); }
    
    .job-header { text-align: center; margin-bottom: 24px; }
    .job-id { color: #94a3b8; font-size: 0.9rem; font-weight: 600; margin-bottom: 8px; }
    .car-name { font-size: 1.3rem; font-weight: 700; margin: 0; color: #f8fafc; }

    .divider { border: 0; height: 1px; background: rgba(255, 255, 255, 0.08); margin: 24px 0; }

    /* Visual Route Map */
    .route-map { display: flex; align-items: center; justify-content: space-between; padding: 10px 0; }
    .map-point { text-align: center; width: 100px; }
    .point-dot { width: 16px; height: 16px; border-radius: 50%; background: #334155; border: 3px solid #1e293b; margin: 0 auto 8px; z-index: 2; position: relative; }
    .point-dot.active { background: #3b82f6; box-shadow: 0 0 10px rgba(59, 130, 246, 0.5); }
    .point-label { font-weight: 600; font-size: 0.95rem; color: #f8fafc; }
    .point-sub { font-size: 0.75rem; color: #64748b; }
    
    .map-line { flex: 1; height: 4px; background: #334155; border-radius: 2px; position: relative; margin: 0 -10px 30px; }
    .line-progress { position: absolute; top: 0; left: 0; height: 100%; width: 75%; background: linear-gradient(90deg, #3b82f6, #60a5fa); border-radius: 2px; }
    .car-icon { position: absolute; top: -14px; left: 75%; transform: translateX(-50%); font-size: 1.5rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3)); }

    /* Timeline */
    .timeline { display: flex; flex-direction: column; gap: 16px; }
    .time-item { display: flex; gap: 16px; align-items: flex-start; }
    .time-dot { font-size: 1.1rem; width: 24px; text-align: center; }
    .time-content { color: #cbd5e1; font-size: 0.95rem; line-height: 1.4; padding-top: 2px; }
    .time-content strong { color: #f8fafc; }
    
    .time-item.current .time-content { color: #60a5fa; font-weight: 500; }
    .time-item.future .time-content { color: #64748b; }
    .pulse { animation: pulse-anim 2s infinite; display: inline-block; }

    /* Driver Card */
    .driver-card { background: rgba(0, 0, 0, 0.2); border-radius: 16px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.05); }
    .driver-info { display: flex; gap: 16px; align-items: center; margin-bottom: 16px; }
    .driver-avatar { font-size: 2.5rem; background: #1e293b; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; border-radius: 50%; }
    .driver-details h3 { margin: 0 0 4px 0; font-size: 1.1rem; }
    .driver-stats { font-size: 0.85rem; color: #94a3b8; }
    .stars { color: #fbbf24; letter-spacing: 2px; }

    .driver-update { background: rgba(255, 255, 255, 0.03); padding: 12px; border-radius: 8px; margin-bottom: 16px; border-left: 3px solid #60a5fa; }
    .update-time { font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; display: block; margin-bottom: 4px; }
    .driver-update p { margin: 0; font-size: 0.9rem; color: #e2e8f0; font-style: italic; }

    .driver-actions { display: flex; gap: 12px; }
    .action-btn { flex: 1; padding: 12px; border-radius: 8px; border: none; font-weight: 600; cursor: pointer; transition: background 0.2s; font-size: 0.95rem;}
    .call-btn { background: rgba(255, 255, 255, 0.1); color: white; }
    .call-btn:hover { background: rgba(255, 255, 255, 0.15); }
    .msg-btn { background: #3b82f6; color: white; }
    .msg-btn:hover { background: #2563eb; }

    @keyframes pulse-anim {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.2); opacity: 0.8; }
        100% { transform: scale(1); opacity: 1; }
    }
</style>