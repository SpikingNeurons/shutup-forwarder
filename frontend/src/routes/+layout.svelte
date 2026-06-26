<script lang="ts">
    import { ClerkProvider, UserButton } from 'svelte-clerk';
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import '../app.css';
    
    let { children } = $props();
    
    let isChecking = $state(true);
    let currentRole = $state('');

    // 1. Read memory on initial load
    onMount(() => {
        currentRole = localStorage.getItem('userRole') || ''; 
        isChecking = false;
    });

    // 2. THE SECURITY GUARD: $effect runs automatically whenever the URL changes!
    $effect(() => {
        if (isChecking) return; 

        const currentPath = $page.url.pathname;

        // PUBLIC ROUTES 
        const isPublicRoute = currentPath === '/' || 
                              currentPath.startsWith('/login') || 
                              currentPath.startsWith('/signup') || 
                              currentPath.startsWith('/driver-apply') || 
                              currentPath.startsWith('/auth-sync');

        if (!currentRole && !isPublicRoute) {
            goto('/login');
        } 
        // SECURITY: Keep drivers out of admin pages
        else if (currentRole === 'FORWARDER' && currentPath.startsWith('/admin')) {
            goto('/');
        } 
        
    });

    // 3. CLEAN SVELTE 5 DERIVED VARIABLES
    let isAdminPath = $derived($page.url.pathname.startsWith('/admin'));

    let navLinks = $derived(() => {
        if (isAdminPath) return []; 
        
        if (!currentRole) return []; 

        if (currentRole === 'admin') {
            return [];
        } else if (currentRole === 'FORWARDER') {
            return [
                { name: 'Available Loads', href: '/jobs' },
                { name: 'My Deliveries', href: '/jobs/active' }
            ];
        } else {
            return [
                { name: 'Book a Service', href: '/submit' },
                { name: 'My Current Jobs', href: '/submit/tracking' } 
            ];
        }
    });

    let displayRole = $derived(() => {
        if (isAdminPath) return 'ADMIN';
        if (currentRole === 'FORWARDER') return 'DRIVER'; 
        return currentRole || 'Guest';
    });
</script>

<ClerkProvider>
    {#if !isChecking}
        
        {#if $page.url.pathname === '/'}
            
            {@render children()}
            
        {:else}
            
            <div class="min-h-screen bg-slate-50 flex flex-col font-sans">
                
                {#if !$page.url.pathname.startsWith('/login') && !$page.url.pathname.startsWith('/signup') && !$page.url.pathname.startsWith('/driver-apply') && !$page.url.pathname.startsWith('/auth-sync')}
                    <header class="bg-slate-900 text-white shadow-md sticky top-0 z-50">
                        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                            <div class="flex items-center justify-between h-16">
                                
                                <div class="flex items-center space-x-4">
                                    <span class="font-bold text-xl tracking-wider text-blue-400">
                                        SHUTUP FORWARDER
                                    </span>
                                </div>

                                <nav class="hidden md:flex space-x-8">
                                    {#each navLinks() as link}
                                        <a 
                                            href={link.href} 
                                            class="text-sm font-medium transition-colors hover:text-blue-400 
                                                   {$page.url.pathname.includes(link.href) ? 'text-blue-400 border-b-2 border-blue-400 pb-1' : 'text-slate-300'}"
                                        >
                                            {link.name}
                                        </a>
                                    {/each}
                                </nav>

                                <div class="flex items-center space-x-4">
                                    {#if currentRole}
                                        <span class="text-xs uppercase tracking-widest text-slate-400 bg-slate-800 px-2 py-1 rounded-md">
                                            {displayRole()}
                                        </span>
        
                                        <!-- UPDATED: Points directly to the central dashboard hub -->
                                        <a 
                                            href="/" 
                                            class="bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-sm font-semibold py-2 px-4 rounded-md border border-slate-700 transition-colors no-underline"
                                        >
                                            Dashboard
                                        </a>

                                        <div class="bg-white rounded-full flex items-center justify-center p-0.5 ml-2">
                                            <UserButton />
                                        </div>

                                    {:else}
                                        <a 
                                            href="/login" 
                                            class="bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold py-2 px-4 rounded-md transition-colors no-underline"
                                        >
                                            Sign In
                                        </a>
                                    {/if}
                                </div>

                            </div>
                        </div>
                    </header>
                {/if}

                <main class="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    {@render children()}
                </main>

            </div>
            
        {/if}
        
    {:else}
        <div class="h-screen bg-slate-50"></div>
    {/if}
</ClerkProvider>