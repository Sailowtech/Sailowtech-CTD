import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useWebapiStore = defineStore('webapi', () => {
  const endpoint = "http://192.168.42.1:80"


  return { endpoint }
})
