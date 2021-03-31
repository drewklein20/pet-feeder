<template>
  <v-container>
    <v-card class="mx-auto">
      <v-card-title>
        Feeder Settings
      </v-card-title>
      <v-card-text>
        <v-expansion-panels v-model="openedPanel" multiple accordian>
          <v-expansion-panel>
            <v-expansion-panel-header>Pet & Device</v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-row>
                <v-col>
                  <v-text-field
                    label="Pet name"
                    placeholder=""
                    v-model="settings.petName"
                    outlined
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    label="Device name"
                    placeholder=""
                    v-model="settings.feederName"
                    outlined
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header>Feeding</v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-row>
                <v-col>
                  <v-text-field
                    label="1 Cup Duration (seconds)"
                    placeholder=""
                    type="number"
                    v-model="settings.cupDuration"
                    outlined
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-layout>
                    <v-checkbox
                      v-model="settings.twoBowls"
                      :label="`Two Bowls`"
                    ></v-checkbox>
                  </v-layout>
                </v-col>
                <v-col>
                  <v-text-field
                    v-if="settings.twoBowls"
                    label="Left Bowl Offset (seconds)"
                    placeholder=""
                    type="number"
                    v-model="settings.leftBowlOffset"
                    outlined
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    v-if="settings.twoBowls"
                    label="Right Bowl Offset (seconds)"
                    placeholder=""
                    type="number"
                    v-model="settings.rightBowlOffset"
                    outlined
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header>Authentication</v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-row>
                <v-col>
                  <v-text-field
                    label="Username"
                    placeholder=""
                    v-model="settings.username"
                    outlined
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    label="Password"
                    placeholder=""
                    v-model="settings.password"
                    outlined
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header>
              <v-switch
                v-on:click.stop
                @change="togglePanel(3, settings.emailNotifications)"
                v-model="settings.emailNotifications"
                label="Email Notifications"
              ></v-switch>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <p v-if="settings.emailNotifications">(Only SMTP)</p>
              <v-row>
                <v-col>
                  <v-text-field
                    v-if="settings.emailNotifications"
                    label="Email"
                    placeholder=""
                    type="email"
                    v-model="settings.emailConfig.proxyEmail"
                    outlined
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    v-if="settings.emailNotifications"
                    label="Password"
                    placeholder=""
                    type="password"
                    v-model="settings.emailConfig.proxyPassword"
                    outlined
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-text-field
                    v-if="settings.emailNotifications"
                    label="To Email(s)"
                    hint="Comma Separated"
                    persistent-hint
                    v-model="settings.emailConfig.toEmail"
                    outlined
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-layout align-center justify-center>
                    <v-checkbox
                      v-if="settings.emailNotifications"
                      label="Use SSL"
                      v-model="settings.emailConfig.ssl"
                      outlined
                    ></v-checkbox>
                  </v-layout>
                </v-col>
                <v-col>
                  <v-text-field
                    v-if="settings.emailNotifications"
                    label="Port"
                    type="number"
                    v-model="settings.emailConfig.port"
                    outlined
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-layout align-center justify-center class="pt-2 pb-6">
                    <v-btn
                      v-if="settings.emailNotifications"
                      :disabled="!emailSettingsValid"
                      color="secondary"
                    >
                      Test Email
                    </v-btn>
                  </v-layout>
                </v-col>
              </v-row>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header
              ><v-switch
                v-on:click.stop
                @change="togglePanel(4, settings.isUsingAlexa)"
                v-model="settings.isUsingAlexa"
                label="Alexa"
              ></v-switch
            ></v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-row>
                <v-col>
                  <v-select
                    v-if="settings.isUsingAlexa"
                    v-model="settings.defaultFeedAmount"
                    :items="amounts"
                    type="number"
                    label="Alexa Default Feed Amount (cups)"
                    hint="Cups"
                    persistent-hint
                    outlined
                  ></v-select>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-text-field
                    v-if="settings.isUsingAlexa"
                    label="Sinric API Key"
                    placeholder=""
                    v-model="settings.sinricAPI"
                    outlined
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    v-if="settings.isUsingAlexa"
                    label="Sinric Device ID"
                    placeholder=""
                    v-model="settings.sinricDeviceId"
                    outlined
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row v-if="settings.isUsingAlexa">
                <v-layout align-center justify-center class="pt-2 pb-6">
                  <v-btn
                    rounded
                    color="secondary"
                    @click="resetAlexa"
                    :disabled="isUpdating"
                  >
                    Reset Alexa
                  </v-btn>
                </v-layout>
              </v-row>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header>
              <v-switch
                v-on:click.stop
                @change="togglePanel(5, settings.isUsingScale)"
                v-model="settings.isUsingScale"
                label="Scale"
              ></v-switch>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-row>
                <v-col>
                  <v-text-field
                    v-if="settings.isUsingScale"
                    label="Scale Reference Unit"
                    placeholder=""
                    type="number"
                    v-model="settings.scaleReferenceUnit"
                    outlined
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    v-if="settings.isUsingScale"
                    label="Full Bowl Weight (g)"
                    placeholder=""
                    type="number"
                    v-model="settings.fullBowlWeight"
                    outlined
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row v-if="settings.isUsingScale">
                <v-layout align-center justify-center class="pt-2 pb-6">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        rounded
                        color="secondary"
                        @click="resetScale"
                        :disabled="isUpdating"
                        v-bind="attrs"
                        v-on="on"
                      >
                        Reset Scale
                      </v-btn>
                    </template>
                    <span>Please empty bowl before resetting the scale</span>
                  </v-tooltip>
                </v-layout>
              </v-row>
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header>
              <v-switch
                v-on:click.stop
                @change="togglePanel(6, settings.isUsingCamera)"
                v-model="settings.isUsingCamera"
                label="Camera"
              ></v-switch>
            </v-expansion-panel-header>
            <v-expansion-panel-content>
              <v-row>
                <v-col> </v-col>
                <v-col> </v-col>
              </v-row>
              <v-row v-if="settings.isUsingCamera">
                <v-layout align-center justify-center class="pt-2 pb-6">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        rounded
                        color="secondary"
                        @click="resetScale"
                        :disabled="isUpdating"
                        v-bind="attrs"
                        v-on="on"
                      >
                        Reset Camera
                      </v-btn>
                    </template>
                    <span>Please empty bowl before resetting the scale</span>
                  </v-tooltip>
                </v-layout>
              </v-row>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
        <v-row>
          <v-col>
            <v-layout align-center justify-center class="pt-11">
              <v-btn
                rounded
                color="secondary"
                @click="updateSettings"
                :disabled="
                  isUpdating ||
                    !fieldsHaveChanged ||
                    !authSettingsValid ||
                    !feedSettingsValid ||
                    !emailSettingsValid ||
                    !alexaSettingsValid ||
                    !scaleSettingsValid
                "
              >
                Update
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
  </v-container>
