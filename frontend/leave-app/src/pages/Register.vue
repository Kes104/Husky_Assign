<template>
  <div>
    <h2>Register</h2>

    <input v-model="name" placeholder="Name" /> <br />
    <input v-model="email" placeholder="Email" /> <br />
    <input v-model="password" type="password" placeholder="Password" /> <br />

    <select v-model="role">
      <option disabled value="">Select Role</option>
      <option value="emp">Employee</option>
      <option value="higher-emp">Higher Employee</option>
    </select> <br />

    <button :disabled="!name || !email || !password || !role" @click="registerUser">
      Register
    </button>
  </div>
</template>

<script>
import API from '../services/api'

export default {
  data() {
    return {
      name: '',
      email: '',
      password: '',
      role: '',
    }
  },

  methods: {
    async registerUser() {

      if (!this.role) {
        alert("Please select a role")
        return
      }

      try {
        const res = await API.post('/register', {
          name: this.name,
          email: this.email,
          password: this.password,
          role: this.role,
        })

        if (!res.data.status) {
          alert("Registration failed")
          return
        }

        const userId = res.data.userId
        const role = res.data.role

        localStorage.setItem('userId', userId)
        localStorage.setItem('role', role)

        if (role === 'emp') {
          this.$router.push(`/lapply?employeeId=${userId}`)
        } 
        else if (role === 'higher-emp') {
          this.$router.push('/lall')
        }

      } catch (error) {
        console.error('Registration failed:', error)
        alert(error?.response?.data?.detail || 'Registration failed')
      }
    },
  },
}
</script>

