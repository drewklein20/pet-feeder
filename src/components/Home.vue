<template>
  <div>
    <v-container>
      <v-row dense>
        <v-col cols="12">
          <v-card
            color="secondary"
            dark
            v-if="settings.isUsingScale || settings.isUsingCamera"
          >
            <v-card-title class="headline mb-3 dark-text">
              Current Bowl
              <v-spacer></v-spacer>
              {{ settings.isUsingScale ? currentWeight + "g" : "" }}
            </v-card-title>

            <v-card-subtitle v-if="settings.isUsingScale">
              <v-progress-linear
                color="primary"
                :value="currentPercentage"
                height="30"
              >
                <strong>{{ currentPercentage }}%</strong>
              </v-progress-linear>
            </v-card-subtitle>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-card v-if="settings.isUsingCamera">
                <v-row>
                  <v-col>
                    <v-img
                      v-if="settings.isUsingCamera"
                      :lazy-src="currentImg"
                      max-height="80"
                      max-width="70"
                      :src="currentImg + '?rnd=' + cacheKey"
                    ></v-img>
                  </v-col>
                  <v-col class="smallCol">
                    <v-layout align-center justify-center class="pt-2 pb-6">
                      <v-icon
                        large
                        color="white"
                        class="pt-3"
                        @click="openPreview"
                      >
                        mdi-eye
                      </v-icon>
                    </v-layout>
                  </v-col>
                </v-row>
              </v-card>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col cols="12" class="pt-4">
          <v-card color="primary" dark>
            <v-card-title class="headline mb-3">
              <div>
                {{ settings.petName }}
                {{ settings.twoBowls ? "have" : "has" }} eaten
              </div>
              <v-spacer></v-spacer>
              <div class="small-header">
                {{ amountFedToday | decimalToFraction }}
                {{ amountFedToday > 1 ? "cups" : "cup" }} today
              </div>
            </v-card-title>

            <v-card-text class="pb-8">
              <v-row>
                <v-tooltip top>
                  <template v-slot:activator="{ on, attrs }">
                    <v-col class="light-text" v-bind="attrs" v-on="on">
                      {{ totalWeight }}
                      <v-icon class="ml-2" color="secondary" dark>
                        mdi-cup
                      </v-icon>
                    </v-col>
                  </template>
                  <span>{{ totalWeight }} cups of dog food</span>
                </v-tooltip>
                <v-tooltip top>
                  <template v-slot:activator="{ on, attrs }">
                    <v-col class="light-text" v-bind="attrs" v-on="on">
                      {{ (totalWeight / cupsPerBag).toFixed(2) }}
                      <v-icon class="ml-2" color="secondary" dark>
                        mdi-sack
                      </v-icon>
                    </v-col>
                  </template>
                  <span
                    >{{ (totalWeight / cupsPerBag).toFixed(2) }} bags of dog
                    food</span
                  >
                </v-tooltip>
                <v-tooltip top>
                  <template v-slot:activator="{ on, attrs }">
                    <v-col class="light-text" v-bind="attrs" v-on="on">
                      {{ (totalWeight / cupsPerBag / 3000).toFixed(2) }}
                      <v-icon class="ml-2" color="secondary" dark>
                        mdi-car-pickup
                      </v-icon>
                    </v-col>
                  </template>
                  <span>
                    {{ (totalWeight / cupsPerBag / 3000).toFixed(2) }} truck
                    loads of dog food</span
                  >
                </v-tooltip>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" class="pt-4">
          <v-card color="secondary" dark>
            <v-card-title class="headline dark-text">
              Last Fed
              <v-spacer></v-spacer>
              Next Feed
            </v-card-title>

            <div class="feed-times ml-4 mr-4">
              <!-- Left column -->
              <span v-if="logs.length" class="dark-text feed-time">
                {{ lastFeed | formatRelative }} ({{
                  lastFeedAmount | decimalToFraction
                }}
                {{ lastFeedAmount > 1 ? " Cups" : "Cup" }})
              </span>
              <span v-else class="dark-text feed-time">
                never
              </span>
              <!-- Right column -->
              <span
                v-if="scheduledFeeds.length"
                class="dark-text feed-time align-right"
              >
                {{ nextFeed | formatRelative }} ({{ nextFeedAmount }}
                {{ nextFeedAmount > 1 ? " Cups" : "Cup" }})
              </span>
              <span v-else class="dark-text feed-time align-right">
                no scheduled feeds
              </span>
            </div>

            <v-card-actions>
              <v-btn
                class="ml-2 mt-1 mb-3"
                outlined
                color="primary"
                rounded
                small
                @click="isShowingFeedNow = true"
              >
                Feed Now
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn
                class="ml-2 mt-1 mb-3"
                outlined
                color="primary"
                rounded
                small
                @click="$emit('clickedDrawer', 'Scheduler')"
              >
                {{
                  scheduledFeeds.length ? "Edit Schedule" : "Add Scheduled Feed"
                }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <v-dialog v-model="isPreviewingImg" max-width="600px">
      <v-card>
        <v-img
          v-if="settings.isUsingCamera"
          :lazy-src="currentImg"
          :src="currentImg + '?rnd=' + cacheKey"
        ></v-img>
      </v-card>
    </v-dialog>

    <v-dialog v-model="isShowingFeedNow" max-width="400px">
      <feed></feed>
    </v-dialog>
  </div>
</template>

<script>
import moment from "moment";
import feed from "../components/Feed";

export default {
  name: "Home",
  components: { feed },
  props: {
    currentWeight: { type: String, required: false },
    currentPercentage: { type: String, required: false },
    settings: { type: Object, required: false },
  },
  data: () => ({
    cupsPerBag: 160,
    datacollection: null,
    weights: [],
    scheduledFeeds: [],
    logs: [],
    intervalId: "",
    timeUnit: "hour",
    interval: "24",
    padding: 8,
    radius: 10,
    value: [0, 2, 5, 9, 5, 10, 3, 5, 0, 0, 1, 8, 2, 9, 0],
    isPreviewingImg: false,
    cacheKey: +new Date(),
    imgInterval: "",
    isShowingFeedNow: false,
  }),
  async mounted() {
    await this.fetchData();
  },
  created() {
    this.imgInterval = setInterval(() => {
      this.cacheKey = +new Date();
    }, 30 * 1000);
  },
  destroyed() {
    clearInterval(this.imgInterval);
  },
  computed: {
    weightLabels() {
      return this.weights.map((a) =>
        this.$options.filters.formatDateTime2(String(a.timestamp))
      );
    },
    weightValues() {
      if (this.weights.length) {
        return this.weights.map((a) => parseInt(a.value));
      } else {
        return [];
      }
    },
    currentImg() {
      return process.env.VUE_APP_CAM_RESOURCES + "live.jpg";
    },
    totalWeight() {
      let sum = 0;

      for (let element of this.logs) {
        if (!isNaN(element.amount)) {
          let amount = parseFloat(element.amount);
          sum = sum + amount;
        }
      }

      if (this.settings.twoBowls == true) {
        sum = sum * 2;
      }

      return sum;
    },
    timeRightNow() {
      const now = moment();

      return now.format("HH:mm");
    },
    lastFeed() {
      if (this.logs.length) {
        return this.logs[0].timestamp;
      } else {
        return null;
      }
    },
    lastFeedAmount() {
      if (this.logs.length) {
        return this.logs[0].amount;
      } else {
        return null;
      }
    },
    nextFeed() {
      if (this.scheduledFeeds.length) {
        let now = moment();
        let closestFeed = moment().add(4, "days");

        for (let element of this.scheduledFeeds) {
          if (element.feedTime < this.timeRightNow) {
            let timeSplit = element.feedTime.split(":");
            let feedDate = moment().add(1, "days");
            feedDate.set({ h: timeSplit[0], m: timeSplit[1] });

            if (feedDate < closestFeed) {
              closestFeed = feedDate;
            }
          } else {
            let timeSplit = element.feedTime.split(":");
            let feedDate = moment();
            feedDate.set({ h: timeSplit[0], m: timeSplit[1] });

            if (feedDate < closestFeed) {
              closestFeed = feedDate;
            }
          }
        }

        return closestFeed.format();
      } else {
        return null;
      }
    },
    amountFedToday() {
      if (this.logs.length) {
        let sum = 0;
        let now = moment();

        for (let element of this.logs) {
          let feedMoment = moment(element.timestamp);

          if (now.isSame(feedMoment, "day")) {
            sum += parseFloat(element.amount);
          }
        }
        return sum;
      } else {
        return 0;
      }
    },
    nextFeedAmount() {
      if (this.scheduledFeeds.length) {
        let amount = "";
        let now = moment();
        let closestFeed = moment().add(4, "days");

        for (let element of this.scheduledFeeds) {
          if (element.feedTime < this.timeRightNow) {
            let timeSplit = element.feedTime.split(":");
            let feedDate = moment().add(1, "days");
            feedDate.set({ h: timeSplit[0], m: timeSplit[1] });

            if (feedDate < closestFeed) {
              closestFeed = feedDate;
              amount = element.amount;
            }
          } else {
            let timeSplit = element.feedTime.split(":");
            let feedDate = moment();
            feedDate.set({ h: timeSplit[0], m: timeSplit[1] });

            if (feedDate < closestFeed) {
              closestFeed = feedDate;
              amount = element.amount;
            }
          }
        }

        return amount;
      } else {
        return null;
      }
    },
  },
  methods: {
    openPreview() {
      this.isPreviewingImg = true;
    },
    fillData() {
      this.datacollection = {
        labels: this.weightLabels,
        datasets: [
          {
            label: "Bowl Weight",
            backgroundColor: "#f87979",
            data: this.weightValues,
          },
        ],
      };
    },
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
    async fetchData() {
      let apiUrl =
        process.env.VUE_APP_BACKEND_URL +
        "?action=all_weights&timeUnit=" +
        this.timeUnit +
        "&interval=" +
        this.interval;
      this.axios.get(apiUrl, {}).then((response) => {
        this.weights = response.data;
        this.fillData();
      });

      apiUrl = process.env.VUE_APP_BACKEND_URL + "?action=feed_logs";
      this.axios.get(apiUrl, {}).then((response) => {
        this.logs = response.data;
      });

      apiUrl = process.env.VUE_APP_BACKEND_URL + "?action=feed_schedule";
      this.axios.get(apiUrl, {}).then((response) => {
        this.scheduledFeeds = response.data;
      });
    },
  },
};
</script>

<style>
.small {
  max-width: 500px;
  margin: 150px auto;
}
.small-header {
  font-size: 18px;
}
.light-text {
  color: #afcbff;
  text-align: center;
  font-weight: 500;
  font-size: 14;
}
.dark-text {
  color: #0e1c36;
}
.feed-times {
  display: flex;
  margin-bottom: 26px;
}
.feed-time {
  width: 50%;
}
.align-right {
  text-align: end;
}
.smallCol {
  max-width: 46px !important;
  margin-left: -13px;
  margin-right: 10px;
}
</style>
