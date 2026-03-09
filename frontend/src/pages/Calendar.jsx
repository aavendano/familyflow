import { apiFetch } from '../lib/api';
import React, { useState, useEffect } from 'react'

export default function CalendarView() {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    apiFetch('/api/families/1/events/')
      .then(data => {
        setEvents(data)
        setLoading(false)
      })
      .catch(err => {
        console.error("Failed to fetch events:", err)
        setLoading(false)
      })
  }, [])

  return (
    <div className="space-y-4">
      {loading ? (
        <p className="text-center text-slate-500">Loading calendar...</p>
      ) : events.length === 0 ? (
        <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-100 text-center">
          <p className="text-slate-500">No events found. Tap + to add one.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {events.map(event => (
            <div key={event.id} className="bg-white p-4 rounded-xl shadow-sm border-l-4 border-l-blue-500 hover:bg-slate-50 cursor-pointer">
              <h3 className="font-semibold text-slate-900">{event.title}</h3>
              <p className="text-sm text-slate-500 mt-1">
                {new Date(event.start_time).toLocaleString()} - {new Date(event.end_time).toLocaleString()}
              </p>
              {event.location && <p className="text-xs text-slate-400 mt-2">📍 {event.location}</p>}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
