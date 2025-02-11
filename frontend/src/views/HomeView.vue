<script setup>
import { ref } from 'vue'
import { useUsers } from '@/composables/useUsers'
import TableComponent from '@/components/TableComponent.vue'
import EditUserFormComponent from '@/components/EditUserFormComponent.vue'

const { users, updateUser } = useUsers()
const user = ref()
const dialog = ref(false)

const columns = ref([
  { key: 'name', label: 'Name' },
  { key: 'username', label: 'Username' },
  { key: 'email', label: 'Email' },
  { key: 'street', label: 'Street' },
  { key: 'city', label: 'city' },
  { key: 'state', label: 'state' },
  { key: 'zip_code', label: 'zipcode' },
])

const userEditForm = (selectedUser) => {
  user.value = selectedUser
  dialog.value = true
}
const handleUserEdit = (user) => {
  updateUser(user)
}
</script>

<template>
  <!-- :edit="true" :remove="true" to add actions -->
  <TableComponent :items="users" :columns="columns" :edit="true" @edit="userEditForm" />

  <EditUserFormComponent
    v-if="user && dialog"
    :user="user"
    @close="dialog = false"
    :dialog="dialog"
    @edit-user="handleUserEdit"
  />
</template>
