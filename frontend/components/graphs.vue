<template>
    <div class="flex pt-5">
        <canvas id="chart" height="30px" width="50px"/>
        <canvas id="chart2" height="30px" width="50px" class="ml-3"/>
    </div>
    </template>
<script setup lang="ts">
import Chart from "chart.js/auto"
import {getdata, datafetch, connect} from "../scripts/utils"

const labels = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august"
]
const data = {
  labels: labels,
  datasets: [{
    label: 'cool label',
    data: [354,3535,5,52,2521,25,24],
    borderColor: 'rgb(23, 194, 4)',
  }]
};

const config = {
  type: 'line',
  data: data,
  options: {}
};

onMounted(() => {
    const chart = new Chart(
        document.getElementById("chart"),
        config
        )    
    const chart1 = new Chart(
        document.getElementById("chart2"),
        config
        )
})

</script> 