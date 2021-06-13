<template>
  <v-card>
    <v-data-table
      :headers="headers"
      :items="logs"
      :items-per-page="15"
      class="elevation-1"
    >
      <template v-slot:item.timestamp="{ item }">
        <span>{{ item.timestamp | formatDate }}</span>
      </template>
      <template v-slot:item.amount="{ item }">
        <span
          >{{ item.amount | decimalToFraction }}
          {{ item.amount > 1 ? "Cups" : "Cup" }}</span
        >
      </template>
      <template v-slot:no-data>
        No feeds yet
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  name: "FeedLog",

  data: () => ({
    logs: [],
    intervalId: "",
    headers: [
      {
        text: "Timestamp",
        align: "start",
        sortable: true,
        value: "timestamp",
      },
      { text: "Amount", value: "amount" },
      { text: "Trigger", value: "trigger" },
    ],
  }),
  mounted() {
    this.fetchData();
    this.intervalId = setInterval(this.fetchData, 6000);
  },
  destroyed() {
    window.clearInterval(this.intervalId);
  },
  methods: {
    authenticate() {
      if (this.username != "" || this.password != "") {
        if (this.username == "drew" && this.password == "millie") {
          this.$emit("authEvent", true);
        } else {
          this.errorMessage = "Incorrect username or password";
        }
      } else {
        this.errorMessage = "Username and password cannot be blank";
      }
    },
    fetchData() {
      let apiUrl = process.env.VUE_APP_BACKEND_URL + "?action=feed_logs";
      this.axios.get(apiUrl, {}).then((response) => {
        this.logs = response.data;
      });
    },
  },
};
</script>
