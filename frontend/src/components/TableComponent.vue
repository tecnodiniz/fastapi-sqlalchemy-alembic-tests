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
defineEmits(['edit'])
</script>
<template>
  <v-table class="text-center">
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
            <v-btn v-if="remove" icon="mdi-delete-circle" variant="plain"> </v-btn>
          </div>
        </td>
      </tr>
    </tbody>
  </v-table>
</template>
