<script setup lang="ts">
import { ref, watch, onMounted, nextTick } from 'vue'
import AMapLoader from '@amap/amap-jsapi-loader'
import type { TripPlan } from '../types'

const props = defineProps<{ plan: TripPlan; activeDay: number }>()

const mapContainer = ref<HTMLDivElement>()
let map: any = null
let markers: any[] = []
let polylines: any[] = []
const dayColors = ['#1677ff', '#f5222d', '#52c41a', '#fa8c16', '#722ed1', '#13c2c2', '#eb2f96']

async function initMap() {
  if (!mapContainer.value) return
  const AMap = await AMapLoader.load({
    key: 'c6f06b8087c000070ddc002a40ac07e3',
    version: '2.0',
  })
  map = new AMap.Map(mapContainer.value, {
    zoom: 12,
    center: [120.15, 30.28],
  })
}

function clearOverlays() {
  markers.forEach(m => map?.remove(m))
  polylines.forEach(p => map?.remove(p))
  markers = []
  polylines = []
}

function updateOverlays() {
  if (!map || !props.plan.schedule) return
  clearOverlays()

  const schedule = props.plan.schedule
  const activeIdx = props.activeDay

  // Show attractions for active day and previous days
  for (let i = 0; i <= activeIdx && i < schedule.length; i++) {
    const day = schedule[i]
    const color = dayColors[i % dayColors.length]
    const isActive = i === activeIdx

    day.attractions?.forEach((a) => {
      if (!a.lng || !a.lat) return
      const marker = new (window as any).AMap.Marker({
        position: [a.lng, a.lat],
        title: a.name,
        label: {
          content: `<span style="background:${color};color:#fff;padding:2px 6px;border-radius:4px;font-size:12px">${isActive ? 'D' + (i + 1) : ''}</span>`,
          offset: [0, -30],
        },
        zIndex: isActive ? 100 : 50,
        opacity: isActive ? 1 : 0.5,
      })
      marker.on('click', () => {
        const info = new (window as any).AMap.InfoWindow({
          content: `<div style="padding:8px"><b>${a.name}</b><br/>${a.address}<br/>门票: ¥${a.ticket_price}</div>`,
        })
        info.open(map, marker.getPosition())
      })
      map.add(marker)
      markers.push(marker)
    })

    // Draw routes for active day
    if (isActive && day.routes) {
      day.routes.forEach((_r, k) => {
        // Simple polyline between consecutive attractions
        if (day.attractions[k] && day.attractions[k + 1]) {
          const from = day.attractions[k]
          const to = day.attractions[k + 1]
          if (from.lng && from.lat && to.lng && to.lat) {
            const polyline = new (window as any).AMap.Polyline({
              path: [[from.lng, from.lat], [to.lng, to.lat]],
              strokeColor: color,
              strokeWeight: 3,
              strokeOpacity: 0.7,
              strokeStyle: 'dashed',
              zIndex: 90,
            })
            map.add(polyline)
            polylines.push(polyline)
          }
        }
      })
    }
  }

  if (schedule[activeIdx]?.attractions?.length) {
    const first = schedule[activeIdx].attractions[0]
    if (first.lng && first.lat) {
      map.setCenter([first.lng, first.lat])
    }
  }
}

onMounted(() => {
  initMap().then(() => updateOverlays())
})

watch(() => props.activeDay, () => updateOverlays())
watch(() => props.plan, () => {
  nextTick(() => updateOverlays())
}, { deep: true })
</script>

<template>
  <div ref="mapContainer" class="map-panel"></div>
</template>

<style scoped>
.map-panel {
  width: 100%;
  height: 380px;
  border-radius: 8px;
  overflow: hidden;
}
</style>
