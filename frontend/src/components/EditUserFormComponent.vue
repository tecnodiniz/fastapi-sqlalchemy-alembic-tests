<script setup>
import { ref, toRef } from 'vue'

const props = defineProps({
  user: {
    type: Object,
    default: () => ({}),
  },
  dialog: Boolean,
})

const dialog = toRef(props, 'dialog')
const emit = defineEmits(['edit-user', 'close'])

const form = ref({
  valid: false,
  id: props.user?.id || '',
  name: props.user?.name || '',
  email: props.user?.email || '',
  username: props.user?.username || '',
  street: props.user?.street || '',
  city: props.user?.city || '',
  state: props.user?.state || '',
  zip_code: props.user?.zip_code || '',
})

const rules = ref({
  nameRules: (value) => {
    if (!value) return 'Name is required'
    if (value?.length < 2) return 'Name must have at least 2 caracters'
    return true
  },
  required: (v) => !!v || 'Field is required',
})

const createPayload = ({ id, name, email, username, street, city, state, zip_code }) => ({
  id,
  name,
  email,
  username,
  address: {
    street,
    city,
    state,
    zip_code,
  },
})

const emitChanges = () => {
  const payload = createPayload(form.value)
  emit('edit-user', payload)
}
</script>
<template>
  <v-dialog v-model="dialog" max-width="600" persistent>
    <v-card prepend-icon="mdi-account" title="Edit User">
      <v-card-text>
        <v-form v-model="form.valid">
          <v-row dense>
            <v-col cols="12" sm="6">
              <v-text-field
                v-model="form.name"
                hint="User Name"
                label="User Name*"
                required
                :rules="[rules.nameRules]"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.email" label="Email" type="email"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.username" label="Username" type="text"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.street" label="Street" type="text"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.city" label="City" type="text"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.state" label="State" type="text"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field v-model="form.zip_code" label="Zip Code" type="text"></v-text-field>
            </v-col>
          </v-row>
        </v-form>
        <slot></slot>

        <small class="text-caption text-medium-emphasis">*indicates required field</small>
      </v-card-text>

      <v-divider></v-divider>

      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn text="Close" variant="plain" @click="$emit('close')"></v-btn>

        <v-btn
          :disabled="!form.valid"
          color="primary"
          text="Upadte"
          variant="tonal"
          @click="emitChanges"
        ></v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
