<script lang="ts">
    import { onMount } from 'svelte';
    import { Chat } from '@ai-sdk/svelte';

    let currentRole = $state('');
    let isChatOpen = $state(false); 

    // 1. Initialize the new Chat class (defaults to /api/chat automatically)
    const chat = new Chat({});
    
    // 2. Create a local state for the input field
    let input = $state('');

    // 3. Create a manual submit handler
    function handleChatSubmit(event: Event) {
        event.preventDefault();
        if (!input.trim()) return;
        
        // Send the message using the new Chat class API
        chat.sendMessage({ text: input });
        input = ''; // Clear the input field
    }

    onMount(() => {
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

                <button 
                    onclick={() => isChatOpen = !isChatOpen}
                    class="bg-gradient-to-r from-slate-900 to-indigo-950 text-white font-semibold py-3 px-6 rounded-lg shadow-md hover:opacity-90 transition-opacity flex items-center gap-2"
                >
                    🤖 Test AI Agent
                </button>
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

{#if isChatOpen}
    <div class="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex justify-end">
        <button class="absolute inset-0 cursor-default bg-transparent border-none w-full h-full" onclick={() => isChatOpen = false} aria-label="Close chat"></button>
        
        <div class="relative w-full max-w-md bg-white h-full shadow-2xl flex flex-col z-10 border-l border-slate-200">
            <div class="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50">
                <div>
                    <h2 class="font-bold text-slate-900 text-lg flex items-center gap-2">🤖 ShutUP Agent</h2>
                    <p class="text-xs text-slate-500">Testing Hybrid Architecture Tool-Calling</p>
                </div>
                <button onclick={() => isChatOpen = false} class="text-slate-400 hover:text-slate-600 text-xl font-bold p-1">&times;</button>
            </div>
<div class="flex-1 p-4 overflow-y-auto space-y-4 bg-slate-50/50">
                {#if chat.messages.length === 0}
                    <div class="text-center text-sm text-slate-400 my-8 px-4">
                        Ask the agent to query the database or find the vector we pushed in our Python backend test!
                    </div>
                {/if}

                {#each chat.messages as message}
                    <div class="flex flex-col">
                        <span class="text-[10px] font-bold tracking-wider text-slate-400 uppercase mb-1 {message.role === 'user' ? 'self-end' : 'self-start'}">
                            {message.role}
                        </span>
                        
                        {#if message.role === 'user'}
                            <div class="bg-blue-600 text-white px-4 py-2.5 rounded-2xl rounded-tr-none max-w-[85%] self-end shadow-sm text-sm">
                                {#each message.parts as part}
                                    {#if part.type === 'text'}
                                        {part.text}
                                    {/if}
                                {/each}
                            </div>
                        {:else}
                            <div class="bg-white border border-slate-200 text-slate-800 px-4 py-2.5 rounded-2xl rounded-tl-none max-w-[85%] self-start shadow-sm text-sm">
                                {#each message.parts as part}
                                    {#if part.type === 'text'}
                                        <p class="leading-relaxed mb-2 last:mb-0">{part.text}</p>
                                    {:else if part.type.startsWith('tool-')}
                                        <div class="mt-2 text-[11px] bg-amber-50 border border-amber-200 text-amber-800 p-2 rounded-lg font-mono flex items-center gap-1.5">
                                            <span class="animate-pulse">⚡</span> Tool Call: {part.type.replace('tool-', '')}
                                        </div>
                                    {/if}
                                {/each}
                            </div>
                        {/if}
                    </div>
                {/each}
            </div>
            <form onsubmit={handleChatSubmit} class="p-4 border-t border-slate-100 bg-white flex gap-2">
                <input 
                    bind:value={input} 
                    placeholder="Ask about the test vector..." 
                    class="flex-1 border border-slate-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-blue-600 transition-colors" 
                />
                <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2.5 rounded-xl font-semibold text-sm transition-colors shadow-sm">
                    Send
                </button>
            </form>
        </div>
    </div>
{/if}

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