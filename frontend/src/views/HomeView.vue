<script setup>
import { ref } from 'vue'
import { useUsers } from '@/composables/useUsers'
import TableComponent from '@/components/TableComponent.vue'
import EditUserFormComponent from '@/components/EditUserFormComponent.vue'
import NewUserFormComponent from '@/components/NewUserFormComponent.vue'

const {
  users,
  createUser,
  updateUser,
  deleteUser,
  userErrorRaised,
  userErrorMessage,
  userErrorFalse,
} = useUsers()

const user = ref()
const dialog = ref(false)
const newUserDialog = ref(false)

const columns = ref([
  { key: 'name', label: 'Name' },
  { key: 'username', label: 'Username' },
  { key: 'email', label: 'Email' },
  { key: 'street', label: 'Street' },
  { key: 'city', label: 'city' },
  { key: 'state', label: 'state' },
  { key: 'zip_code', label: 'zipcode' },
])

const handleNewUser = (user) => createUser(user)
const handleEditUser = (user) => updateUser(user)
const handleDeleteUser = (user_id) => deleteUser(user_id)

const handleNewUserFormClose = () => {
  newUserDialog.value = false
  userErrorFalse()
}

const editUserForm = (selectedUser) => {
  user.value = selectedUser
  dialog.value = true
}
</script>

<template>
  <!-- :edit="true" :remove="true" to add actions -->

  <TableComponent
    :items="users"
    :columns="columns"
    :edit="true"
    :remove="true"
    @delete="handleDeleteUser"
    @edit="editUserForm"
    @new="newUserDialog = true"
  />

  <NewUserFormComponent
    :dialog="newUserDialog"
    @close="handleNewUserFormClose"
    @new-user="handleNewUser"
  >
    <slot v-if="userErrorRaised">{{ userErrorMessage }}</slot>
  </NewUserFormComponent>

  <EditUserFormComponent
    v-if="user && dialog"
    :user="user"
    @close="dialog = false"
    :dialog="dialog"
    @edit-user="handleEditUser"
  />
</template>
