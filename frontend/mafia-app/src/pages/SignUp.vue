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
      <v-text-field
        v-model="state.repeatPassword"
        :append-inner-icon="repeatPasswordVisible ? 'mdi-eye' : 'mdi-eye-off'"
        :error-messages="v$.repeatPassword.$errors.map(e => e.$message)"
        label="Repeat password"
        required
        :type="repeatPasswordVisible ? 'text' : 'password'"
        variant="outlined"
        @click:append-inner="toggleRepeatPasswordVisibility"
      />
      <v-btn
        block
        class="my-4"
        color="primary"
        height="56"
        type="submit"
        variant="flat"
      >
        Sign up
      </v-btn>
      <v-card-text class="text-center">
        <router-link
          class="text-text d-inline-flex"
          style="text-decoration: none !important"
          to="/LogIn"
        >
          Log in now
          <v-icon icon="mdi-chevron-right" />
        </router-link>
      </v-card-text>
    </form>
  </v-card>
</template>

<script setup lang="ts">
  import { computed, reactive, ref } from 'vue';
  import { useVuelidate } from '@vuelidate/core';
  import { helpers, required, sameAs } from '@vuelidate/validators';
  import { ApiClient } from '@/domain/api-client.js';
  import { useRouter } from "vue-router";

  const api = new ApiClient();
  const initialState = {
    nickname: '',
    password: '',
    repeatPassword: '',
  };

  const state = reactive({...initialState});
  const passwordVisible = ref(false);
  const repeatPasswordVisible = ref(false);

  const rules = computed(() => ({
    nickname: { required },
    password: { required },
    repeatPassword: {
      required,
      sameAs: helpers.withMessage(
        'Passwords must match',
        sameAs(state.password)
      ),
    },
  }));

  const v$ = useVuelidate(rules, state);

  const router = useRouter();
  const handleSubmit = async () => {
    const isValid = await v$.value.$validate();
    if (isValid) {
      await registration();
      router.push('/LogIn')
    }
  };

  async function registration () {
    try {
      await api.postRegistration(state.nickname, state.password);
    }
    catch (error) {
      alert(`Error registration: ${error}`);
    }
  }

  function togglePasswordVisibility () {
    passwordVisible.value = !passwordVisible.value;
  }

  function toggleRepeatPasswordVisibility () {
    repeatPasswordVisible.value = !repeatPasswordVisible.value;
  }
</script>
