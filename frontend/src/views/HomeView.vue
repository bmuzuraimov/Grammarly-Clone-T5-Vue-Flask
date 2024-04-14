<template>
  <div class="w-full grid grid-cols-5 gap-3">
    <main class="p-16 col-span-4 w-full">
      <input
        type="text"
        value="Untitled document"
        class="text-2xl font-semibold text-gray-500 text-center focus:outline-none px-2 transition duration-150"
      />
      <editor-content :editor="editor" />
    </main>
    <aside class="fixed top-0 right-0 h-screen w-96 border-l">
      <button
        @click="checkGrammar"
        class="px-4 py-2 text-md w-full font-medium text-green-600 bg-green-50 hover:bg-green-100 active:bg-gray-100 duration-150"
      >
        <span>Check for Grammar</span>
      </button>
      <div class="fixed bottom-0 w-full flex items-center gap-x-4 py-4 px-4 border-t">
        <div>
          <span class="block text-gray-700 text-sm font-semibold">MUZURAIMOV Baiel</span>
        </div>
      </div>
      <div class="h-20 flex justify-center items-center px-4">
        <h2>COMP3065 Project</h2>
      </div>
      <div class="flex-1 flex flex-col overflow-auto">
        <h4 class="px-4 text-lg font-medium">Grammar Corrections</h4>
        <div v-if="loadingGrammar" class="text-center my-4">
          <v-progress-circular :size="50" color="success" indeterminate></v-progress-circular>
        </div>
        <transition-group name="list" tag="ul">
          <ul class="px-4 text-md font-medium flex-1">
            <li v-for="(item, idx) in corrections" :key="idx">
              <p
                class="border rounded-md border-amber-400 p-2 mb-2 hover:border-amber-600 hover:bg-green-50 animated-item"
                v-html="item"
              ></p>
            </li>
          </ul>
        </transition-group>
      </div>
    </aside>
  </div>
</template>
<script lang="ts">
import { ref, onUnmounted } from 'vue'
import { defineComponent } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'

import Document from '@tiptap/extension-document'
import Paragraph from '@tiptap/extension-paragraph'
import Text from '@tiptap/extension-text'
import Code from '@tiptap/extension-code'
import Typography from '@tiptap/extension-typography'

export default defineComponent({
  components: {
    EditorContent
  },

  setup() {
    const editor = useEditor({
      extensions: [Document, Paragraph, Text, Code, Typography],
      content: `
          <p>He goed to the store yesterday and buyed some apple.</p>
          <p>Me and her is going to the cinemas tonight to watch a moovie.</p>
          <p>The mans in the park was playing football and haves a lot of fun.</p>
          <p>I eated a sandvich for lunch, but it was not very tasteful.</p>
          <p>She don't likes to swimm in the ocean because she is afraided of sharks.</p>
        `
    })
    const corrections = ref<unknown[]>([])
    const loadingGrammar = ref(false)
    const checkGrammar = async () => {
      loadingGrammar.value = true
      corrections.value = []
      const content = editor.value?.getText() || ''
      const sentences = content.match(/[^.!?]+[.!?]+/g) || []
      try {
        const fetchPromises = sentences.map(async (text) => {
          const response = await fetch('http://127.0.0.1:5001/api/process_text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
          })
          const data = await response.json()

          // Assuming `data` includes a `correctedText` field with corrections
          if (data.output_text) {
            // Find differences and wrap them in a span
            const diff = getDifferences(text, data.output_text)
            return diff
          }
          return text
        })
        corrections.value = await Promise.all(fetchPromises)
      } catch (error) {
        console.error('Grammar check failed:', error)
      } finally {
        loadingGrammar.value = false
      }
    }

    // A function to find differences and wrap them in span tags
    function getDifferences(originalText: string, correctedText: string) {
      console.log(originalText, correctedText)
      const originalWords = originalText.split(' ')
      correctedText = correctedText.replace('correct: ', '')
      const correctedWords = correctedText.split(' ')
      const maxLength = Math.max(originalWords.length, correctedWords.length)
      let markedText = ''

      for (let i = 0; i < maxLength; i++) {
        let original = originalWords[i] || ''
        let corrected = correctedWords[i] || ''
        original = original.trim()
        corrected = corrected.trim()

        if (original !== corrected) {
          markedText += `<strike>${original}</strike> `
          markedText += `<span style="color: red;">${corrected}</span> `
        } else {
          markedText += `${original} `
        }
      }
      return markedText.trim()
    }

    onUnmounted(() => {
      editor.value?.destroy()
    })

    return {
      editor,
      corrections,
      loadingGrammar,
      checkGrammar
    }
  }
})
</script>

<style lang="scss">
/* Enhanced editor styles for full page width and height with padding */
.tiptap {
  width: 100%;
  font-family: 'Segoe UI', Arial, sans-serif; /* Clean, readable font */
  color: #4a4a4a; /* Soft, dark text color for readability */
  line-height: 1.6; /* Increased line height for readability */
  padding: 20px; /* Padding around the editor content */
  height: calc(100vh - 40px); /* Full viewport height minus padding */
  overflow-y: auto; /* Allow scrolling for content exceeding the viewport */
  box-sizing: border-box; /* Include padding in the calculated height */

  > * + * {
    margin-top: 0.75em; /* Consistent spacing between elements */
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    margin-top: 1.5em; /* Space above headings for clear section breaks */
    line-height: 1.1;
    color: #1a1a1a; /* Darker color for headings */
  }

  p {
    font-size: 1.2em; /* Larger font size for paragraphs */
    margin-bottom: 1em; /* Space out paragraphs */
  }

  code {
    background-color: rgba(97, 97, 97, 0.1);
    color: #616161;
    padding: 0.25em 0.5em; /* Padding for code blocks */
    border-radius: 4px; /* Rounded edges for code blocks */
    font-family: 'Courier New', Courier, monospace; /* Monospaced font for code */
  }

  a {
    color: #0077cc; /* Color for links */
    text-decoration: none; /* No underline to keep text clean */
    &:hover {
      text-decoration: underline; /* Underline on hover */
    }
  }

  ul,
  ol {
    margin-left: 20px; /* Indent lists */
    padding-left: 0;
  }

  blockquote {
    margin: 1em 0;
    padding-left: 1em;
    border-left: 3px solid rgba(0, 0, 0, 0.1); /* Visual cue for quotations */
    font-style: italic; /* Italicize quotes */
  }

  .color {
    white-space: nowrap;

    &::before {
      content: ' ';
      display: inline-block;
      width: 1em;
      height: 1em;
      border: 1px solid rgba(128, 128, 128, 0.3);
      vertical-align: middle;
      margin-right: 0.1em;
      margin-bottom: 0.15em;
      border-radius: 50%; /* Round shapes for a modern look */
      background-color: var(--color);
    }
  }
}
.tiptap:focus {
  outline: none; /* Remove focus outline for a cleaner look */
}

/* Style adjustments for responsiveness */
@media (max-width: 768px) {
  .tiptap {
    padding: 10px; /* Adjust padding on smaller screens */
    height: calc(100vh - 20px); /* Adjust height for smaller screens */
  }
}

@keyframes rotateX {
  from {
    transform: rotateX(-90deg);
    opacity: 0;
  }
  to {
    transform: rotateX(0deg);
    opacity: 1;
  }
}

.animated-item {
  animation: rotateX 1s ease-out forwards;
}
</style>
