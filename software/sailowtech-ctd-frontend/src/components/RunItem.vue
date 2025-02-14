<script setup>
import { useWebapiStore } from '@/stores/webapi'
const store = useWebapiStore()
defineProps(['id', 'timestamp', 'run_type', 'wanted_duration', 'wanted_measurements', 'running', 'deleted'])
</script>

<template>

  <div class="flex min-w-0 gap-x-4">
    <div class="min-w-0 flex-auto">
      <p class="text-sm/6 font-semibold text-gray-900">Run ID: {{ id }}</p>
      <p class="mt-1 truncate text-xs/5 text-gray-500">{{ timestamp }}</p>
    </div>
  </div>
  <div class="flex min-w-0 gap-x-4">
    <a :href="`${store.endpoint}/csv?run_id=${id}`" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">Download data</a>
  </div>
  <div v-if="running && !deleted" class="flex min-w-0 gap-x-4">
    <button v-on:click="stop_run(id)" type="button" class="focus:outline-none text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900">Stop Running</button>
  </div>
  <div v-else class="flex min-w-0 gap-x-4">
  </div>
  <div class="hidden shrink-0 sm:flex sm:flex-col sm:items-end">
    <p class="text-sm/6 text-gray-900">Type: {{ run_type }}</p>
    <div v-if="running" class="mt-1 flex items-center gap-x-1.5">
      <div class="flex-none rounded-full bg-emerald-500/20 p-1">
        <div class="size-1.5 rounded-full bg-emerald-500"></div>
      </div>
      <p class="text-xs/5 text-gray-500">Running</p>
    </div>
    <p v-else class="mt-1 text-xs/5 text-gray-500">Stopped</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      deleted: false
    };
  },
  methods: {
    stop_run(id) {
        const store = useWebapiStore()
        const apiUrl = `${store.endpoint}/stop?run_id=${id}`;

        axios.get(apiUrl)
          .then((response) => {
            this.deleted = response.data;
          })
          .catch((error) => {
            console.error('Error fetching data:', error);
          });

          
      },
    }
  };

</script>