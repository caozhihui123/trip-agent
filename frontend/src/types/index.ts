export interface Attraction {
  name: string
  address: string
  lng: number
  lat: number
  visit_duration: string
  ticket_price: number
  description: string
  poi_id: string | null
}

export interface Meal {
  restaurant: string
  address: string
  lng: number
  lat: number
  meal_type: string
  estimated_cost: number
  recommendation: string
}

export interface Hotel {
  name: string
  address: string
  lng: number
  lat: number
  price_per_night: number
  rating: string
}

export interface Route {
  from_place: string
  to_place: string
  mode: string
  distance: string
  duration: string
  polyline?: string | null
}

export interface DayPlan {
  day: number
  date: string
  attractions: Attraction[]
  meals: Meal[]
  routes: Route[]
}

export interface BudgetDetail {
  tickets: number
  hotel: number
  dining: number
  transportation: number
  total: number
}

export interface TripPlan {
  city: string
  days: number
  schedule: DayPlan[]
  hotel: Hotel | null
  budget: BudgetDetail
  weather: WeatherDay[]
  tips: string[]
}

export interface WeatherDay {
  date: string
  day_weather: string
  night_weather: string
  day_temp: number
  night_temp: number
}

export interface TripFormData {
  city: string
  start_date: string
  days: number
  budget: number
  preferences: string[]
  transportation: string
  hotel_preference: string
}
