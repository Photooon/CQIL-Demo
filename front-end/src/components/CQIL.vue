<template>
  <div class="headContainer">
    <h2>🤖大模型加速Demo</h2>
    <select v-model="selectedModel">
      <option value="base">基准模型</option>
      <option value="cqil">CQIL加速模型</option>
    </select>
  </div>
  <div class="mainContainer">
    <div v-for="item in dialogs" v-bind:key="item.id">
      <div v-if="item.character === 'llm'" class="Row llmRow">
        <img class="characterImg" src="../assets/llm.jpeg" mode="widthFix"/>
        <text class="text llmBackground">{{item.text}}</text>
      </div>
      <div v-if="item.character === 'system'" class="Row systemRow">
        <text class="sysText systemBackground">{{item.text}}</text>
      </div>
      <div v-if="item.character === 'human'" class="Row humanRow">
        <img class="characterImg" src="../assets/human.png" mode="widthFix"/>
        <text class="text humanBackground">{{item.text}}</text>
      </div>
    </div>
  </div>
  <div class="inputContainer">
    <input type="text" v-model="inputText" placeholder="输入文本" @keyup.enter="handleSubmit"/>
    <button @click="handleSubmit">🛫</button>
  </div>
</template>

<script>
export default {
  name: 'CQIL',
  props: {
    msg: String
  },
  data() {
    return {
      "dialogs": [
        {
          "character": "llm",
          "text": "这里是邓仰东老师实验室自建的大模型对话系统，请问有什么可以帮到您？"
        },
        {
          "character": "system",
        }
      ],
      "inputText": '',
      "selectedModel": 'base',
      "startTime": null
    }
  },
  methods: {
    handleSubmit() {
      if (this.inputText.trim() !== '') {
        // 这里可以添加提交文本的处理逻辑
        this.dialogs.push({
          "character": "human",
          "text": this.inputText
        })
        // 触发处理函数
        this.handleFunction();
      }
      // 清空文本框
      this.inputText = '';
    },
    handleFunction() {
      this.startTime = performance.now()
      this.socket.send(JSON.stringify({"prompt": this.inputText, "selected_model": this.selectedModel}))
    }
  },
  mounted() {
    this.socket = new WebSocket("ws://localhost:9000/generate_text/");
    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log(data)
      if (data.isStart) {
        this.dialogs.push({
          "character": "llm",
          "text": data.char
        })
      } else {
        this.dialogs[this.dialogs.length - 1].text += data.char;
        if (data.isEnd) {
          const timecost = performance.now() - this.startTime;
          const textLen = this.dialogs[this.dialogs.length - 1].text.length
          this.dialogs.push({
            "character": "system",
            "text": "速度：" + (textLen / (timecost / 1000)).toFixed(1) + "字/秒"
          })
        }
      }
    }
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.close();
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.headContainer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 65%;
  margin: 0 auto;
}

h2 {
  text-align: left;
}

select {
  font-size: 18px;
  text-align: right;
  border: 0px;
  outline: none;
}

.mainContainer {
  max-width: 65%;
  margin: 0 auto;
  overflow-y: auto;
  height: calc(100vh - 100px - 50px - 20px);
}

.Row {
  display: flex;
  align-items: center;
  position: relative;
}

.llmRow {
  text-align: left;
  position: relative
}

.systemRow {
  text-align: left;
  position: relative;
  padding-left: 70px;
  padding-bottom: 20px;
}

.humanRow {
  text-align: right;
  position: relative;
  flex-direction: row-reverse;
  padding-bottom: 20px;
}

.characterImg {
  width: 50px;
  height: auto;
  border-radius: 50%;
  padding-left: 10px;
  padding-right: 10px;
}

.text {
  font-size: 18px;
  max-width: 50%;
  display: table;
  height: 30px;
  padding: 10px 10px;
  line-height: 30px;
  border-radius: 5px;
  overflow-wrap: anywhere;
  text-align: left;
}

.sysText {
  font-size: 12px;
}

.llmBackground {
  background-color: rgb(235, 232, 232);
}

.systemBackground {
  background-color: white;
}

.humanBackground {
  background-color: rgb(235, 232, 232);
}

.inputContainer {
  min-height: 50px;
  position: fixed;
  bottom: 20px;
  left: 20%;
  right: 20%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #f1f1f1;
  border-radius: 10px;
  box-shadow: 0 -2px 4px rgba(0,0,0,0.1);
}

input[type="text"] {
  border: none;
  padding: 16px;
  flex-grow: 1;
  margin-right: 5px;
  border-radius: 10px;
  font-size: 18px;
}

button {
  border: none;
  color: white;
  cursor: pointer;
  font-size: 30px;
}

</style>
