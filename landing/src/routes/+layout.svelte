<script lang="ts">
    import { ClerkProvider } from 'svelte-clerk';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import '../app.css';
    
    let { children } = $props();
    
    let isChecking = $state(true);

    onMount(() => {
        const currentPath = $page.url.pathname;
        
        // For now, we still check localStorage for the specific 'admin' or 'employee' role
        const userRole = localStorage.getItem('userRole'); 

        // 1. PUBLIC ROUTES (Now ONLY /login is allowed without a role)
        if (!userRole && currentPath !== '/login') {
            console.log("Access Denied: Redirecting to Login");
            goto('/login');
        } 
        
        // 2. EMPLOYEE SECURITY (Keep drivers out of the admin command center)
        else if (userRole === 'employee' && currentPath.startsWith('/admin')) {
            console.log("Unauthorized: Redirecting Driver to Marketplace");
            goto('/jobs');
        } 
        
        // 3. ROOT REDIRECTION (If they type exactly localhost:5173/)
        else if (currentPath === '/') {
            if (userRole === 'admin') {
                goto('/admin');
            } else if (userRole === 'employee') {
                goto('/jobs');
            } else {
                goto('/login');
            }
        }

        // Allow the app to render once routing checks are complete
        isChecking = false;
    });
</script>

<ClerkProvider>
    {#if !isChecking}
        {@render children()}
    {:else}
        <div class="auth-loader">Authenticating Route...</div>
    {/if}
</ClerkProvider>

<style>
    /* Keeps the background dark while checking routes so it doesn't flash white */
    :global(body) {
        margin: 0;
        padding: 0;
        background-color: #0f172a; 
    }
    
    .auth-loader {
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #3b82f6;
        font-family: system-ui, sans-serif;
        font-weight: 600;
        background-color: #0f172a;
    }
</style>