<template >
    <div class="grid gap-x-52 grid-cols-3 border align-middle text-center rounded-md mt-3 py-5 w-[65%] bg-red-500 border-red-400">
        <p class=" text-3xl text-white"><slot/></p>
        <p class=" text-3xl text-white">{{ props.address }}</p>
        <p class=" text-3xl text-white">{{  props.date }}</p>
       
    </div>
</template>
<script setup lang="ts">
const props = defineProps({
    address: String,
    date: String,
})
</script>
