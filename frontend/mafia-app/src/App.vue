<template>
  <v-app class="text-class">
    <v-app-bar color="primary" :elevation="2">
      <v-app-bar-title class="text-class"> CLASSIC MAFIA </v-app-bar-title>
      <template #append>
        <v-btn color="text" @click="navigateTo('/')">Home</v-btn>
        <v-btn color="text" @click="navigateTo('/LogIn')">Log in</v-btn>
        <v-btn color="text" @click="navigateTo('/SignUp')">Sign up</v-btn>
      </template>
    </v-app-bar>
    <v-main color="background">
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
  import { useRouter } from 'vue-router'
  const router = useRouter()
  const navigateTo = (path: string) => {
    router.push(path)
  }
</script>


<style>
.text-class {
  font-family: 'Poppins', sans-serif;
  color: rgb(var(--v-theme-text));
}
</style>
