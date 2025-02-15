<script setup>
import { Chart, registerables } from 'chart.js';
import { Line } from 'vue-chartjs'
import { useWebapiStore } from '@/stores/webapi'
import 'chartjs-adapter-moment';

Chart.register(...registerables);

</script>

<template class="max-h-screen m-8">
  <div>
    <form class="max-w-sm mx-auto">
      <label for="countries" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Select a run to visualize</label>
      <select v-model="selectedRun" @change="fetch_visualization_data($event.target.value)" id="countries" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
        <option v-for="r in runs" :value="r.id">{{ r.id }} - {{  (new Date(Date.parse(r.timestamp))).toLocaleString("de-CH") }}</option>
      </select>
    </form>

    <div class="flex justify-center m-4 p-4">
      <div v-if="chartData" class="w-3/4">
        <Line :data="chartData" :options="chartOptions"/>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      chartData: null,
      runs: null,
      selectedRun: null,
      chartOptions: {
        responsive: true,
        scales: {
          x: { title: { display: true, text: 'Timestamp' }, type: 'time', time: { tooltipFormat: 'DD T'} },
          y: { title: { display: true, text: 'Sensor Value' } }
        }
      }
    };
  },
  methods: {
    fetch_visualization_data(id) {
      const store = useWebapiStore()
      const apiUrl = `${store.endpoint}/visualization-data?run_id=${id}`;

      axios.get(apiUrl)
        .then((response) => {
          console.log(response.data)
          this.chartData = response.data;
        })
        .catch((error) => {
          console.error('Error fetching data:', error);
        });
    },

    fetch_runs_data() {
      const store = useWebapiStore()
      const apiUrl = `${store.endpoint}/runs`;

      axios.get(apiUrl)
        .then((response) => {
          this.runs = response.data.data
          if (this.runs.length > 0) {
            this.selectedRun = this.runs[0].id
            this.fetch_visualization_data(this.selectedRun)
          }

        })
        .catch((error) => {
          console.error('Error fetching data:', error);
        });
    }
  },
  mounted() {
      this.fetch_runs_data()
    },
};

</script>