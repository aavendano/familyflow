import { useState } from 'react'
import StitchHome from './pages/StitchHome'
import CalendarView from './pages/Calendar'
import TasksView from './pages/Tasks'
import GroceriesView from './pages/Groceries'

function App() {
  const [activeTab, setActiveTab] = useState('home')

  return (
    <div className="flex flex-col h-screen bg-slate-50 w-full md:items-center md:justify-center">
      {/* Container to restrict max-width on desktop, simulating mobile app */}
      <div className="w-full max-w-md h-full bg-white shadow-xl relative overflow-hidden">
         {activeTab === 'home' && <StitchHome setActiveTab={setActiveTab} />}
         {activeTab === 'calendar' && (
           <div className="h-full relative pb-20 overflow-y-auto">
             <div className="px-6 py-4 border-b border-slate-100 flex items-center bg-white sticky top-0 z-10">
               <h2 className="text-xl font-bold text-slate-900">Calendar</h2>
               <button onClick={() => setActiveTab('home')} className="ml-auto text-sm text-blue-600 font-medium hover:underline">Done</button>
             </div>
             <div className="p-6">
               <CalendarView />
             </div>
           </div>
         )}
         {activeTab === 'tasks' && (
           <div className="h-full relative pb-20 overflow-y-auto">
             <div className="px-6 py-4 border-b border-slate-100 flex items-center bg-white sticky top-0 z-10">
               <h2 className="text-xl font-bold text-slate-900">Tasks</h2>
               <button onClick={() => setActiveTab('home')} className="ml-auto text-sm text-blue-600 font-medium hover:underline">Done</button>
             </div>
             <div className="p-6">
               <TasksView />
             </div>
           </div>
         )}
         {activeTab === 'groceries' && (
           <div className="h-full relative pb-20 overflow-y-auto">
             <div className="px-6 py-4 border-b border-slate-100 flex items-center bg-white sticky top-0 z-10">
               <h2 className="text-xl font-bold text-slate-900">Groceries</h2>
               <button onClick={() => setActiveTab('home')} className="ml-auto text-sm text-orange-600 font-medium hover:underline">Done</button>
             </div>
             <div className="p-6 h-full pb-20">
               <GroceriesView />
             </div>
           </div>
         )}
      </div>
    </div>
  )
}

export default App
