<script lang="ts">
    import { onMount } from 'svelte';

    let currentRole = $state('');

    onMount(() => {
        // The forced 'admin' override has been completely removed.
        // Now it strictly reads whatever your actual login session provides.
        currentRole = localStorage.getItem('userRole') || '';
    });
</script>

<div class="relative min-h-[85vh] w-full bg-white overflow-hidden flex items-center font-sans">
    
    <div class="absolute inset-0 bg-grid z-0"></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full flex flex-col lg:flex-row items-center justify-between gap-16">
        
        <div class="flex-1 max-w-2xl">
            <div class="inline-flex items-center space-x-2 bg-blue-50 text-blue-600 px-3 py-1 rounded-full text-sm font-medium mb-8 border border-blue-100">
                <span class="text-blue-500">✦</span>
                <span>Now with AI negotiation</span>
            </div>

            <h1 class="text-6xl sm:text-7xl font-extrabold text-slate-900 tracking-tight leading-[1.1] mb-2">
                Your car, <br/> transported. <br/>
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">
                    Zero stress.
                </span>
            </h1>

            <p class="mt-6 text-lg text-slate-600 leading-relaxed max-w-xl">
                Snap a photo, drop a pin. Our AI finds a verified driver, locks in the best price, and watches over your car from pickup to delivery — with a photo record that protects you if anything goes wrong.
            </p>

            <div class="mt-10 flex flex-wrap items-center gap-4">
                <a href="/submit" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center gap-2 shadow-lg shadow-blue-200 no-underline">
                    Get an instant quote &rarr;
                </a>

                {#if !currentRole}
                    <a href="/login" class="bg-white hover:bg-slate-50 text-slate-700 font-semibold py-3 px-6 rounded-lg border border-slate-200 transition-colors shadow-sm no-underline">
                        Login
                    </a>
                {:else if currentRole === 'admin'}
                    <a href="/admin" class="bg-purple-600 hover:bg-purple-500 text-white font-semibold py-3 px-6 rounded-lg shadow-sm transition-colors no-underline">
                        Command Center
                    </a>
                {:else if currentRole === 'employee'}
                    <a href="/jobs" class="bg-slate-800 hover:bg-slate-700 text-white font-semibold py-3 px-6 rounded-lg shadow-sm transition-colors no-underline">
                        Find Loads
                    </a>
                {:else}
                    <a href="/submit/tracking" class="bg-white hover:bg-slate-50 text-slate-700 font-semibold py-3 px-6 rounded-lg border border-slate-200 transition-colors shadow-sm no-underline">
                        Track My Car
                    </a>
                {/if}
            </div>

            <div class="mt-10 flex items-center gap-6 text-sm text-slate-500">
                <div class="flex items-center gap-2">
                    <span class="text-yellow-400">★★★★★</span>
                    <span>4.8 · 2,000+ transports</span>
                </div>
                <div class="w-px h-4 bg-slate-300"></div>
                <div class="flex items-center gap-2">
                    <span>📷 Photos locked at pickup</span>
                </div>
            </div>
        </div>

        <div class="flex-1 flex justify-center lg:justify-end hidden md:flex">
            <div class="bg-slate-900 rounded-[2.5rem] p-3 shadow-2xl w-80 border-8 border-slate-800 transform rotate-2 hover:rotate-0 transition-transform duration-500">
                <div class="bg-white rounded-[1.8rem] h-full w-full p-6 flex flex-col">
                    
                    <div class="text-center mb-6">
                        <span class="text-xs font-semibold text-slate-400 tracking-wider">Job #SF-4821</span>
                        <h3 class="font-bold text-lg text-slate-900 mt-1">Amsterdam &rarr; Munich</h3>
                        <p class="text-xs text-slate-500 mt-1">BMW 3 Series · 2019</p>
                    </div>

                    <div class="space-y-4 mb-8">
                        <div class="flex items-start gap-3">
                            <div class="w-5 h-5 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center text-xs mt-0.5">✓</div>
                            <div>
                                <p class="text-sm font-semibold text-emerald-600">Car collected</p>
                                <p class="text-xs text-slate-400">Thu 09:00</p>
                            </div>
                        </div>
                        <div class="flex items-start gap-3">
                            <div class="w-5 h-5 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center text-xs mt-0.5">✓</div>
                            <div>
                                <p class="text-sm font-semibold text-emerald-600">Departed Netherlands</p>
                            </div>
                        </div>
                        <div class="flex items-start gap-3">
                            <div class="w-5 h-5 rounded-full bg-blue-100 flex items-center justify-center mt-0.5 relative">
                                <div class="w-2 h-2 rounded-full bg-blue-600"></div>
                                <div class="absolute w-2 h-2 rounded-full bg-blue-600 animate-ping"></div>
                            </div>
                            <div>
                                <p class="text-sm font-semibold text-blue-600">Cologne — on schedule</p>
                            </div>
                        </div>
                        <div class="flex items-start gap-3">
                            <div class="w-5 h-5 rounded-full border-2 border-slate-200 flex items-center justify-center mt-0.5"></div>
                            <div>
                                <p class="text-sm font-medium text-slate-400">Munich</p>
                                <p class="text-xs text-slate-400">Est. Sat 09:00</p>
                            </div>
                        </div>
                    </div>

                    <div class="mt-auto border-t border-slate-100 pt-4">
                        <div class="flex justify-between items-center mb-4">
                            <div class="flex items-center gap-2">
                                <div class="w-8 h-8 rounded-full bg-slate-200 overflow-hidden text-2xl flex items-center justify-center">🚐</div>
                                <span class="text-sm font-semibold">Pieter van Dam</span>
                            </div>
                            <span class="text-xs font-bold text-slate-700">★ 4.7</span>
                        </div>
                        <div class="flex gap-2">
                            <button class="flex-1 bg-white border border-slate-200 rounded-lg py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 transition-colors">📞 Call</button>
                            <button class="flex-1 bg-emerald-50 border border-emerald-100 rounded-lg py-2 text-sm font-semibold text-emerald-700 hover:bg-emerald-100 transition-colors">💬 Message</button>
                        </div>
                    </div>

                </div>
            </div>
        </div>

    </div>
</div>

<style>
    .bg-grid {
        background-size: 40px 40px;
        background-image: 
            linear-gradient(to right, rgba(226, 232, 240, 0.6) 1px, transparent 1px), 
            linear-gradient(to bottom, rgba(226, 232, 240, 0.6) 1px, transparent 1px);
        mask-image: linear-gradient(to bottom, black 40%, transparent 100%);
        -webkit-mask-image: linear-gradient(to bottom, black 40%, transparent 100%);
    }
</style>