<template>
  <nav class="navbar">
    <div class="navbar-container">
      <h1 class="navbar-brand">Leave Management System</h1>

      <ul class="navbar-menu">

        <li v-if="!isLoggedIn">
          <router-link to="/login">Login</router-link>
        </li>

        <li v-if="!isLoggedIn">
          <router-link to="/register">Register</router-link>
        </li>

        <li v-if="isLoggedIn">
          <span class="user-info">{{ userRole }}</span>
        </li>

        <li v-if="isLoggedIn">
          <button @click="logout" class="logout-btn">
            Logout
          </button>
        </li>

      </ul>
    </div>
  </nav>
</template>

<script>
import '../styles/NBstyle.css'

export default {
  data() {
    return {
      isLoggedIn: false,
      userRole: '',
    }
  },

  mounted() {
    this.checkLoginStatus()
  },

  methods: {

    checkLoginStatus() {
      const token = localStorage.getItem('token')
      const role = localStorage.getItem('role')

      this.isLoggedIn = !!token
      this.userRole = role ? role.toUpperCase() : ''
    },

    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('userId')
      localStorage.removeItem('role')

      this.isLoggedIn = false
      this.userRole = ''

      this.$router.push('/login')
    }

  }
}
</script>