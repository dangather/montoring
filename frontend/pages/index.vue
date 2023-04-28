<template>
    <div id="main">
      <KeepAlive>
            <component :is="current"/>        
      </KeepAlive>
   </div>
</template>

<script setup lang="ts">
import cards from '~~/components/cards/cards.vue';
import zendesk from "~~/components/zendesk.vue";

const comps = ["cards", "zendesk"]

let current = ref()
const i = ref(0)
let interval: any = null
const time = 2

onMounted(() => {
  interval = setInterval(() =>  {
    i.value++
    if (i.value >= comps.length) {
      i.value = 0
    }
    current.value = comps[i.value]
    console.log(current.value)
    console.log(i.value)
  }, time * 1000) 
})

onBeforeUnmount(() => {
  clearInterval(interval)
})  
</script>