<script lang="ts">
    import { goto } from '$app/navigation';

    // Track the status using simple strings instead of massive Base64 data
    let photos = $state({
        front: '',
        rear: '',
        left: '',
        right: '',
        interior: '',
        odometer: ''
    });

    // We keep these for the UI, but we won't hardcode the AI note anymore
    let isScanning = $state(false);
    let aiNote = $state('Mock Mode: Image evaluation bypassed.');

    // DUMMY UPLOAD FUNCTION - No file reading, no Base64 processing!
    function handleDummyUpload(part: keyof typeof photos) {
        // We instantly set a fake string so the UI knows it's "done"
        photos[part] = 'mock_image_data';

        // Show a brief scanning animation just for UI feel
        if (part === 'front') {
            isScanning = true;
            setTimeout(() => {
                isScanning = false;
            }, 800);
        }
    }

    // Check if all photos have our dummy string
    let allDone = $derived(Object.values(photos).every(data => data !== ''));

    function handleNext() {
        if (!allDone) {
            alert("Please mock all required photos before proceeding.");
            return;
        }
        
        // NOW we are saving tiny mock strings to sessionStorage! 
        // This will pass cleanly to your backend without crashing the token limit.
        sessionStorage.setItem('shutup-step2-photos', JSON.stringify({ 
            completed: true, 
            images: photos 
        }));
        
        goto('/submit/route');
    }
</script>

<svelte:head>
    <title>Step 2: Photos | ShutUP Forwarder</title>
</svelte:head>

