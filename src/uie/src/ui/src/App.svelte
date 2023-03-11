<script lang="ts">
  // @ts-ignore
  import { autoresize } from 'svelte-textarea-autoresize'
  import axios from 'axios'
  import { RingLoader } from 'svelte-loading-spinners'
  import { JSONEditor } from 'svelte-jsoneditor'
  import { Button, Dialog, Modal } from 'attractions'

  let openM = false
  let text: string = ''
  let schema: {
    json?: (string | { [key: string]: string[] })[]
    text?: string
  } = {
    json: ['时间', '选手', '赛事名称'],
    text: '["时间", "选手", "赛事名称"]',
  }

  let loading = false

  interface R {
    [key: string]: {
      text: string
      probability: number
      relations?: R
    }[]
  }

  let results: R = {}

  const parseText = async () => {
    console.log(schema)

    loading = true
    try {
      const { data } = await axios.post('http://localhost:12345/post', {
        data: [{ text }],
        parameters: { schema: JSON.parse(schema.text) },
        execEndpoint: '/',
      })
      const r = data?.data[0].text
      results = JSON.parse(r.replaceAll("'", '"'))[0]
    } finally {
      loading = false
    }
  }

  const parseR = (r: R) => {
    const s: {
      meta: string
      text: string
      probability: number
    }[] = []
    for (const k in r) {
      const v = r[k]

      s.push(
        ...v.map((v) => {
          if (v.relations) {
            s.push(...parseR(v.relations))
          }
          return {
            ...v,
            meta: k,
          }
        })
      )
    }
    return s
  }

  $: loading
</script>

<br />
<div class="container">
  <Modal bind:open={openM} let:closeCallback>
    <Dialog title="Schema 编辑" {closeCallback}>
      <JSONEditor bind:content={schema} />
    </Dialog>
  </Modal>
  <br />
  <div>
    <div
      style="display: flex; flex-direction: row; justify-content: space-between;align-items: center; width: 61.8%; margin: 0 auto;"
    >
      <Button
        style="
          display: flex; 
          justify-content: center;
          --un-gradient: 45deg,#41D1FF,#BD34FE;
          background-image: linear-gradient(var(--un-gradient, var(--un-gradient-stops, rgba(255, 255, 255, 0))));
          --un-text-opacity: 1;
          color: rgba(255,255,255,var(--un-text-opacity));
          width: 100px;
        "
        on:click={() => (openM = !openM)}>Schema</Button
      >
      <h1>Jina X PaddleUIE 可视化信息抽取</h1>
      <Button
        style="
          display: flex; 
          justify-content: center;
          --un-gradient: 45deg,#41D1FF,#BD34FE;
          background-image: linear-gradient(var(--un-gradient, var(--un-gradient-stops, rgba(255, 255, 255, 0))));
          --un-text-opacity: 1;
          color: rgba(255,255,255,var(--un-text-opacity));
          width: 100px;
        "
        on:click={parseText}>Parse</Button
      >
    </div>
  </div>

  <br />

  <div>
    <textarea
      class="textarea"
      placeholder="请输入文本 | 按动右上角按钮进行解析🔍"
      bind:value={text}
      on:keypress={parseText}
      use:autoresize
    />
  </div>

  {#if !loading}
    <div class="wordlist">
      {#each parseR(results) as item}
        <div class="word">
          <div class="item">{item.text}</div>
          <div class="termid">{item.meta}</div>
          <div class="label">{item.probability}</div>
        </div>
      {/each}
    </div>
  {:else}
    <br />
    <div class="loading">
      <!-- <div>正在智能解析中</div> -->
      <RingLoader size="60" color="#006eff" unit="px" duration="1s" />
    </div>
  {/if}
</div>

<style>
  @font-face {
    font-family: 'oppo';
    src: url('/OPPOSans-M.ttf');
    font-weight: normal;
    font-style: normal;
  }

  .textarea {
    resize: none;

    box-sizing: border-box;
    margin: 0;
    font-variant: tabular-nums;
    list-style: none;
    font-feature-settings: 'tnum', 'tnum';
    position: relative;
    display: inline-block;
    width: 100%;
    min-width: 0;
    padding: 4px 11px;
    color: rgba(0, 0, 0, 0.85);
    font-size: 14px;
    background-color: #fff;
    background-image: none;
    border: 1px solid #d9d9d9;
    border-radius: 2px;
    transition: all 0.3s;
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-radius: 16px;
    color: #666;
    font-size: 14px;
    line-height: 35px;
    font-weight: 400;
    outline: none;
    text-align: left;
  }

  .textarea:focus {
    border-color: rgba(82, 168, 236, 0.8);
    outline: 0;
    outline: thin dotted \9;
    -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075),
      0 0 8px rgba(82, 168, 236, 0.6);
    -moz-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075),
      0 0 8px rgba(82, 168, 236, 0.6);
    box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075),
      0 0 8px rgba(82, 168, 236, 0.6);
  }

  .word {
    display: block;
    margin-top: 24px;
    background: rgba(140, 161, 219, 0.4);
    border-radius: 4px;
    padding: 8px 24px;
    text-align: center;
    margin-right: 11px;
    box-shadow: 0px 1px 2px rgba(47, 100, 141, 0.4);
    border-radius: 5px;
    display: flex;
    flex-direction: column;
    line-height: 200%;
    transition: all 0.3s;
  }

  .word:hover {
    box-shadow: 0 8px 17px 2px rgb(47 100 141 / 14%),
      0 3px 14px 2px rgb(47 100 141 / 12%), 0 5px 5px -3px rgb(47 100 141 / 20%);
  }

  .wordlist {
    display: flex;
    flex-wrap: wrap;
  }

  .container {
    font-family: oppo;
  }

  .item {
    font-weight: 800;
    font-size: 16px;
  }

  .label {
    color: rgb(0, 0, 0, 0.7);
  }

  .termid {
    color: rgb(0, 81, 255);
  }

  .loading {
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>
