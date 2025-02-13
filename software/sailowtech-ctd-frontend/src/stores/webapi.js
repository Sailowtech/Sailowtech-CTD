import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useWebapiStore = defineStore('webapi', () => {
  const endpoint = "http://127.0.0.1:8000"


  return { endpoint }
})
