import { ref, onMounted } from 'vue'
import { delete_user, get_users, new_user, update_user } from '@/services/api'

export function useUsers() {
  const users = ref([])
  const userErrorRaised = ref(false)
  const userErrorMessage = ref('')

  const createUser = (user) => {
    new_user(user)
      .then((response) => {
        console.log(response.data)
        fetchUsers()
      })
      .catch((error) => handleError(error))
  }
  const fetchUsers = () => {
    get_users()
      .then((response) => {
        users.value = response.data.map(({ address, ...user }) => {
          if (address) delete address.id
          return { ...user, ...(address || {}) }
        })
      })
      .catch((error) => console.log(error.message))
  }
  const updateUser = (user) => {
    const id = user.id
    delete user.id
    update_user(id, user)
      .then((response) => {
        console.log(response.data)
        fetchUsers()
      })
      .catch((error) => console.log(error))
  }

  const deleteUser = (user_id) => {
    delete_user(user_id)
      .then((response) => {
        fetchUsers()
        console.log(response.data)
      })
      .catch((error) => console.log(error))
  }

  // const formatDate = (isoDate) => {
  //   return new Date(isoDate).toLocaleDateString('en-US', {
  //     day: '2-digit',
  //     month: '2-digit',
  //     year: 'numeric',
  //     hour: '2-digit',
  //     minute: '2-digit',
  //     second: '2-digit',
  //     timeZone: 'UTC',
  //   })
  // }

  const handleError = (error) => {
    const { response } = error
    response.data
      ? (userErrorMessage.value = response.data?.detail)
      : (userErrorMessage.value = error.message)
    userErrorRaised.value = true
    console.log(response.data?.detail)
  }

  const userErrorFalse = () => (userErrorRaised.value = false)
  onMounted(fetchUsers)

  return {
    users,
    fetchUsers,
    updateUser,
    createUser,
    userErrorRaised,
    userErrorMessage,
    userErrorFalse,
    deleteUser,
  }
}
