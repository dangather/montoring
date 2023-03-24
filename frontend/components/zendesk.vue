<template>
    <titlebar>
        Zendesk tickets
    </titlebar>

    <div class="flex justify-center ">
        <zcards title="Open tickets" colour="green" border="8px solid green"> 
                131 
        </zcards>
        <zcards  title="Unassigned" colour="grey" border="8px solid grey"> 
            14
        </zcards>    
        <zcards  title="Unsatisfied clients" colour="red" border="8px solid red"> 
            242423235
        </zcards>    
   
    </div>
</template>

<script setup>
import zcards from "/components/cards/zcards.vue"
import {Icon} from '@iconify/vue'
import titlebar from "./titlebar.vue"

</script>
