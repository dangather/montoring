<template>
<div id="main">
    <component class="com" :is="i == 0 ? c : ''"/>
    <component class="com" :is="i == 1 ? z : ''"/>

</div>
</template>

<script setup lang="ts">
import cards from '~~/components/cards/cards.vue';
import zendesk from "~~/components/zendesk.vue";
let comps: any = []
let c = resolveComponent("cards")
let z = resolveComponent("zendesk")
comps.push(cards)

let i = ref(0)
const time = 5 * 1000
setInterval(() =>  {
    i.value++
    if (i.value >= comps.length) {
        i.value = 0
    }    
}, time) 


</script>