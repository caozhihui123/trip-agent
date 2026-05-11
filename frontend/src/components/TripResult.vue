<script setup lang="ts">
import { ref, computed } from 'vue'
import { Card } from 'ant-design-vue'
import MapPanel from './MapPanel.vue'
import DayCard from './DayCard.vue'
import BudgetPanel from './BudgetPanel.vue'
import ExportToolbar from './ExportToolbar.vue'
import type { TripPlan } from '../types'

const props = defineProps<{ plan: TripPlan }>()
const activeDay = ref(0)

const allDays = computed(() => props.plan.schedule || [])
</script>

<template>
  <div class="trip-result" id="trip-result-content">
    <div class="result-header">
      <h2>{{ plan.city }} · {{ plan.days }} 天旅行计划</h2>
      <ExportToolbar :plan="plan" />
    </div>

    <div class="content-layout">
      <div class="left-panel">
        <Card size="small" style="margin-bottom: 12px">
          <div v-if="plan.weather && plan.weather.length" class="weather-bar">
            <span v-for="w in plan.weather" :key="w.date" class="weather-day">
              {{ w.date.slice(5) }} {{ w.day_weather }} {{ w.day_temp }}°C
            </span>
          </div>
          <div v-if="plan.tips && plan.tips.length" class="tips-bar">
            提示：{{ plan.tips.join('；') }}
          </div>
        </Card>

        <div class="day-nav">
          <div
            v-for="(d, i) in allDays"
            :key="i"
            :class="['day-nav-item', { active: activeDay === i }]"
            @click="activeDay = i"
          >
            第 {{ d.day }} 天
          </div>
        </div>

        <div
          v-for="(d, i) in allDays"
          :key="i"
          :data-day-index="i"
          :style="{ display: activeDay === i ? '' : 'none' }"
        >
          <DayCard :day="d" />
        </div>
      </div>

      <div class="right-panel">
        <MapPanel :plan="plan" :active-day="activeDay" />
        <BudgetPanel :budget="plan.budget" :days="plan.days" :hotel="plan.hotel" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.trip-result {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}
.result-header h2 {
  margin: 0;
  font-size: 22px;
}
.content-layout {
  display: flex;
  gap: 16px;
}
.left-panel {
  flex: 1;
  min-width: 0;
}
.right-panel {
  width: 480px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.weather-bar {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
.weather-day {
  font-size: 13px;
  color: #666;
}
.tips-bar {
  font-size: 13px;
  color: #fa8c16;
  margin-top: 6px;
}
.day-nav {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
.day-nav-item {
  padding: 8px 20px;
  border-radius: 6px;
  background: #f0f0f0;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}
.day-nav-item:hover {
  background: #d6e4ff;
}
.day-nav-item.active {
  background: #1677ff;
  color: #fff;
}
@media (max-width: 1024px) {
  .content-layout {
    flex-direction: column;
  }
  .right-panel {
    width: 100%;
  }
}
</style>
