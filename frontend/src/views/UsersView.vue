<script setup>
import { ref } from 'vue'
import { useUsers } from '@/composables/useUsers'
import TableComponent from '@/components/TableComponent.vue'

const { users } = useUsers()
const columns = ref([
  { key: 'name', label: 'Name' },
  { key: 'username', label: 'Username' },
  { key: 'email', label: 'Email' },
  { key: 'street', label: 'Street' },
  { key: 'city', label: 'city' },
  { key: 'state', label: 'state' },
  { key: 'zip_code', label: 'zipcode' },
])
</script>

<template>
  <TableComponent :items="users" :columns="columns" />
</template>
