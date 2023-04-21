<template >
    <div class="grid text-3xl text-white gap-x-52 grid-cols-3 border align-middle text-center rounded-md mt-3 py-5 w-[65%] bg-red-500 border-red-400">
        <p><slot/></p>
        <p>{{ props.address }}</p>
        <p>{{  props.date }}</p>
       
    </div>
</template>
<script setup lang="ts">
const props = defineProps({
    address: String,
    date: String,
})
</script>
