<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <auth />
  </div>
</template>

<script>
import Auth from "../components/Auth.vue";
// @ is an alias to /src

export default {
  name: "Home",
  components: {
    Auth,
  },
};
</script>
