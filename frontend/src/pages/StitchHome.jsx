import { apiFetch } from '../lib/api';
import React, { useState, useEffect } from 'react';
import { Activity, Bell, Calendar, Home, CheckCircle, ShoppingCart, Plus, CheckSquare, Users } from 'lucide-react';

export default function StitchHome({ setActiveTab }) {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiFetch('/api/families/1/dashboard-summary/')
      .then(data => {
        setDashboard(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching dashboard summary:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="flex justify-center items-center h-full">Loading...</div>;
  }

  const { next_event, tasks, activities } = dashboard || {};

  return (
    <div className="relative flex h-full max-w-md w-full mx-auto flex-col bg-white overflow-hidden shadow-sm">
      {/* Top Header */}
      <header className="flex items-center justify-between px-6 py-4 bg-white border-b border-slate-100">
        <h1 className="text-blue-500 text-2xl font-bold tracking-tight">FamilyFlow</h1>
        <div className="flex items-center gap-4">
          <button className="relative p-2 text-slate-600 hover:bg-blue-50 rounded-full transition-colors">
            <Bell size={24} />
            {activities && activities.length > 0 && <span className="absolute top-2 right-2 flex h-2 w-2 rounded-full bg-red-500"></span>}
          </button>
          <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center overflow-hidden border border-blue-200">
            <img
              alt="User Profile"
              className="w-full h-full object-cover"
              src="https://ui-avatars.com/api/?name=Admin+User&background=0D8ABC&color=fff"
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto px-6 pt-6 pb-28">
        {/* Today's Overview */}
        <section className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-slate-900">Today's Overview</h2>
            <span className="text-xs font-semibold text-blue-600 bg-blue-50 px-2 py-1 rounded-full">
              {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
            </span>
          </div>
          <div className="relative overflow-hidden rounded-xl bg-gradient-to-br from-blue-500 to-blue-700 p-6 text-white shadow-lg shadow-blue-500/20">
            <div className="relative z-10">
              <p className="text-blue-100 text-sm font-medium opacity-90 uppercase tracking-wider">Next Event</p>
              {next_event ? (
                 <>
                   <h3 className="mt-1 text-2xl font-bold">{next_event.title}</h3>
                   <div className="mt-4 flex flex-col gap-2">
                     <div className="flex items-center gap-2 text-sm font-medium bg-white/20 backdrop-blur-md px-3 py-1.5 rounded-lg w-fit">
                       <Calendar size={16} /> {new Date(next_event.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                     </div>
                   </div>
                 </>
              ) : (
                <h3 className="mt-1 text-xl font-bold text-blue-100">No upcoming events</h3>
              )}
            </div>
            {/* Decorative background pattern */}
            <div className="absolute -right-8 -bottom-8 w-32 h-32 bg-white/10 rounded-full blur-2xl"></div>
          </div>
        </section>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 gap-4 mb-8">
          <div className="bg-white p-4 rounded-xl border border-slate-100 shadow-sm cursor-pointer hover:bg-slate-50 transition-colors" onClick={() => setActiveTab('tasks')}>
            <div className="flex items-center gap-2 text-blue-500 mb-1">
              <CheckSquare size={18} />
              <span className="text-xs font-bold uppercase tracking-tight">Tasks</span>
            </div>
            <p className="text-xl font-bold text-slate-900">{tasks?.completed || 0} / {tasks?.total || 0}</p>
            <div className="w-full bg-slate-100 h-1.5 rounded-full mt-2">
              <div className="bg-blue-500 h-full rounded-full transition-all duration-500" style={{ width: tasks?.total > 0 ? `${(tasks.completed/tasks.total)*100}%` : '0%' }}></div>
            </div>
          </div>
          <div className="bg-white p-4 rounded-xl border border-slate-100 shadow-sm">
            <div className="flex items-center gap-2 text-orange-500 mb-1">
              <ShoppingCart size={18} />
              <span className="text-xs font-bold uppercase tracking-tight">Groceries</span>
            </div>
            <p className="text-xl font-bold text-slate-900">Weekly Needs</p>
            <p className="text-xs text-slate-500 mt-2">Tap to view list</p>
          </div>
        </div>

        {/* Recent Activity Timeline */}
        <section>
          <h3 className="text-lg font-bold mb-4 text-slate-900">Recent Activity</h3>
          <div className="space-y-0">
            {(!activities || activities.length === 0) ? (
               <p className="text-sm text-slate-500">No recent activity.</p>
            ) : (
              activities.map((activity, index) => {
                let Icon = Activity;
                let bgClass = "bg-blue-50";
                let textClass = "text-blue-600";

                if (activity.entity_type === 'Event') {
                  Icon = Calendar;
                  bgClass = "bg-blue-50";
                  textClass = "text-blue-600";
                } else if (activity.entity_type === 'Task') {
                  Icon = CheckCircle;
                  bgClass = "bg-green-50";
                  textClass = "text-green-600";
                } else if (activity.entity_type === 'Grocery') {
                  Icon = ShoppingCart;
                  bgClass = "bg-orange-50";
                  textClass = "text-orange-600";
                }

                return (
                  <div key={activity.id} className="flex gap-4">
                    <div className="flex flex-col items-center">
                      <div className={`flex h-10 w-10 items-center justify-center rounded-full ${bgClass} ${textClass}`}>
                        <Icon size={20} />
                      </div>
                      {index < activities.length - 1 && (
                         <div className="w-0.5 grow bg-slate-100 my-1 min-h-[2rem]"></div>
                      )}
                    </div>
                    <div className="flex-1 pb-6 pt-1">
                      <div className="flex justify-between items-start">
                        <div>
                          <p className="text-sm font-bold text-slate-900">{activity.actor_name} {activity.action}</p>
                          <p className="text-sm text-slate-500 mt-0.5">{new Date(activity.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                )
              })
            )}
          </div>
        </section>
      </main>

      {/* Floating Action Button */}
      <button className="absolute bottom-24 right-6 flex h-14 w-14 items-center justify-center rounded-full bg-blue-600 text-white shadow-xl shadow-blue-500/40 hover:scale-105 active:scale-95 transition-transform z-20">
        <Plus size={28} />
      </button>

      {/* Bottom Navigation Bar */}
      <nav className="absolute bottom-0 w-full border-t border-slate-100 bg-white/90 backdrop-blur-xl px-4 pb-6 pt-2 z-10">
        <div className="flex items-center justify-around">
          <button onClick={() => setActiveTab('home')} className="flex flex-col items-center gap-1 group">
            <div className={`flex h-10 w-10 items-center justify-center rounded-xl transition-colors bg-blue-50 text-blue-600`}>
              <Home size={22} className="fill-current" />
            </div>
            <span className={`text-[10px] font-bold uppercase tracking-wider text-blue-600`}>Home</span>
          </button>

          <button onClick={() => setActiveTab('calendar')} className="flex flex-col items-center gap-1 group">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl transition-colors text-slate-400 hover:bg-slate-100">
              <Calendar size={22} />
            </div>
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Calendar</span>
          </button>

          <button onClick={() => setActiveTab('tasks')} className="flex flex-col items-center gap-1 group">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl transition-colors text-slate-400 hover:bg-slate-100">
              <CheckSquare size={22} />
            </div>
            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Tasks</span>
          </button>

          <button className="flex flex-col items-center gap-1 group">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl text-slate-400 group-hover:bg-slate-100 transition-colors">
              <Users size={22} />
            </div>
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Family</span>
          </button>
        </div>
      </nav>
    </div>
  );
}
