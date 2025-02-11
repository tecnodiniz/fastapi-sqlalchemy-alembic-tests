import { ref, onMounted } from 'vue'
import { get_users, update_user } from '@/services/api'

export function useUsers() {
  const users = ref([])

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

  onMounted(fetchUsers)

  return { users, fetchUsers, updateUser }
}
