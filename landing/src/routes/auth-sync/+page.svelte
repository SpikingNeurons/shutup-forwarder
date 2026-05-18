<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';

    onMount(() => {
        // We use an interval to wait exactly until Clerk is fully loaded in the browser
        const checkUser = setInterval(() => {
            if (window.Clerk) {
                clearInterval(checkUser); // Stop checking!
                
                const user = window.Clerk.user;
                
                // Security check: if they somehow got here without logging in, boot them back
                if (!user) {
                    goto('/login');
                    return;
                }

                // Grab the role from the public metadata you just saved!
                const role = user.publicMetadata?.role || 'client';
                
                // The Routing Logic
                if (role === 'admin') {
                    goto('/admin');
                } else if (role === 'employee') {
                    goto('/jobs');
                } else {
                    goto('/'); // Normal clients go to the landing page
                }
            }
        }, 50); // Check every 50 milliseconds so it is lightning fast
    });
</script>

<div class="loader">
    <h2>Verifying your access level...</h2>
</div>

<style>
    .loader {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        font-family: sans-serif;
    }
</style>