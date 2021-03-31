<template>
  <v-app>
    <v-main>
      <auth @authEvent="authEvent" v-if="!isAuthenticated" />
      <feeder v-else @authEvent="authEvent" />
    </v-main>
  </v-app>
</template>

<script>
import Auth from "./components/Auth.vue";
import Feeder from "./components/Feeder";

export default {
  name: "App",

  components: {
    Feeder,
    Auth,
  },

  data: () => ({}),
  computed: {
    isAuthenticated() {
      return this.$store.state.isAuthenticated;
    },
  },
  methods: {
    authEvent(value) {
      this.$store.commit("setIsAuthenticated", value);
    },
  },
};
</script>

<style lang="scss">
.v-btn__content {
  color: #0e1c36;
  .v-icon {
    color: #afcbff !important;
  }
}
</style>
