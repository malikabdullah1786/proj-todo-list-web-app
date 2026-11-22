import { Trash2, CheckCircle, Circle } from 'lucide-react';

interface Task {
  id: number;
  title: string;
  priority: 'low' | 'medium' | 'high';
  due_date: string;
  status: boolean;
}

interface TaskCardProps {
  task: Task;
  onUpdate: (id: number, status: boolean) => void;
  onDelete: (id: number) => void;
}

export default function TaskCard({ task, onUpdate, onDelete }: TaskCardProps) {
  const priorityColors = {
    low: 'bg-blue-100 text-blue-800',
    medium: 'bg-yellow-100 text-yellow-800',
    high: 'bg-red-100 text-red-800',
  };

  return (
    <div className="flex items-center justify-between p-4 bg-white rounded-lg shadow-sm border border-slate-200">
      <div className="flex items-center gap-4">
        <button onClick={() => onUpdate(task.id, !task.status)}>
          {task.status ? (
            <CheckCircle className="w-6 h-6 text-green-500" />
          ) : (
            <Circle className="w-6 h-6 text-slate-400" />
          )}
        </button>
        <div>
          <h3 className={`font-medium ${task.status ? 'line-through text-slate-500' : 'text-slate-900'}`}>
            {task.title}
          </h3>
          <div className="flex gap-2 text-xs mt-1">
            <span className={`px-2 py-0.5 rounded-full ${priorityColors[task.priority]}`}>
              {task.priority}
            </span>
            <span className="text-slate-500">
              {new Date(task.due_date).toLocaleDateString()}
            </span>
          </div>
        </div>
      </div>
      <button 
        onClick={() => onDelete(task.id)}
        className="text-slate-400 hover:text-red-500 transition-colors"
      >
        <Trash2 className="w-5 h-5" />
      </button>
    </div>
  );
}
