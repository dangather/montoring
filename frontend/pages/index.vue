<template>
<div id="main">
    <component class="com" :is="i == 0 ? c : ''"/>
    <component class="com" :is="i == 1 ? h : ''"/>
</div>
</template>

<script setup lang="ts">
import cards from '~~/components/cards.vue';
import hello from "~~/components/hello.vue";
let comps: any = []
let c = resolveComponent("cards")
let h = resolveComponent("hello")
comps.push(cards, hello)

let i = ref(0)
setInterval(() =>  {
    i.value++
    if (i.value >= comps.length) {
        i.value = 0
    }    
}, 5000)




</script>