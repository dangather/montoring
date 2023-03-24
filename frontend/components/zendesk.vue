<template>
    <div class="p-5 text-center shadow text-5xl">
        Zendesk Tickets
    </div>
    <div class="flex justify-center">
    <zcards title="Open tickets" colour="green" border="8px solid green"> 
            131 
    </zcards>
    <Icon name="mdi:youtube" width="50" color="#15CA82"/>
    <zcards  title="Unassigned" colour="grey" border="8px solid grey"> 
        14
    </zcards>
</div>
</template>

<script setup>
import zcards from "/components/cards/zcards.vue"
import {Icon} from '@iconify/vue'

</script>
