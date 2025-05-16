<template>
  <v-app class="text-class">
    <v-app-bar color="primary" :elevation="2">
      <v-app-bar-title class="text-class"> CLASSIC MAFIA </v-app-bar-title>
      <template #append>
        <v-btn color="text" @click="navigateTo('/')">Home</v-btn>
        <div v-if="access_token === ''">
          <v-btn color="text" @click="navigateTo('/LogIn')">Log in</v-btn>
          <v-btn color="text" @click="navigateTo('/SignUp')">Sign up</v-btn>
        </div>
        <div v-else>
          <v-btn color="text" @click="logOut">Log out</v-btn>
        </div>
      </template>
    </v-app-bar>
    <v-main class="custom-main" color="background">
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
  import { useRouter } from 'vue-router'
  import { useAppStore } from "@/stores/app.ts";
  import { ApiClient } from '@/domain/api-client.js';

  const store = useAppStore();
  const access_token = computed(() => store.access_token);

  const api = new ApiClient();
  const router = useRouter();

  const navigateTo = (path: string) => {
    router.push(path)
  }

  const logOut = () => {
    api.logout()
    router.push('/LogIn')
  }

  onMounted(async () => {
    await api.updateToken();
  })
</script>


<style>
.text-class {
  font-family: 'Poppins', sans-serif;
  color: rgb(var(--v-theme-text));
}
.custom-main {
  padding-top: 0 !important;
}
</style>
