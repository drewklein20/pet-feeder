<template>
  <div>
    <v-app-bar height="60px" color="primary" dark prominent>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>{{ selectedDrawerItem }}</v-toolbar-title>

      <v-spacer></v-spacer>

      <div class="pr-4 pt-1" v-if="settings.isUsingScale">
        <span class=" pr-1 bowl-label-pre"> {{ weightInGrams }} g</span>
        <v-icon class="pb-2 bowl-icon">mdi-bowl</v-icon>
        <span class="bowl-label"> {{ weightPercentage }} %</span>
      </div>

      <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn color="secondary" icon v-bind="attrs" v-on="on">
            <v-icon color="secondary">mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="$emit('authEvent', false)">
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" absolute top temporary>
      <v-list dense>
        <v-list-item
          :class="[{ selected: selectedDrawerItem == item.title }]"
          v-for="item in items"
          :key="item.title"
          link
          @click.stop="drawer = !drawer"
          @click="clickedDrawer(item.title)"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <div class="main-content">
      <feed v-if="selectedDrawerItem == 'Feed Now'" />
      <feed-log v-if="selectedDrawerItem == 'Feed Log'" />
      <schedule v-if="selectedDrawerItem == 'Scheduler'" />
      <home
        v-if="selectedDrawerItem == 'Home'"
        :currentWeight="weightInGrams"
        :currentPercentage="weightPercentage"
        :settings="settings"
        @clickedDrawer="clickedDrawer"
      />
      <settings v-if="selectedDrawerItem == 'Settings'" />
    </div>
  </div>
</template>

<script>
import Feed from "./Feed.vue";
import FeedLog from "./FeedLog.vue";
import Schedule from "./Schedule.vue";
import Settings from "./Settings.vue";
import Home from "./Home.vue";
export default {
  components: { FeedLog, Feed, Schedule, Settings, Home },
  name: "Feeder",

  data: () => ({
    selectedDrawerItem: "Home",
    drawer: false,
    items: [
      { title: "Home", icon: "mdi-dog" },
      { title: "Feed Now", icon: "mdi-bowl" },
      { title: "Feed Log", icon: "mdi-table" },
      { title: "Scheduler", icon: "mdi-calendar" },
      { title: "Settings", icon: "mdi-cog-outline" },
    ],
    mini: true,
    weight: [],
    settings: {
      petName: "",
      twoBowls: false,
      username: "admin",
      password: "admin",
      feederName: "",
      defaultFeedAmount: 1,
      fullBowlWeight: 0.0,
      scaleReferenceUnit: 1,
      cupDuration: 3.0,
      isUsingScale: false,
      isUsingAlexa: false,
      sinricAPI: "",
      sinricDeviceId: "",
      leftBowlOffset: 0.0,
      rightBowlOffset: 0.0,
    },
  }),
  computed: {
    weightInGrams() {
      let weightVal = "0";

      if (this.weight.length) {
        weightVal = this.weight[0].value < 0 ? "0" : this.weight[0].value;
      }

      return weightVal;
    },
    weightPercentage() {
      let weightVal = "0";

      if (this.weight.length) {
        weightVal = this.weight[0].value < 0 ? 0 : this.weight[0].value;
      }

      return ((weightVal / this.settings.fullBowlWeight) * 100).toFixed(0);
    },
  },
  mounted() {
    this.fetchData();
    this.intervalId = setInterval(this.fetchData, 6000);
  },
  destroyed() {
    window.clearInterval(this.intervalId);
  },
  methods: {
    clickedDrawer(value) {
      this.selectedDrawerItem = value;
    },
    fetchData() {
      let apiUrl = process.env.VUE_APP_BACKEND_URL + "?action=current_weight";
      this.axios.get(apiUrl, {}).then((response) => {
        this.weight = response.data;
      });

      apiUrl = process.env.VUE_APP_BACKEND_URL + "?action=feeder_settings&id=1";
      this.axios.get(apiUrl, {}).then((response) => {
        this.settings = JSON.parse(response.data[0].preferences);
      });
    },
  },
};
</script>

<style scoped>
.main-content {
  margin: auto;
  width: 96%;
  padding: 20px 20px 20px 20px;
}

.selected {
  background: #afcbff;
}

.nav-bar {
  display: inline-flex;
}

.bowl-icon {
  font-size: 24pt;
  color: #afcbff;
}

.bowl-label {
  font-size: 12pt !important;
  color: #afcbff;
}
.bowl-label-pre {
  font-size: 12pt !important;
  color: #afcbff;
}
</style>
