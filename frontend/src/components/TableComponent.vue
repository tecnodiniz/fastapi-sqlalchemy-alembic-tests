<script setup>
defineProps({
  columns: {
    type: Array,
    require: true,
  },
  items: {
    type: Array,
    require: true,
  },
  edit: {
    type: Boolean,
  },
  remove: {
    type: Boolean,
  },
})
defineEmits(['new', 'edit', 'delete'])
</script>
<template>
  <v-btn
    prepend-icon="mdi-plus-circle"
    variant="flat"
    color="blue"
    class="ma-2"
    @click="$emit('new')"
    >New</v-btn
  >

  <v-table class="text-center" fixed-header height="300px" theme="dark">
    <thead>
      <tr>
        <th v-for="col in columns" :key="col.key" class="text-center">{{ col.label }}</th>
        <th v-if="edit || remove">Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in items" :key="item.id">
        <td v-for="col in columns" :key="col.key">
          <slot>
            {{ item[col.key] }}
          </slot>
        </td>
        <td>
          <div class="d-flex">
            <v-btn
              v-if="edit"
              icon="mdi-pencil-circle"
              variant="plain"
              @click="$emit('edit', item)"
            >
            </v-btn>
            <v-btn
              v-if="remove"
              icon="mdi-delete-circle"
              variant="plain"
              @click="$emit('delete', item.id)"
            >
            </v-btn>
          </div>
        </td>
      </tr>
    </tbody>
  </v-table>
</template>
