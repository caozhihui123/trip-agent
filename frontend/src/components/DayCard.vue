<script setup lang="ts">
import { Card, Tag, Empty } from 'ant-design-vue'
import { EnvironmentOutlined, CompassOutlined, CoffeeOutlined } from '@ant-design/icons-vue'
import type { DayPlan } from '../types'

defineProps<{ day: DayPlan }>()
</script>

<template>
  <Card v-if="day" size="small" class="day-card">
    <template #title>
      <span class="day-title">第 {{ day.day }} 天 · {{ day.date }}</span>
    </template>

    <div v-if="!day.attractions?.length && !day.meals?.length" class="empty-day">
      <Empty description="暂无安排" />
    </div>

    <div v-if="day.attractions?.length" class="section">
      <div class="section-title"><EnvironmentOutlined /> 景点</div>
      <div v-for="(a, i) in day.attractions" :key="i" class="attraction-item">
        <div class="attr-index">{{ i + 1 }}</div>
        <div class="attr-info">
          <div class="attr-name">{{ a.name }}</div>
          <div class="attr-detail">{{ a.address }}</div>
          <div class="attr-meta">
            <Tag color="blue" v-if="a.visit_duration">{{ a.visit_duration }}</Tag>
            <Tag color="orange" v-if="a.ticket_price > 0">¥{{ a.ticket_price }}</Tag>
            <Tag v-else color="green">免费</Tag>
          </div>
          <div class="attr-desc" v-if="a.description">{{ a.description }}</div>
        </div>
      </div>
    </div>

    <div v-if="day.routes?.length" class="section">
      <div class="section-title"><CompassOutlined /> 路线</div>
      <div v-for="(r, i) in day.routes" :key="i" class="route-item">
        <Tag :color="r.mode === 'walking' ? 'green' : r.mode === 'driving' ? 'blue' : 'purple'">
          {{ r.mode === 'walking' ? '步行' : r.mode === 'driving' ? '驾车' : '公交' }}
        </Tag>
        <span class="route-info">{{ r.from_place }} → {{ r.to_place }}</span>
        <span class="route-stats">{{ r.distance }} / {{ r.duration }}</span>
      </div>
    </div>

    <div v-if="day.meals?.length" class="section">
      <div class="section-title"><CoffeeOutlined /> 餐饮</div>
      <div v-for="(m, i) in day.meals" :key="i" class="meal-item">
        <Tag :color="m.meal_type === '早餐' ? 'orange' : m.meal_type === '午餐' ? 'blue' : 'purple'">
          {{ m.meal_type }}
        </Tag>
        <span class="meal-name">{{ m.restaurant }}</span>
        <span class="meal-cost">约¥{{ m.estimated_cost }}</span>
        <div class="meal-rec" v-if="m.recommendation">{{ m.recommendation }}</div>
      </div>
    </div>
  </Card>
</template>

<style scoped>
.day-card {
  margin-bottom: 12px;
}
.day-title {
  font-size: 16px;
  font-weight: 600;
}
.section {
  margin-bottom: 16px;
}
.section-title {
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 8px;
  color: #333;
}
.attraction-item {
  display: flex;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #f0f0f0;
}
.attr-index {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #1677ff;
  color: #fff;
  text-align: center;
  line-height: 24px;
  font-size: 12px;
  flex-shrink: 0;
  margin-top: 2px;
}
.attr-info {
  flex: 1;
}
.attr-name {
  font-weight: 600;
}
.attr-detail {
  font-size: 12px;
  color: #999;
  margin-top: 2px;
}
.attr-meta {
  margin-top: 4px;
}
.attr-desc {
  font-size: 12px;
  color: #666;
  margin-top: 4px;
}
.route-item {
  padding: 6px 0;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}
.route-info {
  color: #333;
}
.route-stats {
  color: #999;
  margin-left: auto;
}
.meal-item {
  padding: 6px 0;
  font-size: 13px;
}
.meal-name {
  font-weight: 500;
  margin-left: 8px;
}
.meal-cost {
  color: #fa8c16;
  margin-left: 8px;
}
.meal-rec {
  font-size: 12px;
  color: #999;
  margin-top: 2px;
  margin-left: 44px;
}
.empty-day {
  padding: 24px 0;
}
</style>
