<template>
  <v-app class="text-class">
    <v-app-bar color="primary" :elevation="2">
      <v-app-bar-title class="text-class"> MAFIA </v-app-bar-title>
      <template v-slot:append>
        <v-btn color="text"> <RouterLink to="/">Home</RouterLink></v-btn>
        <v-btn color="text"> <RouterLink to="/LogIn">Log in</RouterLink></v-btn>
        <v-btn color="text"> <RouterLink to="/SignUp">Sign up</RouterLink></v-btn>
      </template>
    </v-app-bar>
    <v-main color="background">
      <router-view />
    </v-main>
  </v-app>
</template>


<style>
.text-class {
  font-family: 'Poppins', sans-serif;
  color: rgb(var(--v-theme-text));
}
</style>
<script setup lang="ts">
</script>
