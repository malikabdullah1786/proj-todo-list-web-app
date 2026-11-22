'use client';

import { useState, useEffect } from 'react';
import TaskCard from '@/components/TaskCard';
import TaskForm from '@/components/TaskForm';
import { useRouter } from 'next/navigation';

export default function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState<string>('all');
  const router = useRouter();

  const fetchTasks = async () => {
    try {
      const url = filter === 'all' 
        ? 'http://localhost:8000/tasks' 
        : `http://localhost:8000/tasks?status=${filter === 'completed'}`;
      
      const res = await fetch(url, { credentials: 'include' });
      if (res.ok) {
        const data = await res.json();
        setTasks(data);
      } else {
        router.push('/login');
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, [filter]);

  const handleUpdate = async (id: number, status: boolean) => {
    await fetch(`http://localhost:8000/tasks/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ status })
    });
    fetchTasks();
  };

  const handleDelete = async (id: number) => {
    await fetch(`http://localhost:8000/tasks/${id}`, {
      method: 'DELETE',
      credentials: 'include'
    });
    fetchTasks();
  };

  const handleLogout = async () => {
    document.cookie = "access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    router.push('/login');
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-2xl font-bold text-slate-900">Task Dashboard</h1>
        <button 
          onClick={handleLogout}
          className="px-4 py-2 text-sm bg-slate-200 text-slate-700 rounded-lg hover:bg-slate-300"
        >
          Logout
        </button>
      </div>

      <TaskForm onTaskCreated={fetchTasks} />

      <div className="flex gap-2 mb-4">
        <button 
          onClick={() => setFilter('all')} 
          className={`px-3 py-1 rounded text-sm ${filter === 'all' ? 'bg-indigo-600 text-white' : 'bg-slate-200'}`}
        >
          All
        </button>
        <button 
          onClick={() => setFilter('active')} 
          className={`px-3 py-1 rounded text-sm ${filter === 'active' ? 'bg-indigo-600 text-white' : 'bg-slate-200'}`}
        >
          Active
        </button>
        <button 
          onClick={() => setFilter('completed')} 
          className={`px-3 py-1 rounded text-sm ${filter === 'completed' ? 'bg-indigo-600 text-white' : 'bg-slate-200'}`}
        >
          Completed
        </button>
      </div>

      <div className="space-y-3">
        {tasks.map((task: any) => (
          <TaskCard key={task.id} task={task} onUpdate={handleUpdate} onDelete={handleDelete} />
        ))}
        {tasks.length === 0 && (
          <p className="text-center text-slate-500 py-8">No tasks found.</p>
        )}
      </div>
    </div>
  );
}
