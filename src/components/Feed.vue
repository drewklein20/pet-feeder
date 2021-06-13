<template>
  <v-card class="mx-auto" max-width="400">
    <v-card-title>
      Feed Now
    </v-card-title>
    <v-card-text>
      <v-row>
        <v-col>
          <v-select
            v-model="amount"
            :items="amounts"
            label="Feed Amount"
            hint="Cups"
            persistent-hint
            outlined
          >
            <template v-slot:selection="data">
              <span>{{ data.item | decimalToFraction }}</span>
            </template>
            <template v-slot:item="data">
              <span>{{ data.item | decimalToFraction }}</span>
            </template>
          </v-select>

          <!-- <v-select
                  :items="versions"
                  v-model="selectedVersion"
                  @change="changeTranscript"
                  solo
                >
                <template v-slot:selection="data">
                  <span class="transcript-dialog__alternate-text">{{ data.item.text }} {{isAutoSaved(data.item.value) ? '(Autosaved)' : ''}}</span>
                  <v-icon class="ml-2" v-if="isTranscriptPrimary(data.item.value)">closed_caption</v-icon>
                </template>
                <template v-slot:item="data">
                  <span class="transcript-dialog__alternate-text">{{ data.item.text }} {{isAutoSaved(data.item.value) ? '(Autosaved)' : ''}}</span>
                  <v-icon class="ml-2" v-if="isTranscriptPrimary(data.item.value)">closed_caption</v-icon>
                </template>
                </v-select> -->
        </v-col>

        <v-col>
          <v-layout align-center justify-center class="pt-2">
            <v-btn
              rounded
              color="secondary"
              @click="feedRequest"
              :disabled="isFeeding"
            >
              Feed
            </v-btn>
          </v-layout>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-layout align-center justify-center>
        <p>{{ feedResult }}</p>
      </v-layout>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "Feed",

  data: () => ({
    amount: "1",
    feedResult: "",
    amounts: [
      "0.25",
      "0.5",
      "0.75",
      "1",
      "1.25",
      "1.5",
      "1.75",
      "2",
      "2.25",
      "2.5",
      "2.75",
      "3",
      "3.25",
      "3.5",
      "3.75",
      "4",
      "4.25",
      "4.5",
      "4.75",
      "5",
    ],
    isFeeding: false,
  }),
  methods: {
    feedRequest() {
      this.isFeeding = true;
      let cupOrCups = this.amount > 1 ? " cups " : " cup ";
      this.feedResult = "Dispensing " + this.amount + cupOrCups + "now!";
      let body = "action=feed_now&amount=" + this.amount;
      let apiUrl = process.env.VUE_APP_BACKEND_URL;
      this.axios.post(apiUrl, body).then((response) => {
        this.feedResult = response.data;
        this.isFeeding = false;
        self.feedResult = "";
      });

      // var self = this;
      // setTimeout(() => {
      //   self.feedResult = "";
      // }, 5000);
    },
  },
};
</script>
