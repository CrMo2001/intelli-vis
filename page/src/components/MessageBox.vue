<script setup lang="ts">
import { ElIcon, ElText } from 'element-plus'
import { Loading, View } from '@element-plus/icons-vue'
import { nextTick, onMounted, ref } from 'vue'

type Message = {
  content: string;
  sender: "user" | "assistant";
  attachment: string | null;
}

const messages = ref<Message[]>([])
const messageContainer = ref<HTMLElement | null>(null)
const isLoading = ref(false)

const scrollToBottom = () => {
  if (messageContainer.value) {
    console.log("scrollToBottom", messageContainer.value.scrollHeight)
    nextTick(() => {
      messageContainer.value!.scrollTop = messageContainer.value!.scrollHeight
    })
  }
}

function addMessage(message: Message) {
  messages.value.push(message)
  scrollToBottom()
  // console.log(message)
}

function setLoading(loading: boolean) {
  isLoading.value = loading
  scrollToBottom()
}

defineExpose({
  addMessage,
  setLoading,
})

const emits = defineEmits<{
  (e: 'openAttachment', content: string): void;
}>()

</script>

<template>
  <div class="message-content" ref="messageContainer">
    <div v-for="(message, index) in messages" :key="index" :class="['message', 'message-' + message.sender]">
      <div class="message-content">{{ message.content }}
        <div v-if="message.attachment != null" class="message-attachment">
          <!-- link to view the attachement -->
          <button class="message-attachment-button" @click="() => emits('openAttachment', message.attachment!)">
            <el-icon style="margin-right: 0.5vh;">
              <View />
            </el-icon>
            <span>查看附件</span>
          </button>
        </div>
      </div>
    </div>
    <div class="loading-container" v-if="isLoading">
      <div>正在生成回复...</div>
      <el-icon class="is-loading">
        <Loading />
      </el-icon>
    </div>
  </div>
</template>

<style scoped>
.message-content {
  width: 100%;
  height: 100%;
  overflow-y: auto;

  padding: 1vh;
  box-sizing: border-box;
}

.message {
  margin: 1vh 2vh;
  border-radius: 1vh;
  font-size: 1.5vh;
  max-width: 70%;
  width: fit-content;
  font-weight: normal;
}

.message-user {
  background-color: var(--color-dark);
  color: var(--color-light);
  margin-left: auto;
}

.message-assistant {
  background-color: var(--color-light);
  color: var(--color-dark);
}

.message-attachment {
  margin-top: 1vh;
  font-size: 1.5vh;
}

.message-attachment-button {
  padding: 0.5vh 1.5vh;
  height: 100%;
  border-radius: 1vh;

  background-color: transparent;
  color: var(--color-dark);
  border: 1.5px solid var(--color-dark);
  font-size: 1.5vh;
  font-weight: bold;

  transition: all 0.3s ease;
}

.message-attachment-button:hover {
  background-color: var(--color-dark);
  color: var(--color-light);
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1vh;
  font-size: 1.5vh;
  color: var(--color-light)
}
</style>