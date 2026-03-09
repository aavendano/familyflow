import { apiFetch } from '../lib/api';
import React, { useState, useEffect } from 'react'
import { CheckCircle2, Circle } from 'lucide-react'

export default function TasksView() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    apiFetch('/api/families/1/tasks/')
      .then(data => {
        setTasks(data)
        setLoading(false)
      })
      .catch(err => {
        console.error("Failed to fetch tasks:", err)
        setLoading(false)
      })
  }, [])

  return (
    <div className="space-y-4">
      {loading ? (
        <p className="text-center text-slate-500">Loading tasks...</p>
      ) : tasks.length === 0 ? (
        <div className="bg-white p-4 rounded-xl shadow-sm border border-slate-100 text-center">
          <p className="text-slate-500">All caught up!</p>
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-sm overflow-hidden border border-slate-100">
          <ul className="divide-y divide-slate-100">
            {tasks.map(task => (
              <li key={task.id} className="p-4 flex items-center hover:bg-slate-50 cursor-pointer">
                {task.is_completed ? (
                  <CheckCircle2 className="text-green-500 mr-3 shrink-0" />
                ) : (
                  <Circle className="text-slate-300 hover:text-blue-500 mr-3 shrink-0" />
                )}
                <div className="flex-1">
                  <h3 className={`font-medium ${task.is_completed ? 'text-slate-400 line-through' : 'text-slate-900'}`}>
                    {task.title}
                  </h3>
                  {task.due_date && (
                    <p className="text-xs text-red-500 mt-1">
                      Due: {new Date(task.due_date).toLocaleDateString()}
                    </p>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
