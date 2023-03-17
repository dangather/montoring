<template>
<div class="main">
    <cards/>
</div>
</template>

<script setup lang="ts">
import cards from '~~/components/cards.vue';
import hello from "~~/components/hello.vue";
let comps: any = []
comps.push(cards, hello)
let main = document.getElementById
let i = 0
setInterval(() =>  {
    console.log(comps[i])
    i++
    if (i >= comps.length) {
        i = 0
    }    
}, 5000)


</script>