import Vue from "vue";
import moment from "moment";

Vue.filter("formatDate", function(value) {
  if (value) {
    return moment(String(value)).format("LLL");
  }
});

Vue.filter("formatDateShorter", function(value) {
  if (value) {
    return moment(String(value)).format("lll");
  }
});

Vue.filter("formatRelative", function(value) {
  if (value) {
    return moment(String(value)).calendar();
  }
});

Vue.filter("12Hour", function(time) {
  if (time) {
    time = time
      .toString()
      .match(/^([01]\d|2[0-3])(:)([0-5]\d)(:[0-5]\d)?$/) || [time];

    if (time.length > 1) {
      // If time format correct
      time = time.slice(1); // Remove full string match value
      time[5] = +time[0] < 12 ? " AM" : " PM"; // Set AM/PM
      time[0] = +time[0] % 12 || 12; // Adjust hours
    }
    return time.join(""); // return adjusted time or original string

    // let hr = value.split(':')[0]
    // var suffix = hr >= 12 ? "PM":"AM";
    // var hours = ((hr + 11) % 12 + 1)
    // return hours + ':' + value.split(':')[1] + ' ' + suffix
  }
});

Vue.filter("formatDateTime", function(value) {
  if (value) {
    return moment(String(value)).format("YYYY-MM-DD HH:mm:ss");
  }
});

Vue.filter("formatDateTime2", function(value) {
  if (value) {
    return moment(String(value)).format("MM-DD HH:mm");
  }
});

Vue.filter("formatDateTimeOnly", function(value) {
  if (value) {
    return moment(String(value)).format("HH:mm:ss");
  }
});
