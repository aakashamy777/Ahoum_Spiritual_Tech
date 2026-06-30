'use client';
import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import SessionCard from '@/components/SessionCard';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function Home() {
  const [sessions, setSessions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [category, setCategory] = useState('');
  
  const categories = ['All', 'Meditation', 'Yoga', 'Therapy', 'Coaching', 'Other'];

  useEffect(() => {
    setLoading(true);
    const url = category && category !== 'All' ? `/api/sessions/?category=${category}` : '/api/sessions/';
    api.get(url)
      .then(res => setSessions(res.data.results || res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, [category]);

  return (
    <div>
      <div className="text-center py-16">
        <h1 className="text-5xl font-bold mb-4">Find Your Inner Peace</h1>
        <p className="text-xl text-gray-400 mb-8">Book transformative sessions with expert creators.</p>
        <div className="flex justify-center gap-4 flex-wrap">
          {categories.map(cat => (
            <button 
              key={cat} 
              onClick={() => setCategory(cat)}
              className={`px-4 py-2 rounded-full border ${category === cat || (cat === 'All' && !category) ? 'bg-[#F59E0B] text-black border-[#F59E0B]' : 'border-gray-700 hover:border-gray-500'}`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {loading ? <LoadingSpinner /> : (
        sessions.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {sessions.map((s: any) => <SessionCard key={s.id} session={s} />)}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500">No sessions found.</div>
        )
      )}
    </div>
  );
}
