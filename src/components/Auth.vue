<template>
  <v-container>
    <v-layout align-center justify-center>
      <h1 class="auth-title">COMPU-FEED</h1>
    </v-layout>
    <v-card class="mx-auto" max-width="400">
      <v-card-title>
        Login
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col>
            <v-text-field label="username" v-model="username"></v-text-field>
          </v-col>

          <v-col>
            <v-text-field
              v-model="password"
              v-on:keyup.enter="authenticate"
              type="password"
              label="password"
            ></v-text-field>
          </v-col>
        </v-row>
        <span style="color: red">
          {{ errorMessage }}
        </span>
      </v-card-text>
      <v-card-actions>
        <v-layout align-center justify-center>
          <v-btn rounded color="secondary" @click="authenticate">
            Login
          </v-btn>
        </v-layout>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "Auth",

  data: () => ({
    username: "",
    password: "",
    errorMessage: "",
  }),
  methods: {
    authenticate() {
      if (this.username != "" || this.password != "") {
        let body =
          "action=auth&username=" +
          this.username.toLowerCase() +
          "&password=" +
          this.password;
        let apiUrl = process.env.VUE_APP_BACKEND_URL;
        this.axios.post(apiUrl, body).then((response) => {
          if (response.data == true) {
            this.$emit("authEvent", true);
          } else {
            this.errorMessage = "Incorrect username or password";
          }
        });
      } else {
        this.errorMessage = "Username and password cannot be blank";
      }
    },
  },
};
</script>

<style>
.page-title {
  color: #afcbff;
  font-family: "Helvetica Neue", sans-serif;
  font-size: 40px;
  font-weight: bold;
  letter-spacing: -1px;
  line-height: 1;
  text-align: center;
  margin: 20px;
}
.auth-title {
  font-family: monaco, Consolas, "Lucida Console", monospace;
  font-size: 36pt;
  padding: 40px;
  color: #afcbff;
}
</style>
