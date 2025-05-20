<script setup lang="ts">
import { marked } from 'marked';
import { ArrowLeft, Download } from '@element-plus/icons-vue';
import html2pdf from 'html2pdf.js';
// const props = defineProps<{
//   content: string;
// }>();

function setMarkdownContent(content: string) {
  const container = document.getElementById('markdown-content');
  // compile markdown use marked library
  const html = marked(content, {
    async: false,
  });
  // set html to container
  if (container) {
    container.innerHTML = html;
  }
}

function download() {
  const container = document.getElementById('markdown-content');
  if (!container) return;
  const options = {
    margin: 10,
    filename: '报告.pdf',
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2 },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
    // pagebreak: {
    //   mode: ['avoid-all', 'css', 'legacy'],
    //   avoid: ['tr', 'p', 'div', 'h1', 'h2', 'h3'] // 避免这些元素被分页
    // }
  };
  const result = html2pdf()
    .from(container)
    .set(options)
    // .toPdf()
    // .get('pdf')
    .save('report.pdf');
}

const emits = defineEmits<{
  (e: 'close'): void;
}>();

defineExpose({
  setMarkdownContent,
});

</script>

<template>
  <div class="report-container">
    <div class="report-tool">
      <button class="report-tool-button" @click="() => emits('close')">
        <el-icon>
          <ArrowLeft />
        </el-icon>
        <el-text>返回</el-text>
      </button>
      <button class="report-tool-button" @click="download">
        <el-icon>
          <Download />
        </el-icon>
        <el-text>下载</el-text>
      </button>
    </div>
    <div id="markdown-content" class="report-content"></div>
  </div>
</template>

<style>
.report-container {
  /* width: 100vw; */
  min-height: 100vh;

  position: absolute;
  top: 0;
  left: 0;

  /* overflow: scroll; */
  background-color: var(--color-dark);
  color: var(--color-light);
}

.report-tool {
  position: fixed;
  top: 2vh;
  left: 2vh;

  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 2vh;
}

.report-tool-button {
  /* display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1vh; */

  padding: 1vh 2vh;
  border-radius: 100%;
  border: 1.5px solid var(--color-light);

  background-color: var(--color-light);
  color: var(--color-dark);
  font-size: 1.5vh;
  font-weight: bold;

  transition: all 0.3s ease;
}

.report-tool-button:hover {
  background-color: var(--color-dark);
  color: var(--color-light);
}

.report-content {

  padding: 2vh 10%;

  img {
    width: 75%;
    padding-left: 12.5%;
  }

  p,
  h1,
  h2,
  h3,
  table,
  div {
    /* page-break-inside: avoid; */
    /* position: relative; */
    /* top: 2px; */
  }

  .keep-together {
    page-break-inside: avoid;
  }

  .page-break-before {
    page-break-before: always;
  }

  .page-break-after {
    page-break-after: always;
  }
}
</style>