</template>

<script>
import _ from "lodash";

export default {
  components: {},
  name: "Settings",

  data: () => ({
    feederId: 1,
    openedPanel: [],
    amount: "1",
    feedResult: "",
    amounts: [".5", "1", "1.5", "2", "2.5", "3", "3.5", "4", "4.5", "5"],
    tempSettings: {},
    settings: {
      petName: "Pet",
      twoBowls: false,
      username: "admin",
      password: "password",
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
      isUsingCamera: false,
      emailNotifications: false,
      emailConfig: {
        ssl: true,
        port: 587,
        proxyEmail: "",
        proxyPassword: "",
        toEmail: "",
      },
    },
    isUpdating: false,
  }),
  computed: {
    fieldsHaveChanged() {
      let fieldsHaveChanged = false;
      if (this.tempSettings != {}) {
        fieldsHaveChanged = !_.isEqual(this.tempSettings, this.settings);
      } else {
        fieldsHaveChanged = true;
      }

      return fieldsHaveChanged;
    },
    feedSettingsValid() {
      return this.settings.cupDuration != "";
    },
    authSettingsValid() {
      return this.settings.username != "" && this.settings.password != "";
    },
    emailSettingsValid() {
      let emailSettings = this.settings.emailConfig;

      if (this.settings.emailNotifications) {
        return (
          emailSettings.proxyEmail != "" &&
          emailSettings.proxyPassword != "" &&
          emailSettings.toEmail != "" &&
          emailSettings.port != ""
        );
      } else {
        return true;
      }
    },
    alexaSettingsValid() {
      if (this.settings.isUsingAlexa) {
        return (
          this.settings.sinricAPI != "" && this.settings.sinricDeviceId != ""
        );
      } else {
        return true;
      }
    },
    scaleSettingsValid() {
      if (this.settings.isUsingScale) {
        return (
          this.settings.scaleReferenceUnit != "" &&
          this.settings.fullBowlWeight != ""
        );
      } else {
        return true;
      }
    },
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    togglePanel(index, value) {
      if (value == true) {
        this.openedPanel.push(index);
      } else {
        this.openedPanel = this.openedPanel.filter(
          (element) => element != index
        );
      }

      this.openedPanel = _.uniqBy(this.openedPanel);
    },
    fetchData() {
      let apiUrl =
        process.env.VUE_APP_BACKEND_URL +
        "?action=feeder_settings&id=" +
        this.feederId;
      this.axios.get(apiUrl, {}).then((response) => {
        this.settings = JSON.parse(response.data[0].preferences);
        this.tempSettings = _.cloneDeep(this.settings);
      });
    },
    updateSettings() {
      this.isUpdating = true;
      let body =
        "action=update_preferences&preferences=" +
        JSON.stringify(this.settings);
      let apiUrl = process.env.VUE_APP_BACKEND_URL;
      this.axios.post(apiUrl, body).then((response) => {
        this.isUpdating = false;
        this.fetchData();
      });
    },
    resetScale() {
      this.isUpdating = true;
      let body = "action=reset_scale";
      let apiUrl = process.env.VUE_APP_BACKEND_URL;
      this.axios.post(apiUrl, body).then((response) => {
        this.isUpdating = false;
      });
    },
    resetAlexa() {
      this.isUpdating = true;
      let body = "action=reset_alexa";
      let apiUrl = process.env.VUE_APP_BACKEND_URL;
      this.axios.post(apiUrl, body).then((response) => {
        this.isUpdating = false;
      });
    },
  },
};
</script>
<style scoped>
.v-expansion-panel-header div {
  flex: none;
}
</style>
