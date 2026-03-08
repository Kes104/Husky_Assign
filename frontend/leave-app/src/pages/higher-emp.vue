<template>
  <div class="higher-emp-dashboard">
    <h1>Manager Dashboard - Approve/Reject Leaves</h1>
    <LeaveTable :is-approver="true" />
  </div>
</template>

<script>
import LeaveTable from '../components/LeaveTable.vue'
import '../styles/Employer.css'
export default {

  components: {
    LeaveTable,
  },

  mounted() {
    const role = localStorage.getItem('role')

    if (!role) {
      this.$router.push('/login')
      return
    }

    if (role !== 'higher-emp') {
      this.$router.push('/employee')
    }
  }

}
</script>

