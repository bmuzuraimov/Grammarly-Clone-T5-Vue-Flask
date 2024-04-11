<template>
  <div class="h-screen w-full flex flex-row">
    <aside class="h-full border-r bg-white space-y-8">
      <div class="flex flex-col h-full">
        <div class="h-20 flex justify-center items-center px-4">
          <h2>COMP3065</h2>
        </div>
        <div class="flex-1 flex flex-col h-full overflow-auto">
          <h4 class="px-4 text-sm font-medium">Grammar Corrections</h4>
            <div v-if="loadingGrammar" class="text-center my-4">
            <v-progress-circular :size="50" color="primary" indeterminate></v-progress-circular>
          </div>
          <ul class="px-4 text-sm font-medium flex-1">
            <li v-for="(item, idx) in corrections" :key="idx">
              {{ (item as any).output_text }}
            </li>
          </ul>
          <button
            @click="checkGrammar"
            class="px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 active:bg-gray-100 duration-150"
          >
            <span>Check for Grammar</span>
          </button>
          <div>
            <div class="py-4 px-4 border-t">
              <div class="flex items-center gap-x-4">
                <div>
                  <span class="block text-gray-700 text-sm font-semibold">MUZURAIMOV Baiel</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </aside>
    <main class="p-16">
      <h2 class="text-2xl font-semibold text-gray-500 text-center">Text Editor</h2>
      <EditorContent :editor="editor || undefined" v-if="editor" class="h-screen w-full" />
    </main>
  </div>
</template>
<!-- <script lang="ts">
import { Editor, EditorContent, useEditor } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import { defineComponent } from '@vue/runtime-core'

export default defineComponent({
  components: {
    EditorContent,
  },
  setup() {
    const editor = useEditor({
      content: '<p>I’m running tiptap with Vue.js. 🎉</p>',
      extensions: [
      ],
    })
    return {
      editor
    }
  }
});
</script> -->
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
    EditorContent,
  },

  setup() {
    const editor = useEditor({
        extensions: [Document, Paragraph, Text, Code, Typography],
        content: `
          <p>He goed to the store yesterday and buyed some apple.</p>
          <p>Me and her is going to the cinemas tonight to watch a moovie.</p>
          <p>The mans in the park was playing football and haves a lot of fun.</p>
          <p>I eated a sandvich for lunch, but it was not very tasteful.</p>
          <p>She don't likes to swimm in the oshun because she is afraided of sharks.</p>
        `
      });
    const corrections = ref<unknown[]>([])
    const loadingGrammar = ref(false)

    const checkGrammar = async () => {
      loadingGrammar.value = true
      corrections.value = []
      const content = editor.value?.getText() || ''
      const sentences = content.match(/[^.!?]+[.!?]+/g) || []
      try {
        const fetchPromises = sentences.map(async (text) => {
          const response = await fetch('http://127.0.0.1:5000/process_text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
          })
          return response.json()
        })
        corrections.value = await Promise.all(fetchPromises)
      } catch (error) {
        console.error('Grammar check failed:', error)
      } finally {
        loadingGrammar.value = false
      }
    }

    onUnmounted(() => {
      editor.value?.destroy()
    })

    return {
      editor,
      corrections,
      loadingGrammar,
      checkGrammar,
    }
  }
})
</script>



<style lang="scss">
/* Enhanced editor styles for full page width and height with padding */
.tiptap {
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

/* Style adjustments for responsiveness */
@media (max-width: 768px) {
  .tiptap {
    padding: 10px; /* Adjust padding on smaller screens */
    height: calc(100vh - 20px); /* Adjust height for smaller screens */
  }
}
</style>
