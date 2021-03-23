import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex);

function initialState() {
  return {
    username: '',
    password: '',
    isAuthenticated: ''
  }
}

export default new Vuex.Store({
  state: initialState,
  mutations: {
    setIsAuthenticated(state, authEvent) {
      state.isAuthenticated = authEvent;
    },
  },
  actions: {
  },
  modules: {},
  plugins: [createPersistedState({
    paths: ['isAuthenticated'],
    storage: window.sessionStorage
  })]
});
