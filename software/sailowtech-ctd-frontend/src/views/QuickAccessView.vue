<script setup>
import RunItem from '@/components/RunItem.vue';
import { useWebapiStore } from '@/stores/webapi'
</script>

<template>
  <main>

    <div class="m-5">
      <div class="text-2xl">Start measurements</div>
      <div>
        <button v-on:click="start_manual_run()" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">Start Manual Run</button>
      </div>
    </div>


    <div class="m-5">
      <div class="text-2xl">Currently running</div>
      <ul v-if="hasrunning">
        <template v-for="item in runs"><li v-if="item.running" class="flex justify-between gap-x-6 py-5">
          <RunItem :id="item.id" :timestamp="item.timestamp" :run_type="item.run_type" :wanted_duration="item.wanted_duration" :wanted_measurements="item.wanted_measurements" :running="item.running"></RunItem>
        </li></template>
      </ul>
      <p v-else>No measurements currently running</p>
    </div>

    <div class="m-5">
      <div class="text-2xl">All Runs</div>
      <ul role="list" class="divide-y divide-gray-100" v-if="runs">
        <li v-for="item in runs" class="flex justify-between gap-x-6 py-5">
          <RunItem :id="item.id" :timestamp="item.timestamp" :run_type="item.run_type" :wanted_duration="item.wanted_duration" :wanted_measurements="item.wanted_measurements" :running="item.running"></RunItem>
        </li>
      </ul>
      <p v-else>Loading...</p>
    </div>
    
  </main>
</template>



<script>
import axios from 'axios';

export default {
  data() {
    return {
      runs: null,
      hasrunning: null,
    };
  },
  methods: {
    start_manual_run() {
      const store = useWebapiStore()
      const apiUrl = `${store.endpoint}/run?run_type=0`;

      axios.get(apiUrl)
        .then((response) => {
          console.log(response)
        })
        .catch((error) => {
          console.error('Error fetching data:', error);
        });
    }
  },
  mounted() {
      const store = useWebapiStore()
      const apiUrl = `${store.endpoint}/runs`;

      axios.get(apiUrl)
        .then((response) => {
          this.runs = response.data.data;
          this.hasrunning = this.runs.map(e => e.running).includes(true)
        })
        .catch((error) => {
          console.error('Error fetching data:', error);
        });

        
    },
};

</script>