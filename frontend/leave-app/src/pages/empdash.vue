<template>
  <div class="employee-dashboard">
    <h1>Employee Dashboard</h1>

    <div class="content-wrapper">
      <LeaveForm @leave-applied="refreshLeaves" />
      <LeaveTable
        :is-approver="false"
        @leave-updated="refreshLeaves"
        ref="leaveTable"
      />
    </div>

  </div>
</template>

<script>
import LeaveForm from '../components/LeaveForm.vue'
import LeaveTable from '../components/LeaveTable.vue'
import '../styles/Employee.css'
export default {

  components: {
    LeaveForm,
    LeaveTable,
  },

  mounted() {

    const role = localStorage.getItem('role')

    if (!role) {
      this.$router.push('/login')
      return
    }

    if (role !== 'emp') {
      this.$router.push('/lall')
    }

  },

  methods: {

    refreshLeaves() {
      if (this.$refs.leaveTable) {
        this.$refs.leaveTable.fetchLeaves()
      }
    }

  }

}
</script>
