<template>

  {{ players.length }}
<!--  <v-sheet-->
<!--      border="info md"-->
<!--      class="pa-6 text-white mx-auto"-->
<!--      color="#141518"-->
<!--      max-width="400"-->
<!--      rounded-->
<!--    >-->
<!--    <v-sheet-->
<!--      class="pa-1 mx-auto text-center bg-transparent"-->
<!--      max-width="200"-->
<!--      rounded="lg"-->
<!--      border="md opacity-100 double accent"-->
<!--    >-->
<!--      <h4 class="font-weight-bold text-accent">ROLE</h4>-->
<!--    </v-sheet>-->

<!--    <v-sheet-->
<!--      class="pa-1 mx-auto text-center bg-transparent border-tooltip border-opacity-100 border-double"-->
<!--      max-width="200"-->
<!--      rounded="lg"-->
<!--      border="md"-->
<!--    >-->
<!--      <h4 class="font-weight-bold text-tooltip">ROLE</h4>-->
<!--    </v-sheet>-->

<!--      <h4 class="text-h5 font-weight-bold mb-4">Your Privacy</h4>-->

<!--      <p class="mb-8">-->
<!--        This business determines the use of personal data collected on our media properties and across the internet. We may collect data that you submit to us directly or data that we collect automatically including from cookies (such as device information or IP address).-->

<!--        <br>-->
<!--        <br>-->

<!--        Please read our <a class="text-red-accent-2" href="#">Privacy Policy</a> to learn about our privacy practices or click "Your Preferences" to exercise control over your data.-->
<!--      </p>-->

<!--      <v-btn-->
<!--        class="text-none text-black"-->
<!--        color="red-accent-2"-->
<!--        size="x-large"-->
<!--        variant="outlined"-->
<!--      >-->
<!--        Your Preferences-->
<!--      </v-btn>-->

<!--  </v-sheet>-->
</template>

<script setup lang="ts">
  import { useAppStore } from '@/stores/app.ts';
  import { computed } from 'vue';

  const store = useAppStore();
  const players = computed(() => store.players);
</script>
