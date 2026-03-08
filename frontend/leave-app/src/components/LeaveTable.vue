<template>
  <div class="leave-table-container">
    <h2>Leave Requests</h2>

    <div v-if="filteredLeaves.length === 0" class="no-data">
      <p>No pending leave requests found.</p>
    </div>

    <table v-else class="leave-table">
      <thead>
        <tr>
          <th v-if="isApprover">Employee Name</th>
          <th>Leave Type</th>
          <th>Start Date</th>
          <th>End Date</th>
          <th>Reason</th>
          <th>Status</th>
          <th v-if="isApprover">Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="leave in filteredLeaves" :key="leave._id">
          <td v-if="isApprover">{{ leave.employeeName }}</td>

          <td>{{ leave.leaveType }}</td>
          <td>{{ formatDate(leave.startDate) }}</td>
          <td>{{ formatDate(leave.endDate) }}</td>
          <td>{{ leave.reason }}</td>

          <td>
            <span class="status" :class="getStatusClass(leave.status)">
              {{ leave.status }}
            </span>
          </td>

          <td v-if="canApproveReject" class="actions">
            <button
              @click="approve(leave._id)"
              class="approve-btn"
            >
              Approve
            </button>

            <button
              @click="reject(leave._id)"
              class="reject-btn"
            >
              Reject
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-if="message" class="message" :class="messageType">{{ message }}</p>
  </div>
</template>

<script>
import API from '../services/api'

export default {
  props: {
    isApprover: {
      type: Boolean,
      default: false,
    },
  },

  emits: ['leave-updated'],

  data() {
    return {
      leaves: [],
      message: '',
      messageType: 'success',
    }
  },

  computed: {
    canApproveReject() {
      return this.isApprover
    },

    // Only show pending leaves
    filteredLeaves() {
      return this.leaves.filter(l => l.status === 'pending')
    },
  },

  async mounted() {
    await this.fetchLeaves()
  },

  methods: {
    async fetchLeaves() {
      try {
        const employeeId = localStorage.getItem('userId')
        const role = localStorage.getItem('role')

        if (!employeeId || !role) {
          this.$router.push('/login')
          return
        }

        if (role === 'emp') {
          const response = await API.get(`/lapply/${employeeId}`)
          this.leaves = response.data
        } else {
          const response = await API.get('/lall')
          this.leaves = response.data
        }

      } catch (error) {
        this.message = error?.response?.data?.detail || 'Failed to fetch leaves'
        this.messageType = 'error'
      }
    },

    async approve(leaveId) {
      try {
        await API.patch(`/approve/${leaveId}`)

        this.message = 'Leave approved successfully'
        this.messageType = 'success'

        await this.fetchLeaves()

        this.$emit('leave-updated')

      } catch (error) {
        this.message = error?.response?.data?.detail || 'Failed to approve leave'
        this.messageType = 'error'
      }
    },

    async reject(leaveId) {
      try {
        await API.patch(`/reject/${leaveId}`)

        this.message = 'Leave rejected successfully'
        this.messageType = 'success'

        await this.fetchLeaves()

        this.$emit('leave-updated')

      } catch (error) {
        this.message = error?.response?.data?.detail || 'Failed to reject leave'
        this.messageType = 'error'
      }
    },

    formatDate(date) {
      if (!date) return 'N/A'

      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      })
    },

    getStatusClass(status) {
      return status ? status.toLowerCase() : ''
    },
  },
}
</script>
