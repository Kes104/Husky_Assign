<template>
  <div class="leave-form-container">
    <h2>Apply for Leave</h2>

    <form @submit.prevent="submitForm" class="form">

      <div class="form-group">
        <label for="leaveType">Leave Type:</label>
        <select v-model="form.leaveType" id="leaveType" required>
          <option value="">Select Leave Type</option>
          <option value="Sick">Sick Leave</option>
          <option value="Casual">Casual Leave</option>
          <option value="Annual">Annual Leave</option>
          <option value="Maternity">Maternity Leave</option>
          <option value="Other">Other</option>
        </select>
      </div>

      <div class="form-group">
        <label for="startDate">Start Date:</label>
        <input v-model="form.startDate" id="startDate" type="date" required />
      </div>

      <div class="form-group">
        <label for="endDate">End Date:</label>
        <input v-model="form.endDate" id="endDate" type="date" required />
      </div>

      <div class="form-group">
        <label for="reason">Reason:</label>
        <textarea v-model="form.reason" id="reason" rows="4" required></textarea>
      </div>

      <button
        type="submit"
        class="submit-btn"
        :disabled="loading"
      >
        {{ loading ? "Submitting..." : "Submit Application" }}
      </button>

      <p v-if="message" class="message" :class="messageType">
        {{ message }}
      </p>

    </form>
  </div>
</template>

<script>
import API from '../services/api'

export default {

  emits: ['leave-applied'],

  data() {
    return {
      loading: false,

      form: {
        leaveType: '',
        startDate: '',
        endDate: '',
        reason: '',
      },

      message: '',
      messageType: 'success',
    }
  },

  methods: {

    async submitForm() {

      const employeeId = localStorage.getItem('userId')
      const role = localStorage.getItem('role')

      if (!employeeId || !role) {
        this.$router.push('/login')
        return
      }

      if (role !== 'emp') {
        this.message = 'Only employees can apply for leave'
        this.messageType = 'error'
        return
      }

      if (new Date(this.form.startDate) > new Date(this.form.endDate)) {
        this.message = 'End date must be after start date'
        this.messageType = 'error'
        return
      }

      try {

        this.loading = true

        await API.post(`/lapply?employeeId=${employeeId}`, {
          leaveType: this.form.leaveType,
          startDate: this.form.startDate,
          endDate: this.form.endDate,
          reason: this.form.reason,
        })

        this.message = 'Leave application submitted successfully!'
        this.messageType = 'success'

        this.resetForm()

        this.$emit('leave-applied')

      } catch (error) {

        this.message =
          error?.response?.data?.detail ||
          'Failed to submit leave application'

        this.messageType = 'error'

      } finally {

        this.loading = false

      }
    },

    resetForm() {

      this.form = {
        leaveType: '',
        startDate: '',
        endDate: '',
        reason: '',
      }

    }

  }
}
</script>
