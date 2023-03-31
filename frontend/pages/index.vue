<template>
    <div id="main">
        <keep-alive>
            <component :is="i == 1 ? card : zend"/>
        </keep-alive>
    </div>
</template>

<script setup lang="ts">
import cards from '~~/components/cards/cards.vue';
import zendesk from "~~/components/zendesk.vue";
let comps: any = []
const card = resolveComponent("cards")
const zend = resolveComponent("zendesk")
comps.push(card, zend)

let i = ref(0)

const time = 2


setInterval(() =>  {
    i.value++
    if (i.value >= comps.length) {
        i.value = 0
    }
    console.log(i.value)
}, time * 1000) 
</script>