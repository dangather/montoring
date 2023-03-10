<template>
    <div class="text-center pt-5">
        <p v-if="data != null" v-for="f, i in names" key="i">{{ f }} : {{  res[i] }}</p>
        <p v-else>no data sorry!</p>
    
    </div>
</template>

<script setup lang="ts">

import {getdata, datafetch} from "../scripts/utils"
let data = await datafetch("name")
let names: string[] = []

let res: string[] = []
for(let i = 0; i < data!.length; i++) {
    console.log(data![i])
    //@ts-ignore
    names.push(data![i]["name"])
    res.push(await getdata("result", "name", names[i]))
}
</script>