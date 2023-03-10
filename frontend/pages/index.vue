<template>
    <div class="text-center pt-5" >
        <div id="data" v-for="i, k in items" :key="k">
            <p v-if="data != null" >
                {{ i.name }} : {{  i.value }}</p>
            <p v-else>no data sorry!</p>
        </div>

    </div>
</template>

<script setup lang="ts">
import {getdata, datafetch, connect} from "../scripts/utils";
const sb = connect();
let items: any = ref([])
let data = await datafetch("name")
let names: string[] = []
let res: string[] = []

for(let i = 0; i < data!.length; i++) {
    //@ts-ignore
    names.push(data![i]["name"])
    res.push(await getdata("result", "name", names[i]))
    items.value.push({name: names[i], value: res[i]})
}
sb.channel("any").on("postgres_changes", {event: "INSERT", schema: "public", table: "logs"}, async () => {

    let data = await datafetch("name")

    let res: string[] = []
    console.log("event captured. site updated")
    for(let i = 0; i < data!.length; i++) {
    //@ts-ignore
    names.push(data![i]["name"])
    res.push(await getdata("result", "name", names[i]))
    document.getElementById("data")?.remove()
    items.value.push({name: names[i], value: res[i]})
    
}

}).subscribe()





</script>