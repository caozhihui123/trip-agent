import axios from 'axios'
import type { TripFormData, TripPlan } from '../types'

const http = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 180000,
})

export async function planTrip(data: TripFormData): Promise<TripPlan> {
  const res = await http.post('/api/trip/plan', data)
  return res.data
}

export async function searchPoi(keywords: string, city: string) {
  const res = await http.get('/api/map/poi/search', { params: { keywords, city } })
  return res.data
}

export async function getWeather(city: string) {
  const res = await http.get('/api/map/weather', { params: { city } })
  return res.data
}

export async function getRoute(origin: string, destination: string, mode: string, city: string) {
  const res = await http.post('/api/map/route', { origin, destination, mode, city })
  return res.data
}

export async function geocode(address: string, city: string) {
  const res = await http.get('/api/map/geocode', { params: { address, city } })
  return res.data
}
