'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import { api } from '@/lib/api';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function CreatorDashboard() {
  const [tab, setTab] = useState('sessions');
  const [sessions, setSessions] = useState<any[]>([]);
  const [bookings, setBookings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ title: '', description: '', category: 'Meditation', price: 0, duration: 60, max_participants: 10 });

  useEffect(() => {
    fetchData();
  }, [tab]);

  const fetchData = async () => {
    setLoading(true);
    try {
      if (tab === 'sessions') {
        const res = await api.get('/api/sessions/my_sessions/');
        setSessions(res.data.results || res.data);
      } else {
        const res = await api.get('/api/bookings/creator_overview/');
        setBookings(res.data.results || res.data);
      }
    } catch(err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/api/sessions/', form);
      setShowModal(false);
      fetchData();
    } catch(err) {
      alert('Failed to create');
    }
  };

  const handleDelete = async (id: number) => {
    if(confirm('Delete this session?')) {
      await api.delete(`/api/sessions/${id}/`);
      fetchData();
    }
  };

  return (
    <ProtectedRoute role="creator">
      <div className="py-8">
        <h1 className="text-3xl font-bold mb-6">Creator Dashboard</h1>
        <div className="flex gap-4 mb-8 border-b border-gray-800 pb-2">
          <button onClick={() => setTab('sessions')} className={tab === 'sessions' ? 'text-[#F59E0B]' : 'text-gray-400'}>My Sessions</button>
          <button onClick={() => setTab('bookings')} className={tab === 'bookings' ? 'text-[#F59E0B]' : 'text-gray-400'}>Booking Overview</button>
        </div>

        {tab === 'sessions' && (
          <div>
            <div className="mb-4 flex justify-end">
              <button onClick={() => setShowModal(true)} className="bg-[#F59E0B] text-black px-4 py-2 rounded font-bold">Create Session</button>
            </div>
            {loading ? <LoadingSpinner /> : (
              <div className="space-y-4">
                {sessions.map((s: any) => (
                  <div key={s.id} className="bg-[#1a1a2e] p-4 rounded border border-gray-800 flex justify-between items-center">
                    <div>
                      <h3 className="font-bold">{s.title}</h3>
                      <p className="text-sm text-gray-400">${s.price} | {s.category}</p>
                    </div>
                    <div>
                      <button onClick={() => handleDelete(s.id)} className="text-red-400 hover:text-red-300 text-sm">Delete</button>
                    </div>
                  </div>
                ))}
                {sessions.length === 0 && <p className="text-gray-500">No sessions created yet.</p>}
              </div>
            )}
          </div>
        )}

        {tab === 'bookings' && (
          <div>
            {loading ? <LoadingSpinner /> : (
              <div className="space-y-4">
                {bookings.map((b: any) => (
                  <div key={b.id} className="bg-[#1a1a2e] p-4 rounded border border-gray-800">
                    <h3 className="font-bold">Booking #{b.id} - {b.status}</h3>
                    <p className="text-sm text-gray-400">User: {b.user_details?.name || b.user_details?.email}</p>
                    <p className="text-sm text-gray-400">Session: {b.session_details?.title}</p>
                  </div>
                ))}
                {bookings.length === 0 && <p className="text-gray-500">No bookings yet.</p>}
              </div>
            )}
          </div>
        )}

        {showModal && (
          <div className="fixed inset-0 bg-black/80 flex justify-center items-center p-4">
            <div className="bg-[#1a1a2e] p-6 rounded-xl border border-gray-800 w-full max-w-md">
              <h2 className="text-2xl font-bold mb-4">Create Session</h2>
              <form onSubmit={handleCreate} className="space-y-4">
                <input placeholder="Title" required value={form.title} onChange={e => setForm({...form, title: e.target.value})} className="w-full bg-gray-800 rounded p-2" />
                <textarea placeholder="Description" required value={form.description} onChange={e => setForm({...form, description: e.target.value})} className="w-full bg-gray-800 rounded p-2" />
                <input type="number" placeholder="Price" required value={form.price} onChange={e => setForm({...form, price: +e.target.value})} className="w-full bg-gray-800 rounded p-2" />
                <input type="number" placeholder="Duration (min)" required value={form.duration} onChange={e => setForm({...form, duration: +e.target.value})} className="w-full bg-gray-800 rounded p-2" />
                <div className="flex gap-4">
                  <button type="button" onClick={() => setShowModal(false)} className="w-full py-2 bg-gray-800 rounded">Cancel</button>
                  <button type="submit" className="w-full py-2 bg-[#F59E0B] text-black rounded font-bold">Create</button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
