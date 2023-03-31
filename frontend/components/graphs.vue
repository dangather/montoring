<template>
    <div class="flex pt-5">
        <canvas id="chart" height="30px" width="50px"/>
        <canvas id="chart2" height="30px" width="50px" class="ml-3"/>
    </div>
    </template>
<script setup lang="ts">
import Chart, { ChartConfiguration } from "chart.js/auto"
import {getdata, datafetch, connect} from "../scripts/utils"
const labels = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "25",
    ",W5353","EWRWR",",EF"
]
const data = {
  labels: labels,
  datasets: [{
    label: 'cool label',
    data: [354,3535,5,52,2521,6,525,36,25,36,25,255],
    borderColor: 'rgb(23, 194, 4)',
  }]

};const data1 = {
  labels: labels,
  datasets: [{
    label: 'cool label',
    data: [743,64,4,747,46,6,463,6353,23,63,633,6],
    borderColor: 'rgb(227, 5, 5)',
  }]
};

const config = {
  type: 'line',
  data: data,
  options: {}
};

const config1 = {
  type: 'line',
  data: data1,
  options: {}
};

onMounted(() => {
    const chart = new Chart(
        document.getElementById("chart")! as HTMLCanvasElement,
        config as ChartConfiguration
        )    
    const chart1 = new Chart(
        document.getElementById("chart2")! as HTMLCanvasElement,
        config1 as ChartConfiguration
        )
}) 

</script> 