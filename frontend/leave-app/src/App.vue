<script setup>
import NavBar from './components/NavBar.vue'
</script>

<template>
  <div id="app">
    <NavBar />
    <main class="main-content">
      <router-view />
    </main>
    <footer class="footer">
      <p>&copy; 2026 Leave Management System. All rights reserved.</p>
    </footer>
  </div>
</template>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 2rem 1rem;
}

.footer {
  background-color: #1bd80e;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}

.footer p {
  margin: 0;
}
</style>