<section class="wizard-section">
    <div class="container wizard-container">
        <div class="wizard-header">
            <a href="/submit" class="back-link">← Back to Vehicle</a>
            <div class="step-indicator">Step 2 of 5</div>
        </div>

        <div class="wizard-card">
            <h1 class="wizard-title">Vehicle Condition</h1>
            <p class="wizard-sub">Upload module disabled per Praveen's instructions. Click below to mock the uploads.</p>

            <div class="photo-grid">
                <div class="photo-slot" class:completed={photos.front !== ''}>
                    <div class="slot-label">FRONT</div>
                    {#if photos.front !== ''}
                        <div class="status-done">✅ Image Mocked</div>
                    {:else}
                        <button class="upload-btn" onclick={() => handleDummyUpload('front')}>
                            📷 Mock Upload
                        </button>
                    {/if}
                </div>

                <div class="photo-slot" class:completed={photos.rear !== ''}>
                    <div class="slot-label">REAR</div>
                    {#if photos.rear !== ''}
                        <div class="status-done">✅ Image Mocked</div>
                    {:else}
                        <button class="upload-btn" onclick={() => handleDummyUpload('rear')}>
                            📷 Mock Upload
                        </button>
                    {/if}
                </div>

                <div class="photo-slot" class:completed={photos.left !== ''}>
                    <div class="slot-label">LEFT SIDE</div>
                    {#if photos.left !== ''}
                        <div class="status-done">✅ Image Mocked</div>
                    {:else}
                        <button class="upload-btn" onclick={() => handleDummyUpload('left')}>
                            📷 Mock Upload
                        </button>
                    {/if}
                </div>

                <div class="photo-slot" class:completed={photos.right !== ''}>
                    <div class="slot-label">RIGHT SIDE</div>
                    {#if photos.right !== ''}
                        <div class="status-done">✅ Image Mocked</div>
                    {:else}
                        <button class="upload-btn" onclick={() => handleDummyUpload('right')}>
                            📷 Mock Upload
                        </button>
                    {/if}
                </div>

                <div class="photo-slot" class:completed={photos.interior !== ''}>
                    <div class="slot-label">INTERIOR</div>
                    {#if photos.interior !== ''}
                        <div class="status-done">✅ Image Mocked</div>
                    {:else}
                        <button class="upload-btn" onclick={() => handleDummyUpload('interior')}>
                            📷 Mock Upload
                        </button>
                    {/if}
                </div>

                <div class="photo-slot" class:completed={photos.odometer !== ''}>
                    <div class="slot-label">ODOMETER</div>
                    {#if photos.odometer !== ''}
                        <div class="status-done">✅ Image Mocked</div>
                    {:else}
                        <button class="upload-btn" onclick={() => handleDummyUpload('odometer')}>
                            📷 Mock Upload
                        </button>
                    {/if}
                </div>
            </div>

            <div class="ai-box" class:visible={isScanning || aiNote}>
                {#if isScanning}
                    <div class="scanning-text">🤖 Bypassing AI vision processing...</div>
                {:else if aiNote}
                    <div class="ai-alert">{aiNote}</div>
                {/if}
            </div>

            <button class="submit-btn" disabled={!allDone} onclick={handleNext}>
                {allDone ? "Confirm Notes & Next →" : "Mock all photos to continue"}
            </button>
        </div>
    </div>
</section>

<style>
    /* Base styles */
    .wizard-section { min-height: 100vh; background: radial-gradient(circle at top, #1e293b 0%, #0f172a 100%); color: #ffffff; padding: 60px 20px; font-family: 'Inter', system-ui, sans-serif; }
    .wizard-container { max-width: 600px; margin: 0 auto; }
    .wizard-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
    .back-link { color: #94a3b8; text-decoration: none; font-weight: 500; font-size: 0.95rem; }
    .back-link:hover { color: #60a5fa; }
    .step-indicator { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; color: #cbd5e1; }
    
    .wizard-card { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; padding: 48px; backdrop-filter: blur(16px); box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5); }
    .wizard-title { font-size: 2.2rem; font-weight: 700; margin: 0 0 12px 0; background: linear-gradient(to right, #ffffff, #93c5fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .wizard-sub { color: #94a3b8; margin: 0 0 40px 0; font-size: 1.05rem; line-height: 1.5; }

    .photo-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px; }

    .photo-slot {
        background: rgba(0, 0, 0, 0.25); border: 1px dashed rgba(255, 255, 255, 0.2); border-radius: 12px;
        padding: 24px 16px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; transition: all 0.3s ease;
    }
    .photo-slot.completed { border-style: solid; border-color: #4ade80; background: rgba(74, 222, 128, 0.05); padding: 12px; }

    .slot-label { font-size: 0.85rem; font-weight: 600; letter-spacing: 1px; color: #94a3b8; }

    .upload-btn {
        display: inline-block; background: rgba(255, 255, 255, 0.1); border: none; color: white;
        padding: 8px 16px; border-radius: 8px; font-size: 0.9rem; cursor: pointer; transition: background 0.2s ease; text-align: center;
    }
    .upload-btn:hover { background: rgba(59, 130, 246, 0.5); }
    .status-done { color: #4ade80; font-weight: 600; font-size: 0.9rem; margin-top: 4px; text-align: center; }

    .ai-box { opacity: 0; height: 0; overflow: hidden; transition: all 0.4s ease; margin-bottom: 24px; border-radius: 12px; }
    .ai-box.visible { opacity: 1; height: auto; padding: 16px; background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); }
    .scanning-text { color: #fbbf24; font-weight: 500; animation: pulse 1.5s infinite; text-align: center;}
    .ai-alert { color: #fcd34d; font-weight: 500; line-height: 1.4; }

    @keyframes pulse { 0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; } }

    .submit-btn {
        width: 100%; padding: 18px; font-size: 1.1rem; border-radius: 12px; background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white; border: none; font-weight: 600; cursor: pointer; transition: all 0.2s ease;
    }
    .submit-btn:disabled { background: #334155; color: #94a3b8; cursor: not-allowed; box-shadow: none; }
    .submit-btn:not(:disabled):hover { transform: translateY(-2px); box-shadow: 0 10px 20px -10px rgba(37, 99, 235, 0.5); }

    @media (max-width: 600px) {
        .wizard-card { padding: 30px 20px; }
        .wizard-section { padding: 30px 15px; }
    }
</style>