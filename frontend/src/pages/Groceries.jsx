import React, { useState, useEffect } from 'react';
import { ShoppingCart, CheckCircle, Plus, Trash2, Circle } from 'lucide-react';
import { apiFetch } from '../lib/api';

export default function GroceriesView() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newItemName, setNewItemName] = useState('');

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = () => {
    setLoading(true);
    apiFetch('/api/families/1/groceries/')
      .then(data => {
        setItems(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Error fetching groceries:", err);
        setLoading(false);
      });
  };

  const handleAddItem = (e) => {
    e.preventDefault();
    if (!newItemName.trim()) return;

    apiFetch('/api/families/1/groceries/', {
      method: 'POST',
      body: JSON.stringify({ name: newItemName.trim() })
    })
    .then(() => {
      setNewItemName('');
      fetchItems();
    })
    .catch(err => console.error("Error adding grocery item:", err));
  };

  const handleToggleItem = (itemId, isPurchased) => {
    apiFetch(`/api/families/1/groceries/${itemId}`, {
      method: 'PUT',
      body: JSON.stringify({ is_purchased: !isPurchased })
    })
    .then(() => {
      // Optimistic update
      setItems(items.map(item =>
        item.id === itemId ? { ...item, is_purchased: !isPurchased } : item
      ).sort((a, b) => a.is_purchased - b.is_purchased));
    })
    .catch(err => console.error("Error updating grocery item:", err));
  };

  const handleDeleteItem = (itemId) => {
    apiFetch(`/api/families/1/groceries/${itemId}`, {
      method: 'DELETE'
    })
    .then(() => {
      setItems(items.filter(item => item.id !== itemId));
    })
    .catch(err => console.error("Error deleting grocery item:", err));
  };

  if (loading && items.length === 0) {
    return <div className="flex justify-center items-center h-40">Loading groceries...</div>;
  }

  return (
    <div className="flex flex-col h-full bg-slate-50">
      <div className="flex-1 overflow-y-auto pb-24">
        {items.length === 0 ? (
          <div className="flex flex-col items-center justify-center p-8 text-center text-slate-500 mt-10">
            <ShoppingCart size={48} className="mb-4 text-slate-300" />
            <p>Your grocery list is empty.</p>
            <p className="text-sm">Add items below.</p>
          </div>
        ) : (
          <ul className="divide-y divide-slate-100 bg-white shadow-sm rounded-xl m-4 overflow-hidden">
            {items.map(item => (
              <li key={item.id} className="p-4 flex items-center justify-between hover:bg-slate-50">
                <div
                  className="flex items-center gap-3 flex-1 cursor-pointer"
                  onClick={() => handleToggleItem(item.id, item.is_purchased)}
                >
                  {item.is_purchased ? (
                    <CheckCircle className="text-green-500" size={24} />
                  ) : (
                    <Circle className="text-slate-300" size={24} />
                  )}
                  <span className={`text-slate-700 ${item.is_purchased ? 'line-through text-slate-400' : 'font-medium'}`}>
                    {item.name}
                  </span>
                  {item.quantity && (
                    <span className="text-sm text-slate-400">({item.quantity})</span>
                  )}
                </div>
                <button
                  onClick={() => handleDeleteItem(item.id)}
                  className="p-2 text-slate-300 hover:text-red-500 transition-colors ml-2"
                >
                  <Trash2 size={18} />
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="absolute bottom-20 left-0 right-0 p-4 bg-white border-t border-slate-100">
        <form onSubmit={handleAddItem} className="flex gap-2">
          <input
            type="text"
            value={newItemName}
            onChange={(e) => setNewItemName(e.target.value)}
            placeholder="Add new item..."
            className="flex-1 px-4 py-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm bg-slate-50"
          />
          <button
            type="submit"
            disabled={!newItemName.trim()}
            className="bg-blue-600 text-white px-5 py-3 rounded-xl font-medium disabled:opacity-50 flex items-center gap-2 hover:bg-blue-700 active:bg-blue-800 transition-colors shadow-sm"
          >
            <Plus size={18} />
            <span className="hidden sm:inline">Add</span>
          </button>
        </form>
      </div>
    </div>
  );
}
