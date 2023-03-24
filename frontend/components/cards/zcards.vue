<template>
    <div class="border max-w-[75%] shadow m-5 w-fit px-10 rounded-xl pb-5" :style="borderl">
        <div class="text-5xl py-3" :style="styleObject">{{ props.title }}</div>
        <div class="text-5xl">
            <p><slot/></p>
        </div>
    </div>
</template>

<script setup>
const props = defineProps( {
    title: String,
    colour: String,
    border: String
})

const styleObject = ref({
  color: props.colour,
})

const borderl = ref({
    borderLeft: props.border
})

</script>