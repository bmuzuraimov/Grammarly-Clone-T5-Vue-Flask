<template>
  <div class="h-screen w-full flex flex-row">
    <aside class="h-full border-r bg-white space-y-8">
      <div class="flex flex-col h-full">
        <div class="h-20 flex justify-center items-center px-4">
          <h2>COMP3065</h2>
        </div>
        <div class="flex-1 flex flex-col h-full overflow-auto">
          <h4 class="px-4 text-sm font-medium">Grammar Corrections</h4>
          <div v-if="loading_grammar" class="text-center my-4">
            <v-progress-circular :size="50" color="primary" indeterminate></v-progress-circular>
          </div>
          <ul class="px-4 text-sm font-medium flex-1">
            <li v-for="(item, idx) in corrections" :key="idx">
              {{ item.output_text }}
            </li>
          </ul>
          <button
            @click="checkGrammar"
            class="px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 active:bg-gray-100 duration-150"
          >
            <span>Check for Grammar</span>
          </button>
          <div>
            <ul class="px-4 pb-4 text-sm font-medium">
              <li v-for="(item, idx) in navsFooter" :key="idx">
                <a
                  :href="item.href"
                  class="flex items-center gap-x-2 text-gray-600 p-2 rounded-lg hover:bg-gray-50 active:bg-gray-100 duration-150"
                >
                  <div class="text-gray-500" v-html="item.icon"></div>
                  {{ item.name }}
                </a>
              </li>
            </ul>
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
      <EditorContent :editor="editor" class="h-screen w-full" />
    </main>
  </div>
</template>

<script lang="ts">
import Code from '@tiptap/extension-code'
import Document from '@tiptap/extension-document'
import Paragraph from '@tiptap/extension-paragraph'
import Text from '@tiptap/extension-text'
import Typography from '@tiptap/extension-typography'
import { Editor, EditorContent } from '@tiptap/vue-3'

import { ColorHighlighter } from './ColorHighlighter.ts'
import { SmilieReplacer } from './SmilieReplacer.ts'

import SidebarComponent from '../components/home/SidebarComponent.vue'

export default {
  components: {
    EditorContent,
    SidebarComponent
  },

  data() {
    return {
      editor: null,
      corrections: [],
      navsFooter: [],
      loading_grammar: false
    }
  },
  methods: {
    async checkGrammar() {
      this.loading_grammar = true
      this.corrections = []
      const content = this.editor.getText()
      // Use regular expressions to split the text into sentences
      const sentences = content.match(/[^.!?]+[.!?]+/g)
      // Create an array of promises for each fetch request
      const fetchPromises = sentences.map(async (text) => {
        const response = await fetch('http://127.0.0.1:5000/process_text', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text })
        })
        const data = await response.json()
        return data
      })
      // Wait for all fetch requests to complete
      const corrections = await Promise.all(fetchPromises)
      // Update the corrections array
      this.corrections = corrections
      this.loading_grammar = false
    }
  },

  mounted() {
    this.editor = new Editor({
      extensions: [Document, Paragraph, Text, Code, Typography, ColorHighlighter, SmilieReplacer],
      content: `
        <p>
          He goed to the store yesterday and buyed some apple.
        </p>
        <p>
          Me and her is going to the cinemas tonight to watch a moovie.
        </p>
        <p>
          The mans in the park was playing football and haves a lot of fun.
        </p>
        <p>
          I eated a sandvich for lunch, but it was not very tasteful.
        </p>
        <p>She don't likes to swimm in the oshun because she is afraided of sharks.</p>
      `
    })
  },

  beforeUnmount() {
    this.editor.destroy()
  }
}
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
