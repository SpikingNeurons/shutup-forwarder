<script lang="ts">
    import { SignIn } from 'svelte-clerk';
</script>

<div class="login-wrapper">
    <SignIn forceRedirectUrl="/auth-sync" />
</div>

<style>
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background-color: #f3f4f6; 
    }
</style>