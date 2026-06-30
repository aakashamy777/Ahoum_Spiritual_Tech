'use client';
import { useEffect, useState } from 'react';
import ProtectedRoute from '@/components/ProtectedRoute';
import { api } from '@/lib/api';
import { useAuth } from '@/lib/auth';
import LoadingSpinner from '@/components/LoadingSpinner';

export default function Dashboard() {
  const [tab, setTab] = useState('bookings');
  const [bookings, setBookings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const { user, setUser } = useAuth();
  
  const [formData, setFormData] = useState({ name: '', bio: '', avatar_url: '' });

  useEffect(() => {
    if (tab === 'bookings') {
      setLoading(true);
      api.get('/api/bookings/')
        .then(res => setBookings(res.data.results || res.data))
        .finally(() => setLoading(false));
    }
  }, [tab]);

  useEffect(() => {
    if (user) {
      setFormData({ name: user.name || '', bio: user.bio || '', avatar_url: user.avatar_url || '' });
    }
  }, [user]);

  const handleCancel = async (id: number) => {
    try {
      await api.patch(`/api/bookings/${id}/`, { status: 'cancelled' });
      setBookings(bookings.map((b: any) => b.id === id ? { ...b, status: 'cancelled' } : b));
    } catch (err) {
      alert('Failed to cancel');
    }
  };

  const handleProfileSave = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await api.patch('/api/users/me/', formData);
      setUser(res.data);
      alert('Profile updated');
    } catch (err) {
      alert('Update failed');
    }
  };

  const switchToCreator = async () => {
    try {
      const res = await api.patch('/api/users/me/', { role: 'creator' });
      setUser(res.data);
      alert('Switched to Creator!');
    } catch (err) {
      alert('Failed to switch role');
    }
  };

  return (
    <ProtectedRoute>
      <div className="py-8">
        <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
        <div className="flex gap-4 mb-8 border-b border-gray-800 pb-2">
          <button onClick={() => setTab('bookings')} className={tab === 'bookings' ? 'text-[#F59E0B]' : 'text-gray-400'}>My Bookings</button>
          <button onClick={() => setTab('profile')} className={tab === 'profile' ? 'text-[#F59E0B]' : 'text-gray-400'}>Profile</button>
        </div>

        {tab === 'bookings' && (
          <div>
            {loading ? <LoadingSpinner /> : bookings.length > 0 ? (
              <div className="space-y-4">
                {bookings.map((b: any) => (
                  <div key={b.id} className="bg-[#1a1a2e] p-4 rounded border border-gray-800 flex justify-between items-center">
                    <div>
                      <h3 className="font-bold">{b.session_details?.title || 'Session'}</h3>
                      <p className="text-sm text-gray-400">Status: {b.status}</p>
                    </div>
                    {b.status !== 'cancelled' && (
                      <button onClick={() => handleCancel(b.id)} className="text-red-400 hover:text-red-300 text-sm">Cancel</button>
                    )}
                  </div>
                ))}
              </div>
            ) : <p className="text-gray-500">No bookings yet.</p>}
          </div>
        )}

        {tab === 'profile' && (
          <div className="max-w-md">
            <form onSubmit={handleProfileSave} className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-1">Name</label>
                <input type="text" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} className="w-full bg-gray-800 border border-gray-700 rounded p-2" />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Bio</label>
                <textarea value={formData.bio} onChange={e => setFormData({...formData, bio: e.target.value})} className="w-full bg-gray-800 border border-gray-700 rounded p-2 h-24" />
              </div>
              <button type="submit" className="bg-[#F59E0B] text-black px-4 py-2 rounded font-bold">Save Profile</button>
            </form>

            {user?.role !== 'creator' && (
              <div className="mt-12 pt-8 border-t border-gray-800">
                <h3 className="text-xl font-bold mb-2">Become a Creator</h3>
                <p className="text-sm text-gray-400 mb-4">Start hosting your own sessions and earning.</p>
                <button onClick={switchToCreator} className="bg-gray-800 hover:bg-gray-700 text-white px-4 py-2 rounded border border-gray-700">Switch to Creator</button>
              </div>
            )}
          </div>
        )}
      </div>
    </ProtectedRoute>
  );
}
