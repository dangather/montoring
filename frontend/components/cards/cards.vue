<template>
    <titlebar>Service checks</titlebar>
    <div class="grid grid-cols-2 transition-all duration-200 ease-in-out gap-5 m-5 h-[50vh] min-w-[50vw]">
        <div v-for="i, k in final" :key="k">
            <div class="shadow-md text-center mt-50 rounded-xl h-[25vh]" :style="i.value == 'success' ?  'border-top: 8px solid green' : 'border-bottom: 8px solid red'">
                <p class="text-3xl pt-10 font-bold">
                    {{ i.name }}
                </p>
                <p class="grid h-[50%] text-7xl place-items-center">
                    {{ i.value }}
                </p>         
            </div>
            <graphs/>
        </div>
    </div>
</template>

<script setup lang="ts">
import titlebar from "../titlebar.vue";
import {getdata, datafetch, connect} from "../../scripts/utils";
import graphs from "../graphs.vue";
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