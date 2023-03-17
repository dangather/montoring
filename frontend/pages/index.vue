<template>
    <div class="pt-5 block text-center">
        <div id="data" v-for="i, k in final" :key="k">
            <div v-if="data != null">
                <p>{{ i.name }}</p> <p>{{  i.value }}</p>
            </div>
            <div v-else>no data sorry!</div>
        </div>
    </div>
</template>

<script setup lang="ts">
import {getdata, datafetch, connect} from "../scripts/utils";
const sb = connect();
let items: any = []
let data = await datafetch("name")
let names: any[] = []
let res: any[] = []
let final: any = ref([])


for(let i = 0; i < data!.length; i++) {
    //@ts-ignore
    names.push(data![i]["name"])

    res.push(await getdata("result", "name", names[i]))
  
    final.value.push({name: names[i], value: res[i]})
} 

sb.channel("any").on("postgres_changes", {event: "INSERT", schema: "public", table: "logs"}, async () => {
    let data = await datafetch("name")
    let names: any[] = []
    let items: any[] = []
    let res: any[] = []
    console.log("event captured. site updated")
    for(let i = 0; i < data!.length; i++) {
        //@ts-ignore
        names.push(data![i]["name"])
        res.push(await getdata("result", "name", names[i]))
        items.push({name: names[i], value: res[i]})
    }
    console.log(names,res,items)
    final.value = []
    final.value.push(...items)
    console.log(final.value)

}).subscribe()

</script>