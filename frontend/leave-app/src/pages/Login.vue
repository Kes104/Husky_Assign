
<template>
  <div>
    <h2>Login</h2>
    
    <input v-model="email" placeholder="Email" /> <br />
    <input v-model="password" type="password" placeholder="Password" /> <br />

    <button
      :disabled="!email || !password"
      @click="loginUser"
    >
      Login
    </button>
  </div>
</template>

<script>
import API from '../services/api'

export default {
  data() {
    return {
      email: '',
      password: '',
    }
  },

  methods: {
    async loginUser() {
      if (!this.email || !this.password) {
        alert("Please enter email and password")
        return
      }

      try {
        const res = await API.post('/login', {
          email: this.email,
          password: this.password,
        })

        if (!res.data.status) {
          alert("Login failed")
          return
        }

        const token = res.data.token
        const userId = res.data.userId
        const role = res.data.role

        localStorage.setItem('token', token)
        localStorage.setItem('userId', userId)
        localStorage.setItem('role', role)

        if (role === 'emp') {
          this.$router.push(`/lapply/?employeeId=${userId}`)
        }
        else if (role === 'higher-emp') {
          this.$router.push('/lall')
        }

      } catch (error) {
        console.error('Login failed:', error)
        alert(error?.response?.data?.detail || 'Invalid email or password')
      }
    },
  },
}
</script>
