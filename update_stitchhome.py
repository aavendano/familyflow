with open("frontend/src/pages/StitchHome.jsx", "r") as f:
    content = f.read()

content = content.replace("const { next_event, tasks, activities } = dashboard || {};", "const { next_event, tasks, activities, groceries } = dashboard || {};")

old_groceries_card = """
          <div className="bg-white p-4 rounded-xl border border-slate-100 shadow-sm">
            <div className="flex items-center gap-2 text-orange-500 mb-1">
              <ShoppingCart size={18} />
              <span className="text-xs font-bold uppercase tracking-tight">Groceries</span>
            </div>
            <p className="text-xl font-bold text-slate-900">Weekly Needs</p>
            <p className="text-xs text-slate-500 mt-2">Tap to view list</p>
          </div>
"""

new_groceries_card = """
          <div className="bg-white p-4 rounded-xl border border-slate-100 shadow-sm cursor-pointer hover:bg-slate-50 transition-colors" onClick={() => setActiveTab('groceries')}>
            <div className="flex items-center gap-2 text-orange-500 mb-1">
              <ShoppingCart size={18} />
              <span className="text-xs font-bold uppercase tracking-tight">Groceries</span>
            </div>
            <p className="text-xl font-bold text-slate-900">{groceries?.purchased || 0} / {groceries?.total || 0}</p>
            <div className="w-full bg-slate-100 h-1.5 rounded-full mt-2">
              <div className="bg-orange-500 h-full rounded-full transition-all duration-500" style={{ width: groceries?.total > 0 ? `${(groceries.purchased/groceries.total)*100}%` : '0%' }}></div>
            </div>
          </div>
"""

content = content.replace(old_groceries_card.strip(), new_groceries_card.strip())

with open("frontend/src/pages/StitchHome.jsx", "w") as f:
    f.write(content)
