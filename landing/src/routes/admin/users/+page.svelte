<script lang="ts">
    import { onMount } from 'svelte';

    interface User {
        id: string;
        name: string;
        email: string;
        role: string;
    }

    let users = $state<User[]>([]);
    let isLoading = $state(true);
    let isUpdating = $state(false);

    // Fetch real data on page load
    onMount(async () => {
        try {
            const res = await fetch('/api/users');
            if (res.ok) users = await res.json();
        } catch (error) {
            console.error("Failed to load users", error);
        } finally {
            isLoading = false;
        }
    });

    // Call our backend PATCH route
    async function updateRole(userId: string, newRole: string) {
        isUpdating = true;
        
        try {
            const res = await fetch('/api/users', {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userId, role: newRole })
            });

            if (res.ok) {
                const userIndex = users.findIndex(u => u.id === userId);
                if (userIndex !== -1) users[userIndex].role = newRole;
            } else {
                alert("Failed to update role in database.");
            }
        } catch (error) {
            alert("Network error.");
        } finally {
            isUpdating = false;
        }
    }

    // Call our backend DELETE route
    async function deleteUser(userId: string, userName: string) {
        const confirmed = confirm(`CRITICAL WARNING: Are you sure you want to permanently delete ${userName}?`);
        if (!confirmed) return;

        isUpdating = true;
        try {
            const res = await fetch('/api/users', {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userId })
            });

            if (res.ok) {
                users = users.filter(u => u.id !== userId);
            } else {
                alert("Failed to delete user.");
            }
        } catch (error) {
            alert("Network error.");
        } finally {
            isUpdating = false;
        }
    }
</script>
<div class="admin-layout">
    <header class="admin-header">
        <div>
            <h1>User Access Management</h1>
            <p class="subtitle">Assign roles and manage system access</p>
        </div>
        <div class="header-actions">
            <a href="/admin" class="btn-back">← Back to Command Center</a>
        </div>
    </header>

    <div class="table-container">
        <table class="users-table">
            <thead>
                <tr>
                    <th>User / Email</th>
                    <th>Current Role</th>
                    <th>Change Role</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {#each users as user}
                    <tr>
                        <td>
                            <div class="user-info">
                                <span class="user-name">{user.name}</span>
                                <span class="user-email">{user.email}</span>
                            </div>
                        </td>
                        <td>
                            <span class="badge badge-{user.role}">{user.role}</span>
                        </td>
                        <td>
                            <select 
                                class="role-select" 
                                value={user.role} 
                                onchange={(e) => updateRole(user.id, (e.target as HTMLSelectElement).value)}
                                disabled={isUpdating}
                            >
                                <option value="client">Client (Default)</option>
                                <option value="employee">Employee (Driver)</option>
                                <option value="admin">Admin</option>
                            </select>
                        </td>
                        <td>
                            <button 
                                class="delete-btn" 
                                onclick={() => deleteUser(user.id, user.name)}
                                disabled={isUpdating || user.role === 'admin'} 
                                title={user.role === 'admin' ? "Cannot delete admins" : "Delete User"}
                            >
                                🗑️ Remove
                            </button>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>

        {#if users.length === 0}
            <div class="empty-state">No users found in the system.</div>
        {/if}
    </div>
</div>

<style>
    /* Premium Dark Theme Styles */
    .admin-layout { 
        padding: 40px; 
        background: #0f172a; 
        min-height: 100vh; 
        color: #f8fafc; 
        font-family: 'Inter', system-ui, sans-serif; 
    }

    .admin-header { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        margin-bottom: 40px; 
    }
    .admin-header h1 { margin: 0; font-size: 2rem; font-weight: 700; color: #ffffff; }
    .subtitle { margin: 4px 0 0 0; color: #94a3b8; font-size: 0.95rem; }

    .btn-back {
        background: #1e293b; color: #f8fafc; text-decoration: none;
        padding: 8px 16px; border-radius: 8px; font-weight: 500;
        border: 1px solid #334155; transition: all 0.2s;
    }
    .btn-back:hover { background: #334155; }

    /* Table Styles */
    .table-container {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        overflow: hidden;
    }

    .users-table {
        width: 100%;
        border-collapse: collapse;
        text-align: left;
    }

    .users-table th {
        background: #0f172a;
        padding: 16px 24px;
        color: #94a3b8;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        border-bottom: 1px solid #334155;
    }

    .users-table td {
        padding: 16px 24px;
        border-bottom: 1px solid #334155;
        vertical-align: middle;
    }

    .users-table tbody tr:last-child td { border-bottom: none; }
    .users-table tbody tr:hover { background: rgba(255, 255, 255, 0.02); }

    .user-info { display: flex; flex-direction: column; gap: 4px; }
    .user-name { font-weight: 600; color: #f1f5f9; }
    .user-email { font-size: 0.85rem; color: #64748b; }

    /* Role Badges */
    .badge { padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; display: inline-block; }
    .badge-admin { background: rgba(168, 85, 247, 0.1); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.2); }
    .badge-employee { background: rgba(56, 189, 248, 0.1); color: #7dd3fc; border: 1px solid rgba(56, 189, 248, 0.2); }
    .badge-client { background: rgba(148, 163, 184, 0.1); color: #cbd5e1; border: 1px solid rgba(148, 163, 184, 0.2); }

    /* Controls */
    .role-select {
        background: #0f172a; color: #f8fafc; border: 1px solid #334155;
        padding: 8px 12px; border-radius: 8px; outline: none;
        cursor: pointer; font-family: inherit;
    }
    .role-select:disabled { opacity: 0.5; cursor: not-allowed; }

    .delete-btn {
        background: transparent; border: 1px solid rgba(239, 68, 68, 0.3); color: #ef4444;
        padding: 8px 16px; border-radius: 8px; cursor: pointer; transition: all 0.2s;
        font-size: 0.85rem; font-weight: 600;
    }
    .delete-btn:hover:not(:disabled) { background: rgba(239, 68, 68, 0.1); border-color: #ef4444; }
    .delete-btn:disabled { opacity: 0.3; cursor: not-allowed; border-color: #334155; color: #64748b; }

    .empty-state { text-align: center; padding: 40px; color: #64748b; }
</style>
