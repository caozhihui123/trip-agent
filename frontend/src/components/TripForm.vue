<script setup lang="ts">
import { reactive, ref } from 'vue'
import { Input, DatePicker, InputNumber, Select, Button, Tag, message } from 'ant-design-vue'
import { SearchOutlined } from '@ant-design/icons-vue'
import { planTrip } from '../services/api'
import type { TripPlan } from '../types'
import dayjs from 'dayjs'

const emit = defineEmits<{
  'plan-generated': [plan: TripPlan]
  'update:loading': [loading: boolean]
}>()

defineProps<{ loading: boolean }>()

const startDate = ref<dayjs.Dayjs>()

const form = reactive({
  city: '',
  days: 3,
  budget: 3000,
  preferences: [] as string[],
  transportation: 'driving',
  hotel_preference: '舒适型',
})

const prefOptions = ['历史文化', '自然风光', '美食之旅', '亲子游玩', '网红打卡', '购物休闲']

function togglePref(p: string) {
  const idx = form.preferences.indexOf(p)
  if (idx >= 0) form.preferences.splice(idx, 1)
  else form.preferences.push(p)
}

async function submit() {
  if (!form.city || !startDate.value) {
    message.warning('请填写目的地城市和出发日期')
    return
  }
  emit('update:loading', true)
  try {
    const plan = await planTrip({
      city: form.city,
      start_date: startDate.value.format('YYYY-MM-DD'),
      days: form.days,
      budget: form.budget,
      preferences: form.preferences,
      transportation: form.transportation,
      hotel_preference: form.hotel_preference,
    })
    emit('plan-generated', plan)
    message.success('旅行计划生成成功！')
  } catch (e: any) {
    const msg = e?.response?.data?.detail || e?.message || '请求失败'
    message.error('生成失败：' + msg)
  } finally {
    emit('update:loading', false)
  }
}
</script>

<template>
  <div class="trip-form">
    <div class="form-row">
      <div class="form-item">
        <label>目的地城市</label>
        <Input v-model:value="form.city" placeholder="输入中国城市名，如：杭州" size="large" />
      </div>
      <div class="form-item">
        <label>出发日期</label>
        <DatePicker v-model:value="startDate" size="large" style="width:100%" />
      </div>
      <div class="form-item">
        <label>旅行天数</label>
        <InputNumber v-model:value="form.days" :min="1" :max="7" size="large" style="width:100%" />
      </div>
      <div class="form-item">
        <label>预算（元）</label>
        <InputNumber v-model:value="form.budget" :min="500" :step="500" size="large" style="width:100%" />
      </div>
    </div>

    <div class="form-row">
      <div class="form-item">
        <label>旅行偏好</label>
        <div class="pref-tags">
          <Tag
            v-for="p in prefOptions" :key="p"
            :color="form.preferences.includes(p) ? '#1677ff' : 'default'"
            style="cursor:pointer"
            @click="togglePref(p)"
          >
            {{ p }}
          </Tag>
        </div>
      </div>
      <div class="form-item">
        <label>交通方式</label>
        <Select v-model:value="form.transportation" size="large" style="width:100%">
          <Select.Option value="driving">自驾/打车</Select.Option>
          <Select.Option value="transit">公共交通</Select.Option>
          <Select.Option value="mixed">混合</Select.Option>
        </Select>
      </div>
      <div class="form-item">
        <label>酒店偏好</label>
        <Select v-model:value="form.hotel_preference" size="large" style="width:100%">
          <Select.Option value="经济型">经济型 (150-250元/晚)</Select.Option>
          <Select.Option value="舒适型">舒适型 (300-500元/晚)</Select.Option>
          <Select.Option value="豪华型">豪华型 (600-1000元/晚)</Select.Option>
        </Select>
      </div>
      <div class="form-item submit-item">
        <Button
          type="primary" size="large"
          :loading="$props.loading"
          :disabled="!form.city || !startDate"
          @click="submit"
        >
          <template #icon><SearchOutlined /></template>
          {{ $props.loading ? 'AI规划中...' : '生成旅行计划' }}
        </Button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.trip-form {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  margin-bottom: 24px;
}
.form-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  align-items: flex-end;
}
.form-row + .form-row {
  margin-top: 16px;
}
.form-item {
  flex: 1;
  min-width: 180px;
}
.form-item label {
  display: block;
  margin-bottom: 4px;
  font-weight: 500;
  color: #333;
}
.submit-item {
  display: flex;
  align-items: flex-end;
}
.pref-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  min-height: 40px;
  align-items: center;
}
</style>
