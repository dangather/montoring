<template>
    <titlebar>Service checks</titlebar>
    <div class="grid grid-cols-2 transition-all duration-200 ease-in-out gap-5 m-5 mt-20 h-[75vh]">
        <div v-for="i, k in final" :key="k">
            <div class="bg-gray-200 text-center mt-50 rounded-xl h-full border-4" :class="i.value == 'success' ?  'border-green-500' : ' border-red-500'">
                <p class="text-3xl pt-10 font-bold">
                    {{ i.name }}
                </p>
                <p class="grid h-[70%] text-7xl place-items-center">
                    {{ i.value }}
                </p>         
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import titlebar from "../titlebar.vue";
import {getdata, datafetch, connect} from "../../scripts/utils";
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