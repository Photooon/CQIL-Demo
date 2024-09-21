<template>
  <CQIL msg="Welcome to Your Vue.js App" class="CQIL"/>
</template>

<script>
import CQIL from './components/CQIL.vue'

export default {
  name: 'App',
  components: {
    CQIL
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.CQIL {
  background-color: aquamarine;
}
</style>
