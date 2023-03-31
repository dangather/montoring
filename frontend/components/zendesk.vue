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

    <titlebar>
        Outages
    </titlebar>
    <div class="flex mt-5 items-center flex-col justify-center">
        <outage date="12/12/23" address="192.168.1.1">
            this is an outage
        </outage>
        <outage date="13/12/23" address="www.amazon.co.uk">
            this is another outage
        </outage>        
        <outage date="11/05/25" address="14.254.255.2">
            Lsdsdsdsdds
        </outage>
    </div>
    
    
</template>

<script setup lang="ts">
import zcards from "/components/cards/zcards.vue"
import titlebar from "./titlebar.vue"
import outage from "./cards/outage.vue"
</script>
