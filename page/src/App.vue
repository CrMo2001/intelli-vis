<script setup lang="ts">
import { ref } from 'vue'
import { test } from './api/test'
const response = ref('')

test({ key: 'hello world' }).then((res) => {
  response.value = res.data
}).catch((err) => {
  console.error(err)
})

</script>

<template>
  <h1>Hello world</h1>
  <p>{{ response }}</p>
</template>

<style scoped></style>
