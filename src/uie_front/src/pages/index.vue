<script setup lang="ts" >
import VueJsonPretty from 'vue-json-pretty'
import 'vue-json-pretty/lib/styles.css'
const value = ref(['时间', '选手', '赛事名称'])

const input = ref("")
const result = ref()

const send = async (input:string) => {
  const data = await fetch('http://localhost:12345/post', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ "data": [{ "text": input }],"parameters":{schema:value.value}, "execEndpoint": "/" })
  }).then(response => response.json())
  const r = data?.data[0].text 
  result.value = JSON.parse(r.replaceAll("'", "\""))  
}
</script>

<template>
  <button @click="send(input)">Go!</button>
  <div flex px-6>
   <JsonEditorVue v-model="value" />
   <input v-model="input"/>
  </div>
  <vue-json-pretty :data="result" />
</template>
