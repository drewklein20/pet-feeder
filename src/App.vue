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
import _ from "lodash";

export default {
  name: "App",

  components: {
    Feeder,
    Auth,
  },

  data: () => ({
    feederId: 1,
    settings: null,
  }),
  mounted() {
    this.fetchData();
  },
  computed: {
    isAuthenticated() {
      return this.$store.state.isAuthenticated || (!_.isNil(this.settings) && this.settings.isUsingAuthentication == false)
    },
  },
  methods: {
    authEvent(value) {
      this.$store.commit("setIsAuthenticated", value);
    },
    fetchData() {
      let apiUrl =
        process.env.VUE_APP_BACKEND_URL +
        "?action=feeder_settings&id=" +
        this.feederId;
      this.axios.get(apiUrl, {}).then((response) => {
        this.settings = JSON.parse(response.data[0].preferences);
      });
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
