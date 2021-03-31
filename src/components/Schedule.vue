<template>
  <div>
    <v-dialog transition="dialog-bottom-transition" max-width="600">
      <template v-slot:activator="{ on, attrs }">
        <v-layout align-center justify-center class="mb-4">
          <v-btn color="secondary" v-bind="attrs" v-on="on"
            >Add Scheduled Feed</v-btn
          >
        </v-layout>
      </template>
      <template v-slot:default="dialog">
        <v-card>
          <v-card-text>
            <v-row align="center" justify="center">
              <v-col>
                <v-time-picker
                  class="pt-4"
                  v-model="tempTime"
                  ampm-in-title
                ></v-time-picker>
              </v-col>
              <v-col>
                <v-spacer>
                  <v-select
                    class="pt-4"
                    v-model="tempAmount"
                    :items="amounts"
                    label="Feed Amount"
                    hint="Cups"
                    persistent-hint
                    outlined
                  ></v-select>
                </v-spacer>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-btn text color="error" @click="cancelFeed(dialog)">Cancel</v-btn>
            <v-btn
              rounded
              color="secondary"
              @click="addFeed(dialog)"
              :disabled="tempTime == '' || tempAmount == ''"
              >Add</v-btn
            >
          </v-card-actions>
        </v-card>
      </template>
    </v-dialog>

    <v-card>
      <v-simple-table>
        <template v-slot:default>
          <thead>
            <tr>
              <th class="text-left">
                Feed Time
              </th>
              <th class="text-left">
                Amount (cups)
              </th>

              <th class="text-left">
                Last updated
              </th>
              <th class="text-left"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in scheduledFeeds" :key="item.id">
              <td>{{ item.feedTime | 12Hour}}</td>
              <td>{{ item.amount }}</td>
              <td>{{ item.modified | formatDateShorter }}</td>
              <td>
                <v-btn
                  class="mx-2 trashcan"
                  fab
                  dark
                  x-small
                  color="red"
                  @click="removeScheduledFeed(item.id)"
                >
                  <v-icon dark>
                    mdi-delete
                  </v-icon>
                </v-btn>
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "Schedule",

  data: () => ({
    scheduledFeeds: [],
    intervalId: "",
    tempAmount: "",
    tempTime: "",
    amounts: [".5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"],
    scheduleResult: "",
  }),
  mounted() {
    this.fetchData();
    this.intervalId = setInterval(this.fetchData, 6000);
  },
  destroyed() {
    window.clearInterval(this.intervalId);
  },
  methods: {
    cancelFeed(dialog) {
      dialog.value = false;
      this.tempAmount = "";
      this.tempTime = "";
    },
    addFeed(dialog) {
      dialog.value = false;
      this.addScheduledFeed();
    },
    fetchData() {
      let apiUrl = process.env.VUE_APP_BACKEND_URL + "?action=feed_schedule";
      this.axios.get(apiUrl, {}).then((response) => {
        this.scheduledFeeds = response.data;
      });
    },

    addScheduledFeed() {
      let body =
        "action=add_schedule&amount=" +
        this.tempAmount +
        "&feed_time=" +
        this.tempTime;
      let apiUrl = process.env.VUE_APP_BACKEND_URL;
      this.axios.post(apiUrl, body).then((response) => {
        this.scheduleResult = response.data;
      });

      var self = this;
      setTimeout(() => {
        self.fetchData();
        self.tempAmount = "";
        self.tempTime = "";
      }, 1000);
    },

    removeScheduledFeed(id) {
      let body = "action=delete_schedule&id=" + id;
      let apiUrl = process.env.VUE_APP_BACKEND_URL;
      this.axios.post(apiUrl, body).then((response) => {
        this.scheduleResult = response.data;
      });

      var self = this;
      setTimeout(() => {
        self.fetchData();
      }, 600);
    },
  },
};
</script>

<style scoped>
.trashcan i {
  color: white !important;
}
</style>
