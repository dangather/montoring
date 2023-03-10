<template>
    <div class="text-center">
        {{ data }}
    </div>
</template>

<script setup lang="ts">
function getdata(){
    const sb = useSupabaseClient();
    return sb;
}
const data = getdata();
</script>

<style lang="">
    
</style>