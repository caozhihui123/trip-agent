import { reactive } from 'vue'
import type { TripPlan } from '../types'

export const state = reactive({
  plan: null as TripPlan | null,
  activeDay: 0,
  loading: false,
  mapMarkers: [] as Array<{ lng: number; lat: number; name: string; day: number }>,
  polylines: [] as Array<{ path: [number, number][]; color: string; day: number }>,
})
