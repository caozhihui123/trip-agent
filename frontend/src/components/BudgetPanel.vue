<script setup lang="ts">
import { computed } from 'vue'
import { Card, Progress } from 'ant-design-vue'
import type { BudgetDetail, Hotel } from '../types'

const props = defineProps<{ budget: BudgetDetail; days: number; hotel: Hotel | null }>()

const maxVal = computed(() => Math.max(props.budget.total, 1))

const items = computed(() => [
  { label: '门票', value: props.budget.tickets, color: '#1677ff' },
  { label: '酒店', value: props.budget.hotel, color: '#52c41a', extra: props.hotel ? `${props.hotel.name} × ${props.days}晚` : '' },
  { label: '餐饮', value: props.budget.dining, color: '#fa8c16' },
  { label: '交通', value: props.budget.transportation, color: '#722ed1' },
])
</script>

<template>
  <Card size="small" title="预算明细">
    <div class="budget-list">
      <div v-for="item in items" :key="item.label" class="budget-item">
        <div class="budget-label">
          <span>{{ item.label }}</span>
          <span class="budget-value">¥{{ item.value }}</span>
        </div>
        <Progress
          :percent="maxVal ? Math.round(item.value / maxVal * 100) : 0"
          :stroke-color="item.color"
          :show-info="false"
          size="small"
        />
        <div class="budget-extra" v-if="item.extra">{{ item.extra }}</div>
      </div>
    </div>
    <div class="budget-total">
      总计：<strong>¥{{ budget.total }}</strong>
    </div>
  </Card>
</template>

<style scoped>
.budget-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.budget-item {
  font-size: 13px;
}
.budget-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2px;
}
.budget-value {
  font-weight: 600;
}
.budget-extra {
  font-size: 11px;
  color: #999;
  margin-top: 2px;
}
.budget-total {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
  text-align: right;
  font-size: 15px;
}
.budget-total strong {
  color: #f5222d;
  font-size: 18px;
}
</style>
