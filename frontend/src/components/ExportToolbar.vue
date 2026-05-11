<script setup lang="ts">
import { ref } from 'vue'
import { Button, Space } from 'ant-design-vue'
import { FilePdfOutlined, CameraOutlined } from '@ant-design/icons-vue'
import type { TripPlan } from '../types'

const props = defineProps<{ plan: TripPlan }>()
const exporting = ref(false)

async function captureAllDays() {
  const el = document.getElementById('trip-result-content') as HTMLElement
  if (!el) return

  // 找到所有天的卡片容器
  const dayCards = el.querySelectorAll('[data-day-index]') as NodeListOf<HTMLElement>
  dayCards.forEach(d => d.style.setProperty('display', 'block', 'important'))
  const navItems = el.querySelectorAll('.day-nav-item') as NodeListOf<HTMLElement>
  navItems.forEach(n => n.style.setProperty('display', 'none', 'important'))

  try {
    const { default: html2canvas } = await import('html2canvas')
    const canvas = await html2canvas(el, { scale: 2, useCORS: true })
    return canvas
  } finally {
    dayCards.forEach(d => d.style.display = '')
    navItems.forEach(n => n.style.display = '')
  }
}

async function exportPDF() {
  exporting.value = true
  try {
    const canvas = await captureAllDays()
    if (!canvas) return

    const { default: jsPDF } = await import('jspdf')
    const imgData = canvas.toDataURL('image/png')
    const pdf = new jsPDF('p', 'mm', 'a4')
    const pageWidth = pdf.internal.pageSize.getWidth()
    const imgWidth = pageWidth - 20
    const imgHeight = (canvas.height * imgWidth) / canvas.width

    let heightLeft = imgHeight
    let position = 10

    pdf.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight)
    heightLeft -= pdf.internal.pageSize.getHeight() - 20

    while (heightLeft > 0) {
      position = -(pdf.internal.pageSize.getHeight() - imgHeight - 10)
      pdf.addPage()
      pdf.addImage(imgData, 'PNG', 10, position, imgWidth, imgHeight)
      heightLeft -= pdf.internal.pageSize.getHeight() - 20
    }

    pdf.save(`${props.plan.city}_旅行计划.pdf`)
  } finally {
    exporting.value = false
  }
}

async function exportImage() {
  exporting.value = true
  try {
    const canvas = await captureAllDays()
    if (!canvas) return

    const link = document.createElement('a')
    link.download = `${props.plan.city}_旅行计划.png`
    link.href = canvas.toDataURL('image/png')
    link.click()
  } finally {
    exporting.value = false
  }
}
</script>

<template>
  <Space>
    <Button :loading="exporting" @click="exportPDF">
      <template #icon><FilePdfOutlined /></template>
      导出 PDF
    </Button>
    <Button :loading="exporting" @click="exportImage">
      <template #icon><CameraOutlined /></template>
      导出图片
    </Button>
  </Space>
</template>
