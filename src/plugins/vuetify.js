import Vue from "vue";
import Vuetify from "vuetify/lib/framework";

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    themes: {
      light: {
        primary: "#0E1C36",
        secondary: "#AFCBFF",
        accent: "#4caf50",
        error: "#f44336",
        warning: "#cddc39",
        info: "#00bcd4",
        success: "#2196f3",
      },
    },
  },
});
