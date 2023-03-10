<template>
    <div class="text-center pt-5">
        {{ names }}
    </div>
</template>

<script setup lang="ts">
import {getdata, fetch} from "../scripts/utils"
let names = fetch("name")
// @ts-ignore


</script>