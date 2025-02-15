import { ref, watch } from 'vue'
import { defineStore } from 'pinia'

export const useWebapiStore = defineStore('webapi', () => {
  const endpoint = ref('http://192.168.42.1:80')
  const debug = ref(false)

  if (localStorage.getItem("endpoint")) {
    endpoint.value = localStorage.getItem("endpoint");
  }

  if (localStorage.getItem("debug")) {
    debug.value = localStorage.getItem("debug");
  }

  watch(debug, updateEndpoint)

  function updateEndpoint() {
    if (debug.value) {
      endpoint.value = 'http://127.0.0.1:8000'
    } else {
      endpoint.value = 'http://192.168.42.1:80'
    }
    localStorage.setItem('debug', debug.value);
    localStorage.setItem('endpoint', endpoint.value);
  }

  function toggleDebug() {
    debug.value = !debug.value
    if (debug.value) {
      endpoint.value = 'http://127.0.0.1:8000'
    } else {
      endpoint.value = 'http://192.168.42.1:80'
    }
    localStorage.setItem('debug', debug.value);
    localStorage.setItem('endpoint', endpoint.value);
  }



  return { endpoint, debug, toggleDebug }
})
