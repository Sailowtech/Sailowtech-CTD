<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useWebapiStore } from '@/stores/webapi'
import { storeToRefs } from "pinia";
const { endpoint, debug, toggleDebug } = storeToRefs(useWebapiStore());
</script>

<template>
  <notifications />
  <nav class="bg-white border-gray-200 dark:bg-gray-900">
    <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
      <div class="w-full md:block md:w-auto" id="navbar-default">
        <ul class="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
          <li>
            <RouterLink to="/" :class="[ $route.name == 'quickaccess' ? 'block py-2 px-3 text-white bg-blue-700 rounded-sm md:bg-transparent md:text-blue-700 md:p-0 dark:text-white md:dark:text-blue-500' : 'block py-2 px-3 text-gray-900 rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent']">Quick Access</RouterLink>
          </li>
          <li>
            <RouterLink to="/visualize" :class="[ $route.name == 'visualize' ? 'block py-2 px-3 text-white bg-blue-700 rounded-sm md:bg-transparent md:text-blue-700 md:p-0 dark:text-white md:dark:text-blue-500' : 'block py-2 px-3 text-gray-900 rounded-sm hover:bg-gray-100 md:hover:bg-transparent md:border-0 md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent']">Visualize measurements</RouterLink>
          </li>
        </ul>
      </div>
      <div class="md:ml-0 md:mr-0 ml-auto mr-auto mt-4 md:mt-0">
        <label class="inline-flex items-center cursor-pointer">
          <input type="checkbox" v-model="debug" class="sr-only peer">
          <div class="relative w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600 dark:peer-checked:bg-blue-600"></div>
          <span class="ms-3 text-sm font-medium text-gray-900 dark:text-gray-300">Debug mode</span>
        </label>
      </div>
    </div>

  </nav>
  <RouterView />
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      system_time: null
    };
  },
  methods: {
    fetch_system_time() {
      const store = useWebapiStore()
      const apiUrl = `${store.endpoint}/system-time`;

      axios.get(apiUrl)
        .then((response) => {

          this.$notify({
            title: "System time",
            text: `System time is ${new Date(Date.parse(response.data.data.system_time)).toLocaleString("de-CH")}`,
          });

          this.system_time = response.data.system_time;
        })
        .catch((error) => {
          console.error('Error fetching data:', error);
        });
    }
  },
  mounted() {
      this.fetch_system_time()
    },
};

</script>