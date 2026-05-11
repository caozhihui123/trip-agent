<script setup lang="ts">
import { ref } from 'vue'
import TripForm from './components/TripForm.vue'
import TripResult from './components/TripResult.vue'
import type { TripPlan } from './types'

const tripPlan = ref<TripPlan | null>(null)
const loading = ref(false)

function onPlanGenerated(plan: TripPlan) {
  tripPlan.value = plan
}
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <h1>智能旅行助手</h1>
      <p>AI 驱动的中国城市旅行规划</p>
    </header>

    <TripForm
      :loading="loading"
      @update:loading="(v: boolean) => loading = v"
      @plan-generated="onPlanGenerated"
    />

    <TripResult
      v-if="tripPlan"
      :plan="tripPlan"
    />
  </div>
</template>

<style scoped>
.app-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
}
.app-header {
  text-align: center;
  margin-bottom: 24px;
}
.app-header h1 {
  font-size: 28px;
  color: #1a1a2e;
  margin: 0;
}
.app-header p {
  color: #666;
  margin: 4px 0 0;
}
</style>
