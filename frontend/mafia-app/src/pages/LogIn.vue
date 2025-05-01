<template>
  <v-card
    class="mx-auto pa-8 pb-8"
    elevation="8"
    max-width="448"
    rounded="lg"
  >
    <form @submit.prevent="handleSubmit">
      <v-text-field
        v-model="state.nickname"
        :counter="80"
        :error-messages="v$.nickname.$errors.map(e => e.$message)"
        label="Nickname"
        required
        variant="outlined"
      />
      <v-text-field
        v-model="state.password"
        :append-inner-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
        :error-messages="v$.password.$errors.map(e => e.$message)"
        label="Password"
        required
        :type="passwordVisible ? 'text' : 'password'"
        variant="outlined"
        @click:append-inner="togglePasswordVisibility"
      />
      <v-btn
        block
        class="my-4"
        color="primary"
        height="56"
        type="submit"
        variant="flat"
      >
        Log in
      </v-btn>
      <v-card-text class="text-center">
        <router-link
          class="text-text d-inline-flex"
          style="text-decoration: none !important"
          to="/SignUp"
        >
          Sign up now
          <v-icon icon="mdi-chevron-right" />
        </router-link>
      </v-card-text>
    </form>
  </v-card>
</template>


<script setup lang="ts">
  import { computed, reactive, ref } from 'vue';
  import { useVuelidate } from '@vuelidate/core';
  import { required } from '@vuelidate/validators';

  const initialState = {
    nickname: '',
    password: '',
  };

  const state = reactive({ ...initialState });
  const passwordVisible = ref(false);

  const rules = computed(() => ({
    nickname: {required},
    password: {required},
  }));

  const v$ = useVuelidate(rules, state);

  const handleSubmit = async () => {
    const isValid = await v$.value.$validate();
    if (isValid) {
      // Submit logic
    }
  };

  function togglePasswordVisibility () {
    passwordVisible.value = !passwordVisible.value;
  }
</script>
