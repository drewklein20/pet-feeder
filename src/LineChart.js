import { Line, mixins } from "vue-chartjs";
const { reactiveProp } = mixins;

export default {
  extends: Line,
  mixins: [reactiveProp],
  // props: ['options'],
  mounted() {
    var options = {
      responsive: true,
      scales: {
        xAxes: [
          {
            afterTickToLabelConversion: function(data) {
              var xLabels = data.ticks;
              xLabels.forEach(function(labels, i) {
                if (i % 2 == 1) {
                  xLabels[i] = "";
                }
              });
            },
          },
        ],
      },
    };
    // this.chartData is created in the mixin.
    // If you want to pass options please create a local options object
    this.renderChart(this.chartData, options);
  },
};
