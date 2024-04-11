<template>
  <aside class="h-full border-r bg-white space-y-8">
    <div class="flex flex-col h-full">
      <div class="h-20 flex justify-center items-center px-4">
        <h2>COMP3065</h2>
      </div>
      <div class="flex-1 flex flex-col h-full overflow-auto">
        <ul class="px-4 text-sm font-medium flex-1">
          <li v-for="(item, idx) in corrections" :key="idx">
            <a
              :href="item.href"
              class="flex items-center gap-x-2 text-gray-600 p-2 rounded-lg hover:bg-gray-50 active:bg-gray-100 duration-150"
            >
              <div class="text-gray-500" v-html="item.icon"></div>
              {{ item.name }}
            </a>
          </li>
        </ul>
        <button class="px-4 py-2 text-sm font-medium text-gray-600 hover:bg-gray-50 active:bg-gray-100 duration-150">
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
</template>
  
  <script lang="ts">
export default {
  name: 'SidebarComponent',
  data() {
    return {
      corrections: [

      ],
      navsFooter: [

      ]
    }
  }
}
</script>
  