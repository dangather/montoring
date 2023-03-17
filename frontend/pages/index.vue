<template>
    <div class="lg:grid lg:grid-cols-3 md:grid-cols-1 transition-all duration-200 ease-in-out lg:gap-5 m-5 min-h-screen">
        <div v-for="i, k in final" :key="k">
            <div class="bg-gray-200 text-center rounded-xl h-full border-4" :class="i.value == 'success' ?  'border-green-500' : ' border-red-500'">
                <p class="text-xl py-5 font-bold">
                    {{ i.name }}
                </p>
                <p class="text-8xl pt-28 ">
                    {{ i.value }}
                </p>         
            </div>
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
