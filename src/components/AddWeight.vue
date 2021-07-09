<template>
  <v-card class="mx-auto" max-width="400">
    <v-card-title>
      Add Weight
    </v-card-title>
    <v-card-text>
      <v-row>
        <v-col>
          <v-text-field outlined type="number" v-model="amount"/> 
        </v-col>

        <v-col>
          <v-layout align-center justify-center class="pt-2">
            <v-btn
              rounded
              color="secondary"
              @click="addWeight"
            >
              Add
            </v-btn>
          </v-layout>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-layout align-center justify-center>
        <p>{{ addResult }}</p>
      </v-layout>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: "AddWeight",

  data: () => ({
    amount: "1",
    addResult: "",
  }),
  methods: {
    addWeight() {
      let body = "action=add_pet_weight&amount=" + this.amount;
      let apiUrl = process.env.VUE_APP_BACKEND_URL;
      this.axios.post(apiUrl, body).then((response) => {
        this.addResult = response.data;
        if (this.addResult == 'Adding pet weight.') {
           
            var self = this;
            setTimeout(() => {
              self.addResult = "";
              self.$emit("closeDialog");
            }, 1500);
        }
      });
    },
  },
};
</script>